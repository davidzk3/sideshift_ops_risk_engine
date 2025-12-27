from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Incident:
    incident_id: str
    created_at: datetime
    asset: str
    incident_type: str
    severity: str
    trigger: str
    impact_summary: str
    mitigation: str
    resolved_at: Optional[datetime] = None
    postmortem_link: Optional[str] = None
