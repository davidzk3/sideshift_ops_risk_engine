from datetime import datetime
from uuid import uuid4

from incidents.incident_schema import Incident


def maybe_create_incident(
    asset: str,
    price_severity: str,
    liquidity_severity: str,
    trigger: str,
) -> Incident | None:
    """
    Creates an incident if any severity is high.
    """
    if price_severity != "high" and liquidity_severity != "high":
        return None

    incident_id = f"INC-{uuid4().hex[:8]}"

    impact = []
    if price_severity == "high":
        impact.append("pricing divergence risk")
    if liquidity_severity == "high":
        impact.append("liquidity execution risk")

    return Incident(
        incident_id=incident_id,
        created_at=datetime.utcnow(),
        asset=asset,
        incident_type="execution_risk",
        severity="high",
        trigger=trigger,
        impact_summary=", ".join(impact),
        mitigation="asset paused or execution throttled",
    )
