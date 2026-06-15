# Transcript Intake & JTBD Extraction

> The workflow for turning an uploaded customer conversation (interview transcript, sales/support call, chat log, survey verbatims, or pasted notes) into a structured JTBD extraction **and** the right set of follow-up questions. This is the skill's primary "upload-and-analyze" path.

## When this runs

Trigger whenever the user uploads or pastes a transcript / customer conversation and wants JTBD insight — even if they don't say "JTBD." Phrases: "here's a call transcript," "analyze this interview," "what's the job here," "what should I ask next."

## Step 0 — (Optional) run the pre-tagger

If the transcript is in a file, run the helper to get a deterministic first pass:

```bash
python3 scripts/extract_transcript.py <transcript_file> > extraction_starter.md
```

It surfaces candidate signals by category, reports which of the five elements have evidence, and drafts gap-driven questions. **Treat its output as a scaffold, not the answer** — you still read the transcript yourself and apply judgment. If there's no file (pasted text), skip the script and do Step 1 directly.

## Step 1 — Extract the five elements from the transcript

Read the whole transcript first. For each element, pull **direct quotes** as evidence. Tag the speaker. Never invent — if it's not there, leave it empty and note the gap.

| Element | What to hunt for in the text | Signal phrases |
|---|---|---|
| **Job performer** | Who is actually doing the work being described (vs. who's talking) | role mentions, "my team," "I'm the one who…", "we have someone who…" |
| **Main job** | The objective beneath the request — write it as verb + object | "I'm trying to…", "I need to…", "so that…", "in order to…" |
| **Process** | Sequence and steps; map to the 8 stages | "first…", "then…", "after that…", "before I…", "finally…" |
| **Needs** | Frustrations, workarounds, desired outcomes (success criteria) | "it takes too long," "I wish," "the annoying part," "we just manually…", "I end up…" |
| **Circumstances** | Conditions that change how the job goes | "whenever…", "during…", "if it's…", "in the morning," "every time…" |
| **Emotional / social** | How they want to feel / be seen | "I feel…", "I was worried…", "stressed," "confident," "embarrassing," "look bad" |
| **Four Forces** | Only if switching is present | "we used to…", "switched from," "tried X," "considered," "stuck with" |

**Extraction heuristics**
- **Workarounds = confirmed unmet needs.** A spreadsheet hack, a manual step, a copy-paste, a "we just deal with it" → name the underlying need.
- **Complaints aren't needs yet.** "It's too slow" → reframe as a desired outcome: *minimize the time it takes to [X] when [Y]*.
- **Separate the performer from the talker.** The person on the call may be a buyer or manager describing someone else's job. Flag this.
- **Quote, don't paraphrase, for evidence.** Every extracted item gets a verbatim snippet + speaker.

## Step 2 — Score element coverage and find the gaps

After extraction, rate each element:

- **Strong** — multiple clear, quoted data points
- **Partial** — some signal, but ambiguous or thin
- **Missing** — no evidence in the transcript

The **Missing** and **Partial** elements drive your questions. Prioritize gaps in this order:
1. Job performer (is it even clear who does the job?)
2. Main job (can you write a clean verb + object?)
3. Process gaps — especially **Confirm / Monitor / Modify** (chronically under-described)
4. Needs (you have complaints but not success criteria)
5. Circumstances (what makes this job hard/easy is unclear)

## Step 3 — Generate the right follow-up questions

Pull from `assets/question-bank.md`, choosing questions that target the gaps from Step 2. Rules:

- Ask **3–5** questions, only about genuine gaps — never about things the transcript already answers.
- One idea per question (no compound questions).
- Never ask the customer to design a solution; ask about their objective, process, and needs.
- Use the **critical-incident** move when answers are generic: "Tell me about the last time this went wrong — what happened, and what should have happened?"
- Convert vague complaints into measurable probes: *"When you say it's 'too slow' — what's slow specifically, and what would fast enough look like?"*

## Step 4 — Produce the output

Present two things:

1. **A JTBD extraction** using `assets/report-template.md` — filled where there's evidence, with every item cited, and gaps marked *[insufficient data]* or *(inferred)*.
2. **A prioritized question list** — the 3–5 questions, each labeled with the element/gap it closes and a one-line reason it matters.

Then offer next steps: another transcript, a round of answers to fold in, or a play from `references/plays.md`.

## Multi-transcript mode

If several transcripts are uploaded:
- Extract each separately, then **synthesize**: needs/pains recurring across transcripts are stronger (note the count, e.g., "4 of 6 mentioned…").
- You've likely saturated when the same jobs/needs keep recurring (often 10–12 interviews — see `interview-guides.md`).
- Cluster needs by job stage; carry the highest-frequency, highest-frustration items to the top of the report.
