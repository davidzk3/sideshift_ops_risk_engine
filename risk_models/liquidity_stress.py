from dataclasses import dataclass


@dataclass
class LiquidityStressResult:
    notional_usd: float
    estimated_slippage_pct: float
    severity: str
    note: str


def estimate_slippage(notional_usd: float, assumed_liquidity_usd: float) -> float:
    """
    Simple slippage proxy.
    Assumes slippage grows non linearly as trade size consumes liquidity.
    """
    if assumed_liquidity_usd <= 0:
        raise ValueError("Liquidity must be positive")

    ratio = notional_usd / assumed_liquidity_usd
    return min(ratio ** 1.3 * 100, 100)


def assess_liquidity(
    notional_usd: float,
    assumed_liquidity_usd: float,
) -> LiquidityStressResult:
    slippage = estimate_slippage(notional_usd, assumed_liquidity_usd)

    if slippage >= 5:
        severity = "high"
        note = "expected slippage too high, unsafe execution"
    elif slippage >= 2:
        severity = "medium"
        note = "slippage elevated, widen spread or throttle"
    else:
        severity = "low"
        note = "liquidity sufficient"

    return LiquidityStressResult(
        notional_usd=notional_usd,
        estimated_slippage_pct=slippage,
        severity=severity,
        note=note,
    )
