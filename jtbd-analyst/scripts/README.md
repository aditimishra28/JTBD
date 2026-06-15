# scripts/

Helper tools for the JTBD Analyst skill.

## extract_transcript.py

First-pass JTBD signal extractor for an uploaded customer conversation. Reads a
transcript (`.txt`, `.md`, `.vtt`, `.srt`), surfaces candidate signals by category
(main job, process, pain, workarounds, needs, emotional/social, circumstances,
switching, performer role), scores which of the five elements have evidence, and
drafts gap-driven follow-up questions. Deterministic scaffold — the analyst still
reads the transcript and applies judgment.

```bash
python3 extract_transcript.py call.txt            # Markdown extraction starter
python3 extract_transcript.py call.vtt --json     # machine-readable
python3 extract_transcript.py notes.md --max 8    # cap quotes shown per category
```

Pure standard library — no dependencies. See `../references/transcript-extraction.md`.

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
