# System Architecture (v15)

Modular paper-only information system:

1. **Data Ingestion**: Synthetic or injectable market data (price, indicators, on-chain proxies, funding). WebSocket/REST in live mode (not enabled by default).
2. **Strategy Engine**: Asset-class specific multi-factor adaptive strategies with regime detection and vol adjustment.
3. **Risk Manager**: Position limits, drawdown, correlation, anomaly gates independent of strategy.
4. **Security Layer**: Zero-trust helpers for encryption, audit, redaction, anomaly.
5. **Execution Simulator**: Paper signals only; no order submission.
6. **Monitoring & Audit**: Hash-chained logs, CLI demo.

Components designed for safe AI-agent development (synthetic fixtures, CI gates). See security-architecture.md for cyber/data details.
