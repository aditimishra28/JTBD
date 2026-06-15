# JTBD — Jobs to Be Done

A structured Claude skill for **Jobs to Be Done (JTBD)** analysis. Drop in customer feedback, interview notes, surveys, support tickets, or sales notes and get a rigorous, evidence-backed JTBD analysis: the job performer, main job, job map, unmet needs, pain points, circumstances, and next-step plays.

## 📁 Repository structure

```
jtbd-analyst/
├── SKILL.md                       # Core analyst behavior + workflow (entry point)
├── references/                    # Distilled, attributed JTBD methodology
│   ├── core-concepts.md           #   five elements, roles, job types, statement formula
│   ├── job-mapping.md             #   the 8 universal job stages
│   ├── needs-and-opportunities.md #   outcome-statement formula + opportunity algorithm
│   ├── four-forces.md             #   Push / Pull / Anxiety / Habit
│   ├── interview-guides.md        #   Jobs & Switch interviews, critical-incident technique
│   ├── plays.md                   #   the play catalog across 5 value stages
│   └── sources.md                 #   attribution & further reading
├── assets/                        # Reusable, fill-in templates
│   ├── report-template.md         #   the JTBD Analysis Report
│   ├── job-map-template.md        #   job map worksheet
│   ├── jobs-interview-guide.md    #   discussion guide
│   └── outcome-survey-template.csv#   importance/satisfaction survey + sample data
├── scripts/                       # Helper tooling
│   ├── opportunity_score.py       #   ranks needs by ODI opportunity score
│   └── README.md
└── agents/
    └── openai.yaml                # portable agent definition mirroring SKILL.md

jtbd-analyst.skill                 # packaged, installable skill (zip of jtbd-analyst/)
```

This layout follows the standard Claude skill convention: a `SKILL.md` entry point that loads `references/`, `assets/`, `scripts/`, and `agents/` on demand, so the model only pulls deep methodology when a task needs it.

## 🎯 What is Jobs to Be Done?

Customers don't buy products — they "hire" them to make progress on a *job*. JTBD models that job independently of any solution: the **functional** objective first, then the **emotional** (how they want to feel) and **social** (how they want to be seen) layers. Because jobs are stable while solutions change, a good job model drives roadmaps for years.

## 🚀 Using the skill

1. Install / load `jtbd-analyst.skill` (or point Claude at the `jtbd-analyst/` folder).
2. Paste customer data or describe a scenario, or say "run a JTBD analysis."
3. The analyst extracts what's there, asks a few targeted questions, then produces the report.
4. Have rating data? Run `scripts/opportunity_score.py` on an importance/satisfaction CSV to prioritize needs.

## 📚 Methodology & attribution

The reference library is distilled and paraphrased — not reproduced — primarily from **Jim Kalbach, *The Jobs to Be Done Playbook* (Rosenfeld Media, 2020)**, with related work by Ulwick (ODI), Christensen, Moesta (Switch), Levitt, Drucker, Olsen, and Anthony. Full attribution in `jtbd-analyst/references/sources.md`. For complete treatment and worksheets, consult the primary sources directly.

## 👤 Author

Created by [aditimishra28](https://github.com/aditimishra28).

---

**Last updated:** June 15, 2026
