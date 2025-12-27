def divergence_bps(price_a: float, price_b: float) -> float:
    """
    Returns absolute divergence in basis points.
    """
    if price_a <= 0 or price_b <= 0:
        raise ValueError("Prices must be positive")

    mid = (price_a + price_b) / 2.0
    diff = abs(price_a - price_b)
    return (diff / mid) * 10000.0
