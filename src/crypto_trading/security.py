"""Zero-trust security helpers: encryption, audit, anomaly, redaction (v15 enhanced)."""
import hashlib
import hmac
import json
import re
from typing import Dict, Any, List
from cryptography.fernet import Fernet
import os

def get_fernet() -> Fernet:
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        # Generate ephemeral for demo only - NEVER use in production; use KMS/HSM
        key = Fernet.generate_key().decode()
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt_data(data: str) -> str:
    return get_fernet().encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    return get_fernet().decrypt(token.encode()).decode()

class AuditLog:
    def __init__(self):
        self.chain: List[str] = []

    def log(self, event: Dict[str, Any]) -> str:
        payload = json.dumps(event, sort_keys=True, default=str)
        prev = self.chain[-1] if self.chain else "genesis"
        digest = hashlib.sha256(f"{prev}:{payload}".encode()).hexdigest()
        self.chain.append(digest)
        # Optional HMAC for integrity
        return digest

def detect_anomaly(values: List[float], threshold: float = 3.0) -> bool:
    if len(values) < 5:
        return False
    mean = sum(values) / len(values)
    std = (sum((x - mean)**2 for x in values) / len(values))**0.5
    return abs(values[-1] - mean) > threshold * std if std > 0 else False

def multi_layer_anomaly(price_changes: List[float], volume_ratios: List[float], signal_freq: int) -> Dict[str, bool]:
    """Expanded anomaly detection."""
    return {
        "price_outlier": detect_anomaly(price_changes, 2.5),
        "volume_spike": detect_anomaly(volume_ratios, 4.0),
        "high_signal_freq": signal_freq > 10,  # too many signals in window
    }

def redact_secrets(text: str) -> str:
    patterns = [
        r'(api[_-]?key|secret|private[_-]?key|seed|mnemonic|wallet)\s*[:=]\s*\S+',
        r'(0x[a-fA-F0-9]{40,})',  # addresses
        r'([A-Za-z0-9]{32,})',  # long tokens
    ]
    for pat in patterns:
        text = re.sub(pat, r'\1=***REDACTED***' if '=' in pat or ':' in pat else '***REDACTED***', text, flags=re.I)
    return text
