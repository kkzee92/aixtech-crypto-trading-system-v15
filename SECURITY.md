# Security Policy

## Supported Versions
Only the latest main branch is supported for research purposes.

## Reporting a Vulnerability
Please open a private security advisory or contact the maintainer. Do not disclose publicly until addressed.

## Security Practices
- No secrets in repository.
- API keys (if used) must have trade-only, no-withdrawal permissions, IP restrictions.
- Zero-trust: validate inputs, encrypt sensitive data at rest (helpers provided), audit logs.
- Synthetic data only in public fixtures.
- Anomaly detection for unusual signals or data.
