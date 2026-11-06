# Enhanced Trading Strategies by Asset Class (v15)

All strategies are multi-factor, regime-aware, volatility-adjusted, and return structured signals with confidence and size_pct.

## Majors (BTC, ETH)
Hybrid trend (EMA 50/200 + volume + Bollinger Bands) + mean reversion (RSI) with funding rate adjustment and volatility scaling. Regime filter (trend/range/stress) suppresses signals in stress. Size reduced in high ATR.

## Large Alts
Relative strength vs BTC + MACD + volume confirmation. Adaptive to BTC regime. Vol-adjusted sizing.

## DeFi
Protocol metrics (TVL change, fee revenue, active addresses) + price/RSI. Exit on fundamental deterioration.

## Stablecoins
Peg premium arbitrage and yield differential signals. Low directional risk. Higher confidence on clear arb.

## High Volatility
Strict filters: extreme volume spike + moderate ATR + neutral RSI. Tiny position sizes only. Strong vol adjustment.

See `src/crypto_trading/strategies.py` for implementation details. All research/paper only. No live execution.
