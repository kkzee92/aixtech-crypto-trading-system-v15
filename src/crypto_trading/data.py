"""Synthetic data generator and secure ingestion helpers (v15)."""
import random
from typing import Dict, Any

def generate_synthetic(asset_class: str = "majors") -> Dict[str, Any]:
    price = 50000 if asset_class == "majors" else 100
    base = {
        "price": price,
        "ema_50": price * random.uniform(0.97, 1.03),
        "ema_200": price * random.uniform(0.90, 1.10),
        "rsi": random.uniform(25, 75),
        "volume_ratio": random.uniform(0.7, 2.5),
        "funding_rate": random.uniform(-0.015, 0.025),
        "atr_pct": random.uniform(2, 10),
        "bb_upper": price * random.uniform(1.01, 1.05),
        "bb_lower": price * random.uniform(0.95, 0.99),
        "regime": random.choice(["trend", "range", "neutral", "stress"])
    }
    if asset_class == "large_alts":
        base.update({
            "btc_relative_strength": random.uniform(0.85, 1.15),
            "macd_histogram": random.uniform(-2, 2)
        })
    elif asset_class == "defi":
        base.update({
            "tvl_change_7d": random.uniform(-0.15, 0.20),
            "fee_revenue_change": random.uniform(-0.15, 0.25),
            "active_addresses_change": random.uniform(-0.1, 0.15)
        })
    elif asset_class == "stablecoins":
        base.update({
            "premium_to_peg": random.uniform(-0.015, 0.015),
            "yield_diff_bps": random.uniform(0, 150)
        })
    elif asset_class == "high_volatility":
        base.update({
            "atr_pct": random.uniform(5, 15),
            "volume_ratio": random.uniform(1.5, 6)
        })
    return base
