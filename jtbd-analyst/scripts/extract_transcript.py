#!/usr/bin/env python3
"""
extract_transcript.py — First-pass JTBD signal extractor for a customer transcript.

Reads a conversation (plain text, Markdown, .vtt, or .srt), surfaces candidate
JTBD signals by category, reports which of the five core elements have evidence,
and drafts gap-driven follow-up questions.

This is a DETERMINISTIC SCAFFOLD, not the analysis. It uses keyword/phrase
heuristics to pre-tag lines so the analyst (human or model) can work faster.
Always read the transcript and apply judgment on top of this output.

Reference: references/transcript-extraction.md

Usage:
    python3 extract_transcript.py call.txt
    python3 extract_transcript.py call.vtt --json
    python3 extract_transcript.py notes.md --max 8     # cap quotes shown per category
"""

import argparse
import json
import re
import sys
from collections import defaultdict

# --- Signal lexicon: category -> trigger phrases (lowercase substring match) ---
SIGNALS = {
    "main_job_goal": [
        "i'm trying to", "im trying to", "trying to", "i need to", "i want to",
        "i want", "we need to", "so that", "in order to", "my goal", "the goal is",
        "what i'm trying", "i'm looking to", "aiming to", "i have to",
    ],
    "process_step": [
        "first", "then", "after that", "after i", "next", "before i", "before that",
        "finally", "the next step", "once i", "once we", "start by", "i begin",
        "step ", "and then", "from there",
    ],
    "pain_friction": [
        "frustrat", "annoying", "annoyed", "i hate", "hate that", "difficult",
        "hard to", "takes too long", "too slow", "slow", "tedious", "painful",
        "pain", "struggle", "struggling", "problem", "issue", "headache",
        "waste", "wasting", "clunky", "confusing", "a mess", "broken",
    ],
    "workaround": [
        "workaround", "work around", "instead i", "instead we", "we just",
        "i just", "i end up", "we end up", "manually", "by hand", "copy paste",
        "copy and paste", "spreadsheet", "hack", "duct tape", "on the side",
        "outside the system", "in excel", "in a doc",
    ],
    "need_outcome": [
        "i wish", "it would be great", "if only", "what i really want",
        "would love", "would be nice", "ideally", "i need it to", "needs to",
        "make sure", "i want to avoid", "avoid", "reduce", "minimize", "faster",
        "easier", "save time",
    ],
    "emotional_social": [
        "i feel", "i felt", "feel like", "worried", "anxious", "anxiety",
        "stressed", "stress", "confident", "confidence", "relieved", "nervous",
        "scared", "afraid", "embarrass", "look bad", "look good", "judged",
        "proud", "overwhelmed", "frustrated", "happy", "comfortable",
    ],
    "circumstance": [
        "whenever", "every time", "during", "in the morning", "at the end of",
        "when i", "when we", "if it's", "if there's", "usually", "typically",
        "most of the time", "on busy", "under pressure", "deadline", "at night",
        "end of the month", "end of quarter", "peak",
    ],
    "switching_force": [
        "we used to", "i used to", "switched from", "switched to", "moved from",
        "moved to", "we tried", "i tried", "looking for", "considered",
        "stuck with", "our current", "the old", "before we had", "migrated",
        "shopping around", "evaluating",
    ],
    "performer_role": [
        "my team", "my job", "i'm the one", "im the one", "i'm responsible",
        "responsible for", "my role", "as a ", "i'm a ", "im a ", "we have someone",
        "the person who", "whoever", "our analysts", "our reps", "the team that",
    ],
}

# Which signal categories provide evidence for each of the five (+2) elements.
ELEMENT_EVIDENCE = {
    "Job performer": ["performer_role"],
    "Main job": ["main_job_goal"],
    "Process": ["process_step"],
    "Needs": ["pain_friction", "workaround", "need_outcome"],
    "Circumstances": ["circumstance"],
    "Emotional/Social jobs": ["emotional_social"],
    "Four Forces (switching)": ["switching_force"],
}

# Gap-driven question bank (mirrors assets/question-bank.md).
QUESTIONS = {
    "Job performer": [
        "Who actually does this day-to-day — is it you, or someone on your team?",
        "Whose problem is this most — who feels the pain when it goes wrong?",
    ],
    "Main job": [
        "Stepping back from the tools — what are you ultimately trying to accomplish here?",
        "If this worked perfectly, what would you have gotten done by the end?",
    ],
    "Process": [
        "Walk me through it start to finish — what's the very first step, and the last?",
        "After [that step], how do you know it was done correctly before moving on?",
        "What happens when something looks off mid-way — how do you catch and fix it?",
    ],
    "Needs": [
        "When you say it's '[their complaint]' — what specifically is slow/hard, and what would good enough look like?",
        "What workarounds have you built to cope with this today?",
        "What's the single most annoying part, and why is that the one that gets you?",
    ],
    "Circumstances": [
        "In which situations does this go smoothly vs. badly — what's different about the bad ones?",
        "What conditions (timing, volume, pressure) change how you approach it?",
    ],
    "Emotional/Social jobs": [
        "How do you want to feel while doing this — and how does it feel today?",
        "Does anyone else see the result of this work? How do you want to come across to them?",
    ],
    "Four Forces (switching)": [
        "What made you start looking for a different way of doing this?",
        "What's giving you pause about changing — what are you worried might go wrong?",
    ],
}

CRITICAL_INCIDENT = (
    "Tell me about the last specific time this went wrong — what happened, "
    "how did you feel, and what should have happened instead?"
)


def parse_transcript(text):
    """Return list of (speaker, line) tuples. Handles 'Name: text', VTT, SRT, plain."""
    turns = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        # Skip VTT/SRT timing + index lines
        if line == "WEBVTT" or "-->" in line:
            continue
        if re.fullmatch(r"\d+", line):  # SRT sequence number
            continue
        # "Speaker: utterance"
        m = re.match(r"^([A-Z][\w .'\-]{0,40}?):\s+(.*)$", line)
        if m and len(m.group(1).split()) <= 5:
            turns.append((m.group(1).strip(), m.group(2).strip()))
        else:
            turns.append((None, line))
    return turns


def tag(turns):
    """category -> list of (speaker, quote) matches."""
    hits = defaultdict(list)
    seen = defaultdict(set)
    for speaker, line in turns:
        low = line.lower()
        for cat, phrases in SIGNALS.items():
            for p in phrases:
                if p in low:
                    key = (speaker, line)
                    if line not in seen[cat]:
                        hits[cat].append((speaker, line))
                        seen[cat].add(line)
                    break
    return hits


def coverage(hits):
    """element -> ('Strong'|'Partial'|'Missing', count)."""
    cov = {}
    for element, cats in ELEMENT_EVIDENCE.items():
        n = sum(len(hits.get(c, [])) for c in cats)
        if n >= 3:
            status = "Strong"
        elif n >= 1:
            status = "Partial"
        else:
            status = "Missing"
        cov[element] = (status, n)
    return cov


def build_questions(cov):
    """Pick questions for Missing first, then Partial, in priority order."""
    priority = ["Job performer", "Main job", "Process", "Needs",
                "Circumstances", "Emotional/Social jobs", "Four Forces (switching)"]
    picked = []
    for status_want in ("Missing", "Partial"):
        for element in priority:
            status, _ = cov[element]
            if status == status_want:
                # don't ask Four Forces unless there's a switching signal
                if element == "Four Forces (switching)" and status == "Missing":
                    continue
                for q in QUESTIONS[element]:
                    picked.append((element, q))
                    break  # one question per element per pass
            if len(picked) >= 5:
                return picked
    return picked


def render_markdown(hits, cov, questions, max_quotes):
    out = []
    out.append("# JTBD Extraction Starter (auto-generated)\n")
    out.append("> Deterministic first pass from `extract_transcript.py`. "
               "A scaffold — verify against the transcript and apply judgment.\n")

    out.append("## Element coverage\n")
    out.append("| Element | Coverage | Signals found |")
    out.append("|---|---|---|")
    for element, (status, n) in cov.items():
        mark = {"Strong": "🟢", "Partial": "🟡", "Missing": "🔴"}[status]
        out.append(f"| {element} | {mark} {status} | {n} |")
    out.append("")

    labels = {
        "main_job_goal": "Candidate main-job / goal signals",
        "process_step": "Process / sequence signals",
        "pain_friction": "Pain & friction",
        "workaround": "Workarounds (= confirmed unmet needs)",
        "need_outcome": "Desired-outcome / wish signals",
        "emotional_social": "Emotional & social signals",
        "circumstance": "Circumstance signals",
        "switching_force": "Switching / Four-Forces signals",
        "performer_role": "Job-performer signals",
    }
    out.append("## Candidate signals by category\n")
    for cat, label in labels.items():
        rows = hits.get(cat, [])
        if not rows:
            continue
        out.append(f"### {label}  ({len(rows)})")
        for speaker, quote in rows[:max_quotes]:
            who = f"**{speaker}:** " if speaker else ""
            q = quote if len(quote) <= 220 else quote[:217] + "..."
            out.append(f"- {who}\"{q}\"")
        if len(rows) > max_quotes:
            out.append(f"- _...and {len(rows) - max_quotes} more_")
        out.append("")

    out.append("## Suggested follow-up questions (gap-driven)\n")
    if questions:
        for element, q in questions:
            out.append(f"- **[{element}]** {q}")
        out.append(f"- **[Any element, when answers go generic]** {CRITICAL_INCIDENT}")
    else:
        out.append("- Coverage looks strong across elements — proceed to drafting the "
                   "JTBD Analysis Report and validate the inferred items.")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="First-pass JTBD signal extractor for a transcript.")
    ap.add_argument("transcript", help="Path to transcript (.txt, .md, .vtt, .srt)")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    ap.add_argument("--max", type=int, default=6, help="Max quotes shown per category (default 6)")
    args = ap.parse_args()

    try:
        with open(args.transcript, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"ERROR: could not read {args.transcript}: {e}")

    if not text.strip():
        sys.exit("ERROR: transcript is empty.")

    turns = parse_transcript(text)
    hits = tag(turns)
    cov = coverage(hits)
    questions = build_questions(cov)

    if args.json:
        payload = {
            "coverage": {k: {"status": v[0], "signals": v[1]} for k, v in cov.items()},
            "signals": {cat: [{"speaker": s, "quote": q} for s, q in rows]
                        for cat, rows in hits.items()},
            "suggested_questions": [{"element": e, "question": q} for e, q in questions],
            "critical_incident_probe": CRITICAL_INCIDENT,
        }
        print(json.dumps(payload, indent=2))
    else:
        print(render_markdown(hits, cov, questions, args.max))


if __name__ == "__main__":
    main()
