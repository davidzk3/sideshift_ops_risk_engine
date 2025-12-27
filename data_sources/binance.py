import requests


BINANCE_BASE = "https://api.binance.com"


def get_spot_price(symbol: str) -> float:
    """
    symbol example: ETHUSDT
    """
    url = f"{BINANCE_BASE}/api/v3/ticker/price"
    r = requests.get(url, params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    data = r.json()
    return float(data["price"])
