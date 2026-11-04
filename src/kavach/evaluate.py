"""Evaluate Kavach and write eval/RESULTS.md.

Two test sets:

1. data/handwritten/holdout.jsonl: 80 hand-written messages (45 scam, 35
   legitimate) in English, Tamil, Hindi and mixed script, committed before
   the rules were written.
2. The 15% test split of the public SMS phishing dataset (never used for
   training or for choosing the classifier threshold).

"Flagged" means the result was "Warning" or "Be careful". A legitimate
message that is flagged is a false alarm.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from . import classifier as clf
from .engine import analyse

ROOT = Path(__file__).resolve().parents[2]
HOLDOUT = ROOT / "data" / "handwritten" / "holdout.jsonl"
OUT_DIR = ROOT / "eval"


def pr(tp: int, fp: int, fn: int) -> tuple[float, float]:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return round(p, 3), round(r, 3)


def score_set(items: list[tuple[str, str, int]], mode: str) -> dict:
    """items: (text, sender, label 1=scam). mode: rules, classifier, combined."""
    tp = fp = fn = tn = 0
    danger_tp = danger_fp = 0
    for text, sender, y in items:
        if mode == "classifier":
            model = clf.load()
            flagged = model.score(text) >= model.threshold
            danger = False
        else:
            r = analyse(text, sender, use_classifier=(mode == "combined"))
            flagged = r.level in ("danger", "caution")
            danger = r.level == "danger"
        if y and flagged:
            tp += 1
        elif y:
            fn += 1
        elif flagged:
            fp += 1
        else:
            tn += 1
        if danger and y:
            danger_tp += 1
        if danger and not y:
            danger_fp += 1
    p, r = pr(tp, fp, fn)
    return {
        "precision": p,
        "recall": r,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "false_alarm_rate": round(fp / (fp + tn), 3) if fp + tn else 0.0,
        "warning_recall": round(danger_tp / (tp + fn), 3) if tp + fn else 0.0,
        "warning_false_alarms": danger_fp,
    }


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rows = [json.loads(line) for line in HOLDOUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    hold = [(r["text"], r.get("sender", ""), 1 if r["label"] == "scam" else 0) for r in rows]

    results: dict = {"holdout": {}, "dataset_test": {}}
    for mode in ("rules", "classifier", "combined"):
        results["holdout"][mode] = score_set(hold, mode)

    # Per-message detail for the combined system.
    detail = []
    by_lang: dict[str, dict[str, int]] = defaultdict(lambda: {"scam": 0, "scam_flagged": 0, "legit": 0, "legit_flagged": 0})
    for r in rows:
        res = analyse(r["text"], r.get("sender", ""))
        flagged = res.level in ("danger", "caution")
        lang = r["lang"]
        if r["label"] == "scam":
            by_lang[lang]["scam"] += 1
            by_lang[lang]["scam_flagged"] += int(flagged)
        else:
            by_lang[lang]["legit"] += 1
            by_lang[lang]["legit_flagged"] += int(flagged)
        detail.append(
            {
                "id": r["id"],
                "label": r["label"],
                "lang": lang,
                "level": res.level,
                "rules": [f.id for f in res.findings],
                "classifier": None if res.classifier.score is None else round(res.classifier.score, 3),
            }
        )
    results["holdout_by_language"] = dict(by_lang)

    model = clf.load()
    _, _, test = clf.split(clf.load_dataset())
    ds = [(t, "", y) for t, y in test]
    for mode in ("rules", "classifier", "combined"):
        results["dataset_test"][mode] = score_set(ds, mode)
    results["classifier_threshold"] = model.threshold
    labels = clf.original_labels()
    for sub in ("smishing", "spam"):
        part = [(t, "", 1) for t, y in test if y == 1 and labels.get(clf._key(t)) == sub]
        flagged = sum(1 for t, _, _ in part if analyse(t, use_classifier=False).level != "none")
        results["dataset_test"][f"rules_recall_{sub}"] = {"flagged": flagged, "total": len(part)}

    (OUT_DIR / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    (OUT_DIR / "holdout_predictions.jsonl").write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in detail) + "\n", encoding="utf-8")
    write_markdown(results, detail)
    print((OUT_DIR / "RESULTS.md").read_text())


def _row(name: str, m: dict) -> str:
    return (
        f"| {name} | {m['precision']:.3f} | {m['recall']:.3f} | {m['warning_recall']:.3f} | "
        f"{m['false_alarm_rate']:.3f} | {m['tp']} | {m['fp']} | {m['fn']} | {m['tn']} |"
    )


def write_markdown(results: dict, detail: list[dict]) -> None:
    head = (
        "| System | Precision | Recall (flagged) | Recall (Warning only) | False alarm rate | TP | FP | FN | TN |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )
    lines = [
        "# Kavach evaluation results",
        "",
        "Generated by `uv run kavach-eval`. Do not edit by hand.",
        "",
        '"Flagged" means the result was "Warning: this looks like a scam" or "Be careful". '
        '"Recall (Warning only)" counts only the strongest result. For the classifier alone there is no Warning level, so that column is 0.',
        "",
        "## 1. Hand-written holdout set (80 messages: 45 scam, 35 legitimate)",
        "",
        "Written by the author from public RBI, NPCI, I4C and DoT advisories and committed before any rule existed (see git history). "
        "The same person then wrote the rules with these scam types in mind, so a perfect score here shows the rules cover the "
        "advisory patterns they were built for. It is not an unbiased estimate of real-world accuracy. "
        "The Classifier row shows the classifier deciding alone; in Kavach as shipped it is only a hint and does not change the result.",
        "",
        head,
    ]
    for mode in ("rules", "classifier", "combined"):
        lines.append(_row({"rules": "Rules only", "classifier": "Classifier only", "combined": "Kavach as shipped (rules decide)"}[mode], results["holdout"][mode]))
    lines += ["", "### By language (Kavach combined)", "", "| Language | Scam flagged | Legitimate flagged (false alarms) |", "| --- | --- | --- |"]
    for lang, v in sorted(results["holdout_by_language"].items()):
        lines.append(f"| {lang} | {v['scam_flagged']} / {v['scam']} | {v['legit_flagged']} / {v['legit']} |")
    misses = [d for d in detail if d["label"] == "scam" and d["level"] == "none"]
    alarms = [d for d in detail if d["label"] == "legit" and d["level"] != "none"]
    lines += ["", "### Misses (scam messages with no flag)", ""]
    lines += [f"* {d['id']} ({d['lang']}), classifier {d['classifier']}" for d in misses] or ["* none"]
    lines += ["", "### False alarms (legitimate messages that were flagged)", ""]
    lines += [f"* {d['id']} ({d['lang']}): {d['level']}, rules {', '.join(d['rules']) or 'none'}, classifier {d['classifier']}" for d in alarms] or ["* none"]
    lines += [
        "",
        f"## 2. Public dataset test split ({sum(results['dataset_test']['combined'][k] for k in ('tp', 'fp', 'fn', 'tn'))} messages)",
        "",
        "Mishra and Soni (2022) SMS Phishing Dataset, CC BY 4.0, deduplicated, 15% stratified test split with seed 42. "
        "Positive class is spam or smishing. The classifier was trained on the 70% train split and its threshold "
        f"({results['classifier_threshold']}) was chosen on the 15% validation split. "
        "The rules were not written from this dataset; most of its spam is marketing spam (ringtones, prize texts), "
        "which Kavach's rules are not designed to catch.",
        "",
        head,
    ]
    for mode in ("rules", "classifier", "combined"):
        lines.append(_row({"rules": "Rules only", "classifier": "Classifier only", "combined": "Kavach as shipped (rules decide)"}[mode], results["dataset_test"][mode]))
    sm, sp = results["dataset_test"]["rules_recall_smishing"], results["dataset_test"]["rules_recall_spam"]
    lines += [
        "",
        f"Rules recall by original label: smishing {sm['flagged']} / {sm['total']}, marketing spam {sp['flagged']} / {sp['total']}.",
        "",
        "The classifier scores well here because this split comes from the same source as its training data. "
        "On the hand-written Indian set it raised false alarms on ordinary bank and service messages, which is why it "
        "does not decide the result. See eval/HISTORY.md.",
    ]
    (OUT_DIR / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
