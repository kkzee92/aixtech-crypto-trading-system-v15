# Cyber and Data Security Architecture (v15)

Zero-trust design for research system, with production recommendations:

- **Input validation**: Type, range, and anomaly checks on all market data.
- **Encryption**: Fernet helpers for any sensitive config (keys never in code). In production: use AWS KMS, HashiCorp Vault, or HSM. Prefer enclave-based key custody where possible.
- **Audit logging**: Hash-chained logs for signals and decisions; immutable JSONL recommended.
- **Anomaly detection**: Statistical outliers on volume, price moves, signal frequency (multi-layer).
- **Secret redaction**: Expanded patterns for API keys, private keys, seeds, mnemonics, addresses blocked in logs/docs.
- **Least privilege**: No withdrawal scopes on API keys; paper mode default; IP allow-listing; separate keys per strategy/bot.
- **Isolation**: Synthetic data for CI and agent work; network optional and injectable. Microservices isolation for components.
- **Key hygiene**: Rotate keys every 90 days; never hardcode; environment variables or secrets manager only.
- **Monitoring**: Logs, metrics, alerts on anomalies, fill quality, error rates.
- **Kill switches**: Hard position/loss limits outside strategy logic.

Inspired by best practices (defense-in-depth, hot/warm/cold models for any custody) and the agent harness security gates. This system is paper-only.
