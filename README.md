# AIxTech Crypto Trading System v15

> Enhanced paper-only automated cryptocurrency trading information system with multi-factor adaptive strategies per asset class, refined zero-trust cyber and data security architecture, and AI-agent harness principles for safe development.

**Disclaimer:** Research and educational purposes only. No live order execution, no withdrawal permissions, no financial advice. Cryptocurrency trading involves substantial risk of loss. This is not investment advice.

## Overview
Builds on previous versions (v14 and earlier) and the AI coding-agent harness from [zeekiankok92/aixtech-agent-harness-demo](https://github.com/zeekiankok92/aixtech-agent-harness-demo). Features:

- Asset-class specific strategies: Majors (BTC/ETH), Large Alts, DeFi, Stablecoins, High-Volatility
- Regime-aware, multi-factor signals with volatility scaling, Bollinger Bands, on-chain proxies, adaptive filters, vol-adjusted sizing
- Advanced risk gates: position limits, drawdown controls, correlation awareness, multi-layer anomaly
- Zero-trust security: encryption helpers (KMS/HSM recommended for prod), hash-chained audits, expanded anomaly detection, input validation, comprehensive secret redaction
- Synthetic data mode by default for CI and safe agent development
- CI gates inspired by the harness (lint, tests, secret scan)

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m crypto_trading demo
```

## Architecture
See [docs/architecture.md](docs/architecture.md).

## Strategies
See [docs/trading-strategies.md](docs/trading-strategies.md).

## Security
See [SECURITY.md](SECURITY.md) and [docs/security-architecture.md](docs/security-architecture.md).

## Enhancements in v15
- Added Bollinger Band filters and volatility-adjusted position sizing across strategies
- Expanded on-chain activity proxies for DeFi
- Multi-layer anomaly detection in security module
- Stronger secret redaction patterns
- Updated docs for production security recommendations (IP whitelist, no withdrawals, KMS)

## Licence
MIT
