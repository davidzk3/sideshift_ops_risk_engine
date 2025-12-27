import requests


HYPERLIQUID_BASE = "https://api.hyperliquid.xyz"


def get_mid_price(asset: str) -> float:
    """
    asset example: ETH
    Uses Hyperliquid info endpoint.
    """
    url = f"{HYPERLIQUID_BASE}/info"
    payload = {"type": "allMids"}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    data = r.json()

    if asset not in data:
        raise ValueError(f"Asset {asset} not found in Hyperliquid mids")

    return float(data[asset])
