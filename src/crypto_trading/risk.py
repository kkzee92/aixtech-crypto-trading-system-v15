"""Risk management gates."""
from typing import Dict, Any

class RiskManager:
    def __init__(self, max_drawdown: float = 0.15, max_exposure: float = 0.5):
        self.max_drawdown = max_drawdown
        self.max_exposure = max_exposure
        self.current_drawdown = 0.0

    def check_signal(self, signal: Dict[str, Any], portfolio: Dict[str, Any]) -> Dict[str, Any]:
        size = signal.get("size_pct", 0.5)
        if self.current_drawdown > self.max_drawdown:
            signal["signal"] = "HOLD"
            signal["reason"] += "; drawdown limit"
            signal["size_pct"] = 0.0
            return signal
        # Class multipliers
        class_mult = {"majors": 1.0, "large_alts": 0.7, "defi": 0.5, "stablecoins": 0.3, "high_volatility": 0.2}.get(signal.get("asset_class"), 0.5)
        signal["size_pct"] = min(size * class_mult, self.max_exposure)
        return signal
