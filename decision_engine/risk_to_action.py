from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RiskDecision:
    severity: str
    action: str
    note: str


def decide_price_divergence(divergence_bps: float, rules: Dict[str, Any]) -> RiskDecision:
    thresholds = rules["price_divergence_bps"]
    actions = rules["actions"]

    if divergence_bps >= thresholds["high"]:
        sev = "high"
    elif divergence_bps >= thresholds["medium"]:
        sev = "medium"
    elif divergence_bps >= thresholds["low"]:
        sev = "low"
    else:
        sev = "ok"

    if sev == "ok":
        return RiskDecision(severity="ok", action="none", note="within tolerance")

    return RiskDecision(
        severity=sev,
        action=actions[sev]["action"],
        note=actions[sev]["note"],
    )
