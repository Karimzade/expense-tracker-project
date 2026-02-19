from __future__ import annotations

from typing import Iterable

FIELDS = ["date", "type", "category", "amount", "note"]

def make_tx(date: str, tx_type: str, category: str, amount: float, note: str = "") -> dict:
    return {
        "date": date,
        "type": tx_type,           # "income" or "expense"
        "category": category,
        "amount": float(amount),
        "note": note or "",
    }

def add_transaction(ledger: list[dict], tx: dict) -> None:
    for k in FIELDS:
        if k not in tx:
            raise KeyError(f"Transaction missing field: {k}")
    ledger.append(tx)

def filter_transactions(
    ledger: Iterable[dict],
    tx_type: str | None = None,
    category: str | None = None,
) -> list[dict]:
    out = []
    for tx in ledger:
        if tx_type and tx.get("type") != tx_type:
            continue
        if category and tx.get("category") != category:
            continue
        out.append(tx)
    return out
