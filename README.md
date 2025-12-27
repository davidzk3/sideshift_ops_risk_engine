# Cross Chain Liquidity and Risk Operations Engine

An operations risk MVP that monitors real time pricing divergence across Binance and Hyperliquid, classifies severity, and outputs an ops action.

This mirrors how exchange and broker operations teams protect execution quality and inventory during fast markets.

## What it does now
- Pulls live Binance spot price
- Pulls live Hyperliquid mid price
- Computes divergence in basis points
- Applies a decision ruleset
- Outputs severity and recommended action

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
