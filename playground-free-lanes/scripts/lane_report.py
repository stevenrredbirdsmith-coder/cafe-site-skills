#!/usr/bin/env python3
"""Lane budget report: parse CAFE receipts + budgets -> per-lane spend & remaining."""
import json
from pathlib import Path

CAFE = Path("A:/_SPA/CAFE")
BUDGETS = Path(__file__).parent / "lane_budgets.json"

def main():
    budgets = json.loads(BUDGETS.read_text()) if BUDGETS.exists() else {}
    spend = {}
    done = CAFE / "jobs" / "done"
    if done.exists():
        for f in done.glob("*.json"):
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            lane = d.get("lane", "unknown")
            spent = d.get("credits_spent") or 0
            s = spend.setdefault(lane, {"spent": 0, "jobs": 0, "cost_incurred": 0})
            s["spent"] += spent
            s["jobs"] += 1
            if d.get("cost_state") == "COST_INCURRED":
                s["cost_incurred"] += 1
    print(f"{'lane':12} {'jobs':>4} {'spent':>10} {'cap':>10} {'remaining':>12}  flags")
    for lane in sorted(set(list(spend) + list(budgets))):
        s = spend.get(lane, {"spent": 0, "jobs": 0, "cost_incurred": 0})
        b = budgets.get(lane, {})
        cap = b.get("monthly_budget")
        if isinstance(cap, (int, float)):
            remaining = cap - s["spent"]
        elif b.get("unmetered"):
            remaining = "unmetered"
        else:
            remaining = "NO BUDGET SET"
        flags = []
        if s["cost_incurred"]:
            flags.append(f"QUARANTINE({s['cost_incurred']} COST_INCURRED)")
        if cap is None and not b.get("unmetered"):
            flags.append("budget TBD")
        print(f"{lane:12} {s['jobs']:>4} {s['spent']:>10} {str(cap) if cap is not None else '-':>10} {str(remaining):>12}  {' '.join(flags)}")

if __name__ == "__main__":
    main()
