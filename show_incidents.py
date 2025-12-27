import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

LOG_PATH = Path("incidents/incident_log.jsonl")
console = Console()


def load_incidents():
    if not LOG_PATH.exists():
        return []

    incidents = []
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            incidents.append(json.loads(line))
    return incidents


def print_incidents(incidents, limit=20):
    table = Table(title=f"Incident Log (latest {min(limit, len(incidents))})")
    table.add_column("id")
    table.add_column("time")
    table.add_column("asset")
    table.add_column("severity")
    table.add_column("impact")

    for i in incidents[-limit:]:
        table.add_row(
            i.get("incident_id", ""),
            i.get("created_at", ""),
            i.get("asset", ""),
            i.get("severity", ""),
            i.get("impact_summary", ""),
        )

    console.print(table)


if __name__ == "__main__":
    incidents = load_incidents()
    if not incidents:
        console.print("[yellow]No incidents found. Run python main.py with stress enabled.[/yellow]")
    else:
        print_incidents(incidents, limit=20)
