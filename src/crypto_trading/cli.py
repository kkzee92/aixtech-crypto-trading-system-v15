"""CLI entry for demo."""
import argparse
from .strategies import get_strategy
from .data import generate_synthetic
from .risk import RiskManager
from .security import AuditLog, redact_secrets

def main():
    parser = argparse.ArgumentParser(description="Crypto trading info system demo (paper-only)")
    parser.add_argument("command", choices=["demo"], nargs="?", default="demo")
    args = parser.parse_args()

    if args.command == "demo":
        audit = AuditLog()
        risk = RiskManager()
        for ac in ["majors", "large_alts", "defi", "stablecoins", "high_volatility"]:
            data = generate_synthetic(ac)
            strat = get_strategy(ac)
            sig = strat.generate_signal(data)
            sig = risk.check_signal(sig, {})
            digest = audit.log(sig)
            print(f"{ac}: {sig} | audit={digest[:8]}")
        print("Demo complete. Synthetic data only. Not financial advice.")

if __name__ == "__main__":
    main()
