# Cross Chain Liquidity and Risk Operations Engine

An operations-grade risk monitoring and incident management engine for cross-venue crypto execution.

This system mirrors how exchange and broker operations teams monitor execution safety, liquidity stress, and pricing divergence across centralized and decentralized venues, and how they trigger, persist, and review incidents under adverse market conditions.

---

## What This System Does

The engine evaluates whether executing a swap is safe in real time, based on:

1. Cross-venue price divergence  
2. Liquidity depth and slippage stress  
3. Deterministic risk thresholds  
4. Automated incident creation and audit logging  

It is designed from an operations and risk ownership perspective, not as a passive analytics dashboard.

---

## Core Risk Signals

### 1. Price Divergence Risk
- Pulls live prices from Binance spot and Hyperliquid mid prices
- Computes absolute divergence in basis points
- Classifies severity using configurable thresholds
- Outputs an operational action such as monitor, widen spread, or pause asset

### 2. Liquidity Stress Risk
- Models expected execution size in USD
- Compares against assumed venue liquidity
- Estimates nonlinear slippage under stress
- Flags execution as safe, elevated, or unsafe

### 3. Incident Creation
An incident is automatically created when:
- Price severity is high, or
- Liquidity severity is high

Each incident includes:
- Unique incident ID
- Timestamp
- Asset
- Severity
- Trigger
- Impact summary
- Mitigation recommendation

---

## Incident Persistence and Audit Trail

All incidents are persisted to disk as JSON Lines (.jsonl) for auditability.

This provides:
- Append-only incident history
- Replayable ops timelines
- Inputs for postmortems or compliance review

Location:
incidents/incident_log.jsonl

The log file is intentionally excluded from version control.

---

## Incident Review Tooling

A lightweight CLI viewer (show_incidents.py) renders the incident log into a clean table for ops review.

This mirrors how operators scan recent incidents during:
- shift handover
- incident review
- risk retrospectives

---

## Project Structure

```text
sideshift_ops_risk_engine/
├── main.py
├── show_incidents.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data_sources/
│   ├── binance.py
│   └── hyperliquid.py
│
├── risk_models/
│   ├── price_divergence.py
│   └── liquidity_stress.py
│
├── decision_engine/
│   ├── rules.yaml
│   └── risk_to_action.py
│
└── incidents/
    ├── incident_schema.py
    ├── incident_generator.py
    ├── incident_store.py
    └── example_incidents.md
```
---
## How to Run

### Setup

```text
python -m venv .venv  
.venv\Scripts\activate  
pip install -r requirements.txt
```

### Run the risk engine

```text
python main.py
```

This will:
- Fetch live prices
- Evaluate price and liquidity risk
- Create incidents under stress
- Persist incidents to disk

### View incidents

```text
python show_incidents.py
```

---

## Configuration Notes

- Risk thresholds are explicit and explainable
- Liquidity assumptions are intentionally simple and conservative
- The system favors false positives over silent failure, consistent with ops best practice

---

## Why This Exists

Most crypto systems focus on charts, dashboards, and historical metrics.

This project focuses on:
- execution safety
- real-time decisioning
- failure ownership
- incident lifecycle management

It is designed to demonstrate operations risk thinking, not just data analysis.

---

## Roadmap

- Composite risk score across signals
- Venue health and API latency monitoring
- Exposure caps per asset
- Incident resolution and postmortem workflow
- Alerting via Telegram or Slack

---

## Disclaimer

This project is for educational and demonstration purposes only.  
It is not financial advice and does not connect to production trading systems.
