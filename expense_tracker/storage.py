from __future__ import annotations

import csv
from pathlib import Path

FIELDS = ["date", "type", "category", "amount", "note"]

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def load_csv(path: Path) -> list[dict]:
    ledger: list[dict] = []
    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                tx = {k: (row.get(k, "") or "") for k in FIELDS}
                try:
                    tx["amount"] = float(tx["amount"])
                except ValueError:
                    continue  # skip corrupted rows rather than crash
                ledger.append(tx)
    except FileNotFoundError:
        pass
    return ledger

def save_csv(path: Path, ledger: list[dict]) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for tx in ledger:
            row = {k: tx.get(k, "") for k in FIELDS}
            try:
                row["amount"] = f"{float(row['amount']):.2f}"
            except Exception:
                row["amount"] = "0.00"
            w.writerow(row)
