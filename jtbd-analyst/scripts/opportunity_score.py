#!/usr/bin/env python3
"""
opportunity_score.py — Rank JTBD desired-outcome statements by opportunity.

Implements the Outcome-Driven Innovation (ODI) opportunity algorithm:

    satisfaction_gap = max(importance - satisfaction, 0)
    opportunity      = importance + satisfaction_gap

Scores fall on a 0-20 range when importance and satisfaction are on 0-10 scales.
Higher = bigger opportunity (important but under-satisfied need).

Reference: references/needs-and-opportunities.md
(Methodology after Tony Ulwick / Strategyn, via Kalbach, "The JTBD Playbook", 2020.)

Usage:
    python3 opportunity_score.py needs.csv
    python3 opportunity_score.py needs.csv --scale 5      # importance/sat on 0-5
    python3 opportunity_score.py needs.csv --json

Input CSV must have columns: need_statement, importance, satisfaction
(an optional `stage` column is preserved in output if present).
"""

import argparse
import csv
import json
import sys


def opportunity(importance: float, satisfaction: float) -> float:
    """ODI opportunity score: importance + max(importance - satisfaction, 0)."""
    return importance + max(importance - satisfaction, 0.0)


def band(score: float, scale: float) -> str:
    """Human-readable opportunity band, normalized to the input scale (max 2*scale)."""
    pct = score / (2 * scale)  # 0..1
    if pct > 0.75:
        return "EXTREME (strongly underserved)"
    if pct >= 0.60:
        return "ATTRACTIVE"
    if pct >= 0.50:
        return "MODERATE"
    return "well served / low priority"


def load_rows(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"need_statement", "importance", "satisfaction"}
        missing = required - set(h.strip() for h in (reader.fieldnames or []))
        if missing:
            sys.exit(f"ERROR: CSV is missing required column(s): {', '.join(sorted(missing))}")
        rows = []
        for i, r in enumerate(reader, start=2):
            try:
                imp = float(r["importance"])
                sat = float(r["satisfaction"])
            except (TypeError, ValueError):
                sys.exit(f"ERROR: non-numeric importance/satisfaction on line {i}")
            rows.append({
                "need_statement": r["need_statement"].strip(),
                "stage": (r.get("stage") or "").strip(),
                "importance": imp,
                "satisfaction": sat,
                "satisfaction_gap": round(max(imp - sat, 0.0), 2),
                "opportunity": round(opportunity(imp, sat), 2),
            })
        return rows


def main():
    ap = argparse.ArgumentParser(description="Rank JTBD needs by ODI opportunity score.")
    ap.add_argument("csv", help="Input CSV (need_statement, importance, satisfaction[, stage])")
    ap.add_argument("--scale", type=float, default=10.0,
                    help="Max value of importance/satisfaction scale (default 10)")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    args = ap.parse_args()

    rows = load_rows(args.csv)
    for r in rows:
        r["band"] = band(r["opportunity"], args.scale)
    rows.sort(key=lambda r: r["opportunity"], reverse=True)

    if args.json:
        print(json.dumps(rows, indent=2))
        return

    print(f"\n{'Rank':<5}{'Opp':<7}{'Imp':<6}{'Sat':<6}{'Gap':<6}{'Band':<28}Need")
    print("-" * 100)
    for rank, r in enumerate(rows, start=1):
        print(f"{rank:<5}{r['opportunity']:<7}{r['importance']:<6}{r['satisfaction']:<6}"
              f"{r['satisfaction_gap']:<6}{r['band']:<28}{r['need_statement']}")
    print()


if __name__ == "__main__":
    main()
