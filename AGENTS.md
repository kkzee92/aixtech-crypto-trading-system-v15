# Agent Rules for AIxTech Crypto Trading System

This repository follows AI coding-agent harness principles (inspired by zeekiankok92/aixtech-agent-harness-demo).

## Core Rules
- No production personal data, secrets, or live API keys in code, prompts, fixtures, or logs.
- Use only synthetic data for tests and demos.
- Paper-only / research mode: never enable live order placement or withdrawal scopes.
- All changes must pass CI gates: lint, tests, secret scans.
- Human review required for Definition of Done.
- Disclose AI assistance in commits (AI-Assisted: trailer) and PRs.

## Development Guidelines
- Prefer stdlib and minimal dependencies.
- Validate all inputs.
- Log decisions with audit trails where applicable.
- Strategies must include confidence scores and risk-aware sizing.
