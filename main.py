import yaml
from rich.console import Console
from rich.table import Table
from datetime import datetime

from data_sources.binance import get_spot_price
from data_sources.hyperliquid import get_mid_price
from risk_models.price_divergence import divergence_bps
from decision_engine.risk_to_action import decide_price_divergence
from risk_models.liquidity_stress import assess_liquidity
from incidents.incident_generator import maybe_create_incident
from incidents.incident_store import persist_incident
from incidents.incident_schema import Incident


console = Console()


def load_rules() -> dict:
    with open("decision_engine/rules.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_once(asset: str) -> dict:
    """
    asset example: ETH
    binance symbol will be ETHUSDT
    """
    rules = load_rules()

    binance_symbol = f"{asset}USDT"

    price_binance = get_spot_price(binance_symbol)
    price_hl = get_mid_price(asset)

    div_bps = divergence_bps(price_binance, price_hl)
    decision = decide_price_divergence(div_bps, rules)

    # liquidity stress assumptions
    expected_swap_usd = 600000  # keep high to force incidents while testing

    assumed_liquidity_map = {
        "ETH": 5_000_000,
        "BTC": 10_000_000,
        "SOL": 1_000_000,
    }

    assumed_liquidity = assumed_liquidity_map.get(asset, 500_000)

    liquidity_result = assess_liquidity(
        notional_usd=expected_swap_usd,
        assumed_liquidity_usd=assumed_liquidity,
    )

    # incident creation on high severity breaches
    incident = maybe_create_incident(
        asset=asset,
        price_severity=decision.severity,
        liquidity_severity=liquidity_result.severity,
        trigger="price divergence or liquidity stress breach",
    )

    print("DEBUG incident object:", incident)

    if incident:
        persist_incident(incident)

    # Forced persistence verification (temporary)
    forced_incident = Incident(
        incident_id="INC-FORCED-001",
        created_at=datetime.utcnow(),
        asset=asset,
        incident_type="forced_test",
        severity="high",
        trigger="forced write test",
        impact_summary="forced persistence verification",
        mitigation="none",
    )
    persist_incident(forced_incident)

    return {
        "asset": asset,
        "binance_spot": price_binance,
        "hyperliquid_mid": price_hl,
        "divergence_bps": div_bps,
        "price_severity": decision.severity,
        "price_action": decision.action,
        "liquidity_slippage_pct": liquidity_result.estimated_slippage_pct,
        "liquidity_severity": liquidity_result.severity,
        "liquidity_note": liquidity_result.note,
        "incident_id": incident.incident_id if incident else "",
    }


def print_table(rows: list[dict]) -> None:
    t = Table(title="Cross Chain Liquidity and Risk Operations Engine MVP")
    t.add_column("asset")
    t.add_column("div bps", justify="right")
    t.add_column("price sev")
    t.add_column("price action")
    t.add_column("slippage %", justify="right")
    t.add_column("liq sev")
    t.add_column("liq note")
    t.add_column("incident")

    for r in rows:
        t.add_row(
            r["asset"],
            f'{r["divergence_bps"]:.2f}',
            r["price_severity"],
            r["price_action"],
            f'{r["liquidity_slippage_pct"]:.2f}',
            r["liquidity_severity"],
            r["liquidity_note"],
            r["incident_id"],
        )

    console.print(t)


if __name__ == "__main__":
    assets = ["ETH", "BTC", "SOL"]
    rows = []

    for a in assets:
        try:
            rows.append(run_once(a))
        except Exception as e:
            rows.append(
                {
                    "asset": a,
                    "binance_spot": 0.0,
                    "hyperliquid_mid": 0.0,
                    "divergence_bps": 0.0,
                    "price_severity": "error",
                    "price_action": "check_feed",
                    "liquidity_slippage_pct": 0.0,
                    "liquidity_severity": "error",
                    "liquidity_note": str(e),
                    "incident_id": "",
                }
            )

    print_table(rows)
