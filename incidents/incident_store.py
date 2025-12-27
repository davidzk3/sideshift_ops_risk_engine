import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime

from incidents.incident_schema import Incident


# Resolve repo root reliably (…/sideshift_ops_risk_engine)
BASE_DIR = Path(__file__).resolve().parent.parent

# incidents/incident_log.jsonl under repo root
INCIDENT_LOG_PATH = BASE_DIR / "incidents" / "incident_log.jsonl"


def persist_incident(incident: Incident) -> None:
    """
    Append incident as JSON line for auditability.
    """
    print(">>> Persisting incident:", incident.incident_id)
    print(">>> Writing to:", INCIDENT_LOG_PATH)

    # Ensure incidents directory exists
    INCIDENT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = asdict(incident)

    # Convert datetimes to ISO strings
    for k, v in record.items():
        if isinstance(v, datetime):
            record[k] = v.isoformat()

    # Append as JSONL
    with INCIDENT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
        f.flush()

    # Hard assertion for sanity
    if not INCIDENT_LOG_PATH.exists():
        raise RuntimeError("Incident log file was not created")
