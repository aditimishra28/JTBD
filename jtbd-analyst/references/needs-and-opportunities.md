# Needs and Opportunity Scoring

> Distilled from Kalbach, *The Jobs to Be Done Playbook*, Ch. 4 ("Find Underserved Needs"), based on Ulwick's Outcome-Driven Innovation. See `sources.md`.

## Desired-outcome (need) statements

In JTBD, a **need** is a measurable success criterion for a job step — not a feature request. Write each one with four parts:

**Direction of change + Unit of measure + Object of the need + Clarifier**

- **Direction** — a verb of improvement. Prefer **"minimize" / "reduce" / "decrease"** (people can picture zero) over the fuzzier "maximize."
- **Unit of measure** — what's being measured: time, effort, number, likelihood, frequency, skill required, etc.
- **Object** — what the measure applies to.
- **Clarifier** — context that pins down the circumstance.

**Examples**

- Minimize the *time it takes to* summarize conference insights, e.g., as notes, presentations, reports.
- Reduce the *time it takes to* get ingredients ready when preparing a meal.
- Minimize the *likelihood that* a document is missing when preparing taxes, e.g., pay stubs, receipts.

Good outcome statements are stable (solution-free), granular, and non-redundant.

## The unmet-need idea

A need is an opportunity when it is **important** to the performer **and** poorly **satisfied** by current solutions. Plot needs on a 2×2 of importance (y) vs. satisfaction (x): the high-importance / low-satisfaction quadrant is where opportunity concentrates.

## The ODI opportunity algorithm

After collecting needs qualitatively and surveying job performers on **importance** and **satisfaction** (typical scale 1–10):

```
Satisfaction gap   = Importance − Satisfaction        (floored at 0)
Opportunity score  = Importance + max(Importance − Satisfaction, 0)
```

The score falls on a 0–20 range. Higher = bigger opportunity. Rough reading:

- **> 15** — extreme / strongly underserved opportunity
- **12–15** — attractive opportunity worth targeting
- **10–12** — moderate
- **< 10** — well served; low priority

> `scripts/opportunity_score.py` computes and ranks these from a CSV.

## ODI process (simplified)

1. **Gather all desired outcomes** from qualitative research with job performers — you're done when the same needs keep recurring (often 10–20+ interviews).
2. **Formulate outcome statements** consistently; have the team review and de-duplicate.
3. **Survey job performers** — pair each statement with an importance and a satisfaction scale. Sample size rule of thumb: at least 2× the number of statements; 150+ for broad domains.
4. **Compute opportunity scores** and prioritize.

**Caveats:** ODI is rigorous and costly. Cutting corners (incomplete need set, wrong sample, not actual job performers) produces unreliable or misleading results.

## Lighter-weight alternatives

- **Olsen importance-vs-satisfaction matrix** (*Lean Product Playbook*): importance on 1–5 (polar), satisfaction on a 1–7 Likert (negative satisfaction is meaningful). Can even be run with a **sample size of zero** — the team estimates positions, forms a hypothesis, and tests it with experiments (ties JTBD to Lean).
- **Anthony jobs scoring sheet** (*The Innovator's Guide to Growth*): rate each *job* 1–5 on importance, frequency, and dissatisfaction with current solutions; combine into a score to find high-opportunity jobs.
- **Job-step prioritization:** survey the stages from your job map instead of individual needs (see `job-mapping.md`).
