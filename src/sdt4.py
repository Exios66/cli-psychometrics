# #!/usr/bin/env python3
“””
sd4_assessment.py

Interactive command-line administration of the Short Dark Tetrad (SD4).

Reference:
Paulhus, D. L., Buckels, E. E., Trapnell, P. D., & Jones, D. N. (2021).
Screening for dark personalities: The Short Dark Tetrad (SD4).
European Journal of Psychological Assessment, 37(3), 208-222.
https://doi.org/10.1027/1015-5759/a000602

Usage:
python sd4_assessment.py

Outputs (written to ./sd4_results/):
- sd4_responses_<timestamp>.csv   : Per-item responses with question text
- sd4_scores_<timestamp>.txt      : Subscale scores, means, interpretation
- sd4_assessment_<timestamp>.log  : Full session log

Notes:
- All 28 items are scored 1-5 (Strongly Disagree → Strongly Agree).
- There is NO reverse-scoring in the SD4; raw responses map directly to scores.
- Subscale score = sum of 7 items (range 7-35); mean = score / 7 (range 1-5).
- Euphemistic subscale labels per Paulhus et al. (2021):
Machiavellianism → “Crafty”
Narcissism       → “Special”
Psychopathy      → “Wild”
Sadism           → “Mean”
- This script is for RESEARCH / EDUCATIONAL purposes only.
It does NOT constitute a clinical assessment or psychological advice.
“””

import csv
import logging
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# —————————————————————————

# OUTPUT DIRECTORY

# —————————————————————————

OUTPUT_DIR = Path(“sd4_results”)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime(”%Y%m%d_%H%M%S”)

LOG_FILE   = OUTPUT_DIR / f”sd4_assessment_{TIMESTAMP}.log”
CSV_FILE   = OUTPUT_DIR / f”sd4_responses_{TIMESTAMP}.csv”
SCORE_FILE = OUTPUT_DIR / f”sd4_scores_{TIMESTAMP}.txt”

# —————————————————————————

# LOGGING SETUP

# —————————————————————————

def configure_logging() -> logging.Logger:
“”“Configure dual-sink logging: file (DEBUG) + console (INFO).”””
logger = logging.getLogger(“SD4”)
logger.setLevel(logging.DEBUG)

```
# File handler — verbose, timestamped
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh_fmt = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
fh.setFormatter(fh_fmt)

# Console handler — clean, INFO-only
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch_fmt = logging.Formatter("%(message)s")
ch.setFormatter(ch_fmt)

logger.addHandler(fh)
logger.addHandler(ch)
return logger
```

logger = configure_logging()

# —————————————————————————

# ASSESSMENT INSTRUMENT  — SD4 (Paulhus et al., 2021)

# —————————————————————————

# Subscale keys:

# M = Machiavellianism (items 1-7)

# N = Narcissism       (items 8-14)

# P = Psychopathy      (items 15-21)

# S = Sadism           (items 22-28)

# 

# All items scored 1 (Strongly Disagree) to 5 (Strongly Agree).

# No reverse-scoring is required.

ASSESSMENT = [
# ── Machiavellianism ────────────────────────────────────────────────────
{“id”:  1, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “It’s not wise to let people know your secrets.”},
{“id”:  2, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “Whatever it takes, you must get the important people on your side.”},
{“id”:  3, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “Avoid direct conflict with others because they may be useful in the future.”},
{“id”:  4, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “Keep a low profile if you want to get your way.”},
{“id”:  5, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “Manipulating the situation takes planning.”},
{“id”:  6, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “Flattery is a good way to get people on your side.”},
{“id”:  7, “subscale”: “M”, “label”: “Machiavellianism”,
“text”: “I love it when a tricky plan succeeds.”},

```
# ── Narcissism ───────────────────────────────────────────────────────────
{"id":  8, "subscale": "N", "label": "Narcissism",
 "text": "People see me as a natural leader."},
{"id":  9, "subscale": "N", "label": "Narcissism",
 "text": "I have a unique talent for persuading people."},
{"id": 10, "subscale": "N", "label": "Narcissism",
 "text": "Group activities tend to be dull without me."},
{"id": 11, "subscale": "N", "label": "Narcissism",
 "text": "I know that I am special because everyone keeps telling me so."},
{"id": 12, "subscale": "N", "label": "Narcissism",
 "text": "I have been compared to famous people."},
{"id": 13, "subscale": "N", "label": "Narcissism",
 "text": "I am a born leader."},
{"id": 14, "subscale": "N", "label": "Narcissism",
 "text": "I like to show off every now and then."},

# ── Psychopathy ──────────────────────────────────────────────────────────
{"id": 15, "subscale": "P", "label": "Psychopathy",
 "text": "I like to pick on losers."},
{"id": 16, "subscale": "P", "label": "Psychopathy",
 "text": "I'll say anything to get what I want."},
{"id": 17, "subscale": "P", "label": "Psychopathy",
 "text": "Revenge must be swift and nasty."},
{"id": 18, "subscale": "P", "label": "Psychopathy",
 "text": "People often say I'm out of control."},
{"id": 19, "subscale": "P", "label": "Psychopathy",
 "text": "It's true that I can be mean to others."},
{"id": 20, "subscale": "P", "label": "Psychopathy",
 "text": "Whatever it takes, I will get what I want."},
{"id": 21, "subscale": "P", "label": "Psychopathy",
 "text": "I tend to fight against authorities and their rules."},

# ── Sadism ───────────────────────────────────────────────────────────────
{"id": 22, "subscale": "S", "label": "Sadism",
 "text": "I enjoy watching people fight."},
{"id": 23, "subscale": "S", "label": "Sadism",
 "text": "Given the right situation, I could enjoy hurting people."},
{"id": 24, "subscale": "S", "label": "Sadism",
 "text": "I enjoy making cutting remarks to others."},
{"id": 25, "subscale": "S", "label": "Sadism",
 "text": "Some people deserve to suffer."},
{"id": 26, "subscale": "S", "label": "Sadism",
 "text": "I know how to hurt someone with words alone."},
{"id": 27, "subscale": "S", "label": "Sadism",
 "text": "I have fantasized about hurting people who have annoyed me."},
{"id": 28, "subscale": "S", "label": "Sadism",
 "text": "There is something satisfying about seeing someone's humiliation."},
```

]

NUM_QUESTIONS = len(ASSESSMENT)   # 28

# ── Response scale ────────────────────────────────────────────────────────────

SCALE = {
1: “Strongly Disagree”,
2: “Disagree”,
3: “Neutral”,
4: “Agree”,
5: “Strongly Agree”,
}

# ── Subscale metadata ─────────────────────────────────────────────────────────

SUBSCALES = {
“M”: {
“name”:       “Machiavellianism”,
“euphemism”:  “Crafty”,
“items”:      7,
“score_range”: (7, 35),
“description”: (
“Reflects a strategic, calculating orientation toward social life. “
“High scorers are manipulative, prioritize self-interest, and avoid “
“direct confrontation in favor of long-term planning and flattery.”
),
},
“N”: {
“name”:       “Narcissism”,
“euphemism”:  “Special”,
“items”:      7,
“score_range”: (7, 35),
“description”: (
“Reflects grandiose self-perception and a desire for admiration. “
“High scorers see themselves as uniquely talented leaders and actively “
“seek recognition and status from others.”
),
},
“P”: {
“name”:       “Psychopathy”,
“euphemism”:  “Wild”,
“items”:      7,
“score_range”: (7, 35),
“description”: (
“Reflects impulsivity, callousness, and antagonism. High scorers “
“act without regard for others, pursue goals aggressively, and show “
“little remorse for harmful behavior.”
),
},
“S”: {
“name”:       “Sadism”,
“euphemism”:  “Mean”,
“items”:      7,
“score_range”: (7, 35),
“description”: (
“Reflects pleasure derived from the pain, humiliation, or suffering “
“of others — whether through direct cruelty or vicarious observation. “
“High scorers may enjoy watching or inflicting emotional or physical pain.”
),
},
}

# ── Interpretation thresholds (mean score 1-5) ────────────────────────────────

# Based on published normative data direction (Paulhus et al., 2021, Table 4).

# Note: exact population norms are sample-dependent; these ranges reflect

# the broad low / moderate / elevated / high convention used in the literature.

INTERPRETATION_THRESHOLDS = [
(1.00, 1.99, “Low”,      “Your score falls well below average for this trait.”),
(2.00, 2.74, “Below Average”, “Your score is somewhat below the typical range.”),
(2.75, 3.24, “Average”,  “Your score is near the population midpoint for this trait.”),
(3.25, 3.99, “Above Average”, “Your score is somewhat elevated relative to the typical range.”),
(4.00, 5.00, “High”,     “Your score is notably elevated on this trait.”),
]

HELP_TEXT = textwrap.dedent(”””  
╔══════════════════════════════════════════════════════════════════╗
║                SD4  ASSESSMENT  —  INSTRUCTIONS                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  For each statement, indicate how much you AGREE or DISAGREE:   ║
║                                                                  ║
║    1 = Strongly Disagree                                         ║
║    2 = Disagree                                                  ║
║    3 = Neutral                                                   ║
║    4 = Agree                                                     ║
║    5 = Strongly Agree                                            ║
║                                                                  ║
║  There are no right or wrong answers. Respond honestly and       ║
║  spontaneously. After entering your answer you will be asked     ║
║  to confirm it before moving on.                                 ║
║                                                                  ║
║  Commands available at any prompt:                               ║
║    help  — show these instructions again                         ║
║    quit  — exit (progress is NOT saved)                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
“””)

# —————————————————————————

# UTILITIES

# —————————————————————————

def divider(char: str = “─”, width: int = 66) -> str:
return char * width

def wrap(text: str, width: int = 64, indent: str = “  “) -> str:
“”“Wrap long strings for clean terminal display.”””
return textwrap.fill(text, width=width, initial_indent=indent,
subsequent_indent=indent)

def interpret_mean(mean: float) -> tuple[str, str]:
“”“Return (level_label, description) for a subscale mean score.”””
for lo, hi, label, desc in INTERPRETATION_THRESHOLDS:
if lo <= mean <= hi:
return label, desc
return “Unknown”, “Score outside expected range.”

def percentile_bar(mean: float, width: int = 30) -> str:
“”“Render a simple ASCII progress bar for a 1-5 scale.”””
filled = int(round((mean - 1) / 4 * width))
filled = max(0, min(width, filled))
bar = “█” * filled + “░” * (width - filled)
return f”[{bar}]  {mean:.2f} / 5.00”

# —————————————————————————

# INPUT HELPERS

# —————————————————————————

def prompt_answer(item: dict, question_num: int) -> int:
“””
Present a single item and collect a confirmed 1-5 response.
Returns the integer response.  Handles ‘help’ and ‘quit’ gracefully.
“””
while True:
print(f”\n{divider()}”)
print(f”  Question {question_num} of {NUM_QUESTIONS}  “
f”[{item[‘label’]}]”)
print(divider())
print(wrap(f’”{item[“text”]}”’))
print()
print(”  1 = Strongly Disagree   2 = Disagree   3 = Neutral”)
print(”  4 = Agree               5 = Strongly Agree”)
print()

```
    raw = input("  Your answer (1-5): ").strip().lower()
    logger.debug("Item %d raw input: %r", item["id"], raw)

    if raw in ("quit", "q", "exit"):
        logger.info("User requested early exit at item %d.", item["id"])
        print("\n  Exiting assessment. Goodbye.\n")
        sys.exit(0)

    if raw in ("help", "h", "?"):
        print(HELP_TEXT)
        logger.debug("Help text displayed at item %d.", item["id"])
        continue

    if not raw.isdigit():
        print("\n  ⚠  Please enter a number between 1 and 5.")
        logger.debug("Non-numeric input at item %d: %r", item["id"], raw)
        continue

    answer = int(raw)
    if answer < 1 or answer > 5:
        print(f"\n  ⚠  {answer} is out of range. Please enter 1, 2, 3, 4, or 5.")
        logger.debug("Out-of-range input %d at item %d.", answer, item["id"])
        continue

    # Confirm answer
    print(f"\n  You selected: {answer} — {SCALE[answer]}")
    confirm = input("  Confirm? (Y to accept / any key to re-answer): ").strip().lower()

    if confirm in ("y", "yes"):
        logger.debug("Item %d confirmed: %d (%s)", item["id"], answer, SCALE[answer])
        return answer
    else:
        logger.debug("Item %d — answer rejected, re-prompting.", item["id"])
        print("  Re-answering this question...\n")
```

def prompt_respondent_info() -> dict:
“”“Optionally collect a participant identifier (never required).”””
print(f”\n{divider(‘═’)}”)
print(”  PARTICIPANT INFORMATION  (optional — press ENTER to skip)”)
print(divider(‘═’))
name = input(”  Name / ID: “).strip() or “Anonymous”
logger.info(“Participant identifier: %s”, name)
return {“participant”: name}

# —————————————————————————

# SCORING

# —————————————————————————

def compute_scores(responses: list[dict]) -> dict:
“””
Compute raw sum and mean for each subscale from collected responses.

```
Args:
    responses: list of dicts with keys 'subscale', 'response'.

Returns:
    dict keyed by subscale code ('M', 'N', 'P', 'S') with:
        sum  — raw subscale total (7-35)
        mean — subscale mean (1.00-5.00)
        level, interpretation — from thresholds
"""
totals = {k: 0 for k in SUBSCALES}
counts = {k: 0 for k in SUBSCALES}

for r in responses:
    key = r["subscale"]
    totals[key] += r["response"]
    counts[key] += 1

scores = {}
for key, meta in SUBSCALES.items():
    raw_sum = totals[key]
    n       = counts[key]
    mean    = raw_sum / n if n else 0.0
    level, interp = interpret_mean(mean)
    scores[key] = {
        "name":           meta["name"],
        "euphemism":      meta["euphemism"],
        "sum":            raw_sum,
        "n_items":        n,
        "mean":           round(mean, 3),
        "level":          level,
        "interpretation": interp,
        "description":    meta["description"],
    }
    logger.debug(
        "Subscale %s (%s): sum=%d, mean=%.3f, level=%s",
        key, meta["name"], raw_sum, mean, level,
    )

return scores
```

# —————————————————————————

# EXPORT FUNCTIONS

# —————————————————————————

def export_csv(responses: list[dict], participant: str) -> None:
“”“Write per-item responses to a CSV file.”””
fieldnames = [
“participant”, “item_id”, “subscale”, “subscale_name”,
“question_text”, “response”, “response_label”,
]
try:
with open(CSV_FILE, “w”, newline=””, encoding=“utf-8”) as f:
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()
for r in responses:
writer.writerow({
“participant”:     participant,
“item_id”:         r[“item_id”],
“subscale”:        r[“subscale”],
“subscale_name”:   r[“subscale_name”],
“question_text”:   r[“question_text”],
“response”:        r[“response”],
“response_label”:  r[“response_label”],
})
logger.info(“Responses exported → %s”, CSV_FILE)
print(f”\n  ✔  Item responses saved to: {CSV_FILE}”)
except OSError as exc:
logger.error(“CSV export failed: %s”, exc)
print(f”\n  ✖  Could not write CSV file: {exc}”)

def export_score_report(
scores: dict,
participant: str,
start_time: datetime,
end_time: datetime,
) -> None:
“”“Write a human-readable score interpretation report.”””
duration = end_time - start_time
minutes, seconds = divmod(int(duration.total_seconds()), 60)

```
lines = []
W = 66

def hr(char="─"):
    lines.append(char * W)

def add(text=""):
    lines.append(text)

hr("═")
add("  SHORT DARK TETRAD  (SD4)  —  SCORE REPORT")
hr("═")
add(f"  Participant : {participant}")
add(f"  Date/Time   : {start_time.strftime('%Y-%m-%d  %H:%M:%S')}")
add(f"  Duration    : {minutes}m {seconds:02d}s")
add(f"  Items       : {NUM_QUESTIONS} (7 per subscale × 4 subscales)")
hr()
add()
add("  Reference: Paulhus, Buckels, Trapnell & Jones (2021).")
add("  European Journal of Psychological Assessment, 37(3), 208-222.")
add()
add("  ⚠  FOR RESEARCH / EDUCATIONAL USE ONLY.  This output does  ")
add("     NOT constitute clinical assessment or psychological advice. ")
add()
hr("═")
add("  SUBSCALE SCORES")
hr("═")

for key in ("M", "N", "P", "S"):
    s = scores[key]
    add()
    add(f"  {s['name']}  ({s['euphemism']})")
    hr()
    add(f"  Raw sum  : {s['sum']} / 35   (7 items × max 5)")
    add(f"  Mean     : {percentile_bar(s['mean'])}")
    add(f"  Level    : {s['level']}")
    add(f"  Note     : {s['interpretation']}")
    add()
    for line in textwrap.wrap(s["description"], width=62,
                              initial_indent="  ", subsequent_indent="  "):
        add(line)
    add()
    hr()

# Summary table
add()
add("  SUMMARY TABLE")
hr()
add(f"  {'Subscale':<22}  {'Sum':>5}  {'Mean':>6}  {'Level':<15}")
hr("·")
for key in ("M", "N", "P", "S"):
    s = scores[key]
    add(f"  {s['name']:<22}  {s['sum']:>5}  {s['mean']:>6.2f}  {s['level']:<15}")
hr()
add()
add("  Score range per subscale: 7 (min) – 35 (max)")
add("  Mean  range per subscale: 1.00 – 5.00")
add()
hr("═")
add("  OUTPUT FILES")
hr()
add(f"  Responses  : {CSV_FILE}")
add(f"  This report: {SCORE_FILE}")
add(f"  Session log: {LOG_FILE}")
hr("═")

report_text = "\n".join(lines)

try:
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        f.write(report_text + "\n")
    logger.info("Score report exported → %s", SCORE_FILE)
    print(f"  ✔  Score report saved to:    {SCORE_FILE}")
except OSError as exc:
    logger.error("Score report export failed: %s", exc)
    print(f"\n  ✖  Could not write score report: {exc}")

# Also print to terminal
print()
print(report_text)
```

# —————————————————————————

# MAIN FLOW

# —————————————————————————

def run_assessment() -> None:
“”“Orchestrate the full SD4 administration.”””
logger.info(“SD4 Assessment session started. Output dir: %s”, OUTPUT_DIR)

```
# ── Welcome screen ──────────────────────────────────────────────────────
print()
print(divider("═"))
print("  SHORT DARK TETRAD  (SD4)  ASSESSMENT")
print(divider("═"))
print(f"  {NUM_QUESTIONS} items  ·  4 subscales  ·  ~5-8 minutes")
print()
print("  Paulhus, Buckels, Trapnell & Jones (2021)")
print("  European Journal of Psychological Assessment, 37(3), 208-222")
print()
print("  ⚠  For research / educational use only.")
print(divider("═"))
print()
print(HELP_TEXT)

# ── Participant info ────────────────────────────────────────────────────
meta = prompt_respondent_info()
participant = meta["participant"]

input(f"\n  Press ENTER to begin the {NUM_QUESTIONS}-item assessment…\n")

# ── Administer items ────────────────────────────────────────────────────
start_time = datetime.now()
responses: list[dict] = []

for idx, item in enumerate(ASSESSMENT, start=1):
    answer = prompt_answer(item, idx)
    responses.append({
        "item_id":        item["id"],
        "subscale":       item["subscale"],
        "subscale_name":  item["label"],
        "question_text":  item["text"],
        "response":       answer,
        "response_label": SCALE[answer],
    })
    logger.info(
        "Item %02d/%d  [%s]  →  %d (%s)",
        idx, NUM_QUESTIONS, item["label"], answer, SCALE[answer],
    )

end_time = datetime.now()
logger.info(
    "Assessment complete. Duration: %.1f seconds.",
    (end_time - start_time).total_seconds(),
)

# ── Score ───────────────────────────────────────────────────────────────
scores = compute_scores(responses)

# ── Export ──────────────────────────────────────────────────────────────
print(f"\n{divider('═')}")
print("  SAVING RESULTS…")
print(divider("═"))

export_csv(responses, participant)
export_score_report(scores, participant, start_time, end_time)

logger.info("Session complete. All outputs written to %s.", OUTPUT_DIR)

print()
print(divider("═"))
print("  Thank you for completing the SD4 Assessment.")
print(divider("═"))
print()
```

# —————————————————————————

# ENTRY POINT

# —————————————————————————

if **name** == “**main**”:
try:
run_assessment()
except KeyboardInterrupt:
print(”\n\n  Assessment interrupted by user (Ctrl+C). Goodbye.\n”)
logger.warning(“Assessment interrupted via KeyboardInterrupt.”)
sys.exit(1)
except Exception as exc:
logger.exception(“Unhandled exception: %s”, exc)
print(f”\n  ✖  An unexpected error occurred: {exc}”)
print(f”     See log file for details: {LOG_FILE}\n”)
sys.exit(2)
