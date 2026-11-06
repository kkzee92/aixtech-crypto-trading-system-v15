"""Enhanced multi-factor adaptive strategies per asset class (v15)."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    name: str = "base"
    asset_class: str = "general"

    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _safe_get(self, data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        try:
            return float(data.get(key, default))
        except (TypeError, ValueError):
            return default

    def _vol_adjust(self, base_size: float, atr_pct: float) -> float:
        """Reduce size in high volatility."""
        if atr_pct > 10:
            return base_size * 0.3
        elif atr_pct > 5:
            return base_size * 0.6
        return base_size

class MajorsStrategy(BaseStrategy):
    name = "majors_hybrid_v15"
    asset_class = "majors"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        ema_50 = self._safe_get(data, "ema_50", price)
        ema_200 = self._safe_get(data, "ema_200", price)
        rsi = self._safe_get(data, "rsi", 50.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        funding_rate = self._safe_get(data, "funding_rate", 0.0)
        atr_pct = self._safe_get(data, "atr_pct", 3.0)
        regime = data.get("regime", "neutral")
        bb_upper = self._safe_get(data, "bb_upper", price * 1.02)
        bb_lower = self._safe_get(data, "bb_lower", price * 0.98)

        signal = "HOLD"
        confidence = 0.3
        reason = "Neutral"
        size_pct = 0.5

        if regime == "stress":
            return {"signal": "HOLD", "confidence": 0.1, "reason": "Stress regime - stand aside", "size_pct": 0.0, "asset_class": self.asset_class}

        if price > ema_50 > ema_200 and volume_ratio > 1.2 and price < bb_upper:
            signal, confidence, reason, size_pct = "BUY", 0.82, "Bullish trend + volume + within BB", 1.0
        elif price < ema_50 < ema_200 and volume_ratio > 1.1 and price > bb_lower:
            signal, confidence, reason, size_pct = "SELL", 0.75, "Bearish trend", 0.8
        elif rsi < 30 and price < ema_50 * 0.97 and price < bb_lower:
            signal, confidence, reason, size_pct = "BUY", 0.70, "Oversold reversion + BB", 0.6
        elif rsi > 70 and price > ema_50 * 1.03 and price > bb_upper:
            signal, confidence, reason, size_pct = "SELL", 0.65, "Overbought reversion", 0.5

        if funding_rate > 0.01 and signal == "BUY":
            confidence *= 0.85
            reason += "; high funding"
        size_pct = self._vol_adjust(size_pct, atr_pct)

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

class LargeAltsStrategy(BaseStrategy):
    name = "large_alts_momentum_v15"
    asset_class = "large_alts"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        btc_relative = self._safe_get(data, "btc_relative_strength", 1.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        macd_hist = self._safe_get(data, "macd_histogram", 0.0)
        atr_pct = self._safe_get(data, "atr_pct", 4.0)
        regime = data.get("regime", "neutral")

        signal, confidence, reason, size_pct = "HOLD", 0.4, "Awaiting confirmation", 0.4

        if regime == "stress":
            return {"signal": "HOLD", "confidence": 0.15, "reason": "Stress - reduced exposure", "size_pct": 0.1, "asset_class": self.asset_class}

        if btc_relative > 1.05 and macd_hist > 0 and volume_ratio > 1.5:
            signal, confidence, reason, size_pct = "BUY", 0.85, "RS + momentum + volume", 0.9
        elif btc_relative < 0.95 and macd_hist < 0:
            signal, confidence, reason, size_pct = "SELL", 0.75, "Underperforming BTC", 0.7

        size_pct = self._vol_adjust(size_pct, atr_pct)
        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

class DeFiStrategy(BaseStrategy):
    name = "defi_protocol_aware_v15"
    asset_class = "defi"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tvl_change = self._safe_get(data, "tvl_change_7d", 0.0)
        fee_change = self._safe_get(data, "fee_revenue_change", 0.0)
        rsi = self._safe_get(data, "rsi", 50.0)
        onchain_active = self._safe_get(data, "active_addresses_change", 0.0)

        signal, confidence, reason, size_pct = "HOLD", 0.35, "Monitoring protocol", 0.3

        if tvl_change > 0.05 and fee_change > 0.1 and rsi < 60 and onchain_active > 0.02:
            signal, confidence, reason, size_pct = "BUY", 0.78, "Growing TVL/fees + activity", 0.6
        elif tvl_change < -0.1 or fee_change < -0.15 or onchain_active < -0.05:
            signal, confidence, reason, size_pct = "SELL", 0.70, "Declining metrics", 0.5

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": size_pct, "asset_class": self.asset_class}

class StablecoinStrategy(BaseStrategy):
    name = "stable_arb_yield_v15"
    asset_class = "stablecoins"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        premium = self._safe_get(data, "premium_to_peg", 0.0)
        yield_diff = self._safe_get(data, "yield_diff_bps", 0.0)

        signal, confidence, reason, size_pct = "HOLD", 0.5, "Peg stable", 0.2

        if abs(premium) > 0.005:
            signal = "BUY" if premium < 0 else "SELL"
            confidence, reason, size_pct = 0.90, f"Arb: premium {premium:.4f}", 1.0
        elif yield_diff > 50:
            signal, confidence, reason, size_pct = "BUY", 0.68, "Yield opportunity", 0.4

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": size_pct, "asset_class": self.asset_class}

class HighVolStrategy(BaseStrategy):
    name = "high_vol_controlled_v15"
    asset_class = "high_volatility"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        atr_pct = self._safe_get(data, "atr_pct", 5.0)
        volume_spike = self._safe_get(data, "volume_ratio", 1.0)
        rsi = self._safe_get(data, "rsi", 50.0)

        signal, confidence, reason, size_pct = "HOLD", 0.2, "High vol - waiting", 0.1

        if volume_spike > 3.0 and atr_pct < 8.0 and 40 < rsi < 60:
            signal, confidence, reason, size_pct = "BUY", 0.50, "Controlled volume spike + neutral RSI", 0.15

        size_pct = self._vol_adjust(size_pct, atr_pct)
        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

STRATEGIES: Dict[str, BaseStrategy] = {
    "majors": MajorsStrategy(),
    "large_alts": LargeAltsStrategy(),
    "defi": DeFiStrategy(),
    "stablecoins": StablecoinStrategy(),
    "high_volatility": HighVolStrategy(),
}

def get_strategy(asset_class: str) -> BaseStrategy:
    return STRATEGIES.get(asset_class, MajorsStrategy())
