from __future__ import annotations

from collections import defaultdict

def totals(ledger: list[dict]) -> dict:
    income = 0.0
    expenses = 0.0
    for tx in ledger:
        amt = float(tx.get("amount", 0.0))
        if tx.get("type") == "income":
            income += amt
        elif tx.get("type") == "expense":
            expenses += amt
    return {"income": income, "expenses": expenses, "balance": income - expenses}

def expense_by_category(ledger: list[dict]) -> dict[str, float]:
    per_cat: dict[str, float] = defaultdict(float)
    for tx in ledger:
        if tx.get("type") == "expense":
            per_cat[str(tx.get("category", ""))] += float(tx.get("amount", 0.0))
    return dict(sorted(per_cat.items(), key=lambda kv: (-kv[1], kv[0])))
