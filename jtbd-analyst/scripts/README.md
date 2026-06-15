# scripts/

Helper tools for the JTBD Analyst skill.

## opportunity_score.py

Ranks desired-outcome (need) statements by the ODI opportunity algorithm
(`importance + max(importance - satisfaction, 0)`).

```bash
# default 0-10 scales, table output
python3 opportunity_score.py ../assets/outcome-survey-template.csv

# 0-5 scales
python3 opportunity_score.py needs.csv --scale 5

# machine-readable
python3 opportunity_score.py needs.csv --json
```

Input CSV columns: `need_statement`, `importance`, `satisfaction` (optional `stage`).
Pure standard library — no dependencies. See `../references/needs-and-opportunities.md`.
