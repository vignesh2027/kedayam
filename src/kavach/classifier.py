"""A small text classifier trained on the public SMS phishing dataset.

It is a secondary signal only. The engine lets it raise "no known pattern"
to "be careful", never lower a rule-based warning, and it is skipped for
text that is mostly not in Latin script, because the training data is
almost all English.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "smishing" / "Dataset_5971.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "classifier.joblib"
META_PATH = MODEL_DIR / "classifier.json"
SEED = 42
# Precision we want on validation before the classifier may raise a caution
# on its own. High, because a false alarm teaches people to ignore Kavach.
TARGET_PRECISION = 0.95


def _key(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def load_dataset(path: Path = DATA) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            label = r["LABEL"].strip().lower()
            text = r["TEXT"].strip()
            if not text or label not in {"ham", "spam", "smishing"}:
                continue
            k = _key(text)
            if k in seen:
                continue
            seen.add(k)
            rows.append((text, 0 if label == "ham" else 1))
    return rows


def original_labels(path: Path = DATA) -> dict[str, str]:
    """Map normalised text to its original label (ham, spam or smishing)."""
    out: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(_key(r["TEXT"].strip()), r["LABEL"].strip().lower())
    return out


def split(rows: list[tuple[str, int]], seed: int = SEED):
    """Stratified 70/15/15 split."""
    rnd = random.Random(seed)
    parts: dict[str, list] = {"train": [], "val": [], "test": []}
    for cls in (0, 1):
        items = [r for r in rows if r[1] == cls]
        rnd.shuffle(items)
        n = len(items)
        a, b = int(n * 0.70), int(n * 0.85)
        parts["train"] += items[:a]
        parts["val"] += items[a:b]
        parts["test"] += items[b:]
    for v in parts.values():
        rnd.shuffle(v)
    return parts["train"], parts["val"], parts["test"]


def build() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True, lowercase=True)),
            ("lr", LogisticRegression(C=8.0, class_weight="balanced", max_iter=2000, random_state=SEED)),
        ]
    )


def metrics(y_true: list[int], probs: list[float], threshold: float) -> dict[str, float]:
    pred = [1 if p >= threshold else 0 for p in probs]
    p, r, f, _ = precision_recall_fscore_support(y_true, pred, average="binary", zero_division=0)
    tp = sum(1 for a, b in zip(y_true, pred) if a == b == 1)
    fp = sum(1 for a, b in zip(y_true, pred) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y_true, pred) if a == 1 and b == 0)
    tn = sum(1 for a, b in zip(y_true, pred) if a == b == 0)
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4), "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def pick_threshold(y: list[int], probs: list[float]) -> float:
    """Lowest threshold whose validation precision reaches the target."""
    for th in [x / 100 for x in range(50, 100)]:
        if metrics(y, probs, th)["precision"] >= TARGET_PRECISION:
            return th
    return 0.99


def train(verbose: bool = True) -> dict:
    rows = load_dataset()
    tr, va, te = split(rows)
    model = build()
    model.fit([t for t, _ in tr], [y for _, y in tr])
    vprobs = model.predict_proba([t for t, _ in va])[:, 1].tolist()
    th = pick_threshold([y for _, y in va], vprobs)
    tprobs = model.predict_proba([t for t, _ in te])[:, 1].tolist()
    meta = {
        "dataset": "Mishra and Soni (2022), SMS Phishing Dataset, Mendeley Data, doi:10.17632/f45bkkt8pr.1, CC BY 4.0",
        "dataset_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "rows_after_dedup": len(rows),
        "split": {"train": len(tr), "val": len(va), "test": len(te), "seed": SEED},
        "positive_class": "spam or smishing",
        "threshold": th,
        "target_precision_on_val": TARGET_PRECISION,
        "val": metrics([y for _, y in va], vprobs, th),
        "test": metrics([y for _, y in te], tprobs, th),
        "test_at_0.5": metrics([y for _, y in te], tprobs, 0.5),
    }
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    META_PATH.write_text(json.dumps(meta, indent=2) + "\n")
    if verbose:
        print(json.dumps(meta, indent=2))
    return meta


@dataclass
class Classifier:
    model: Pipeline
    threshold: float

    def score(self, text: str) -> float:
        return float(self.model.predict_proba([text])[0, 1])


_cached: Classifier | None = None


def latin_share(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isascii()) / len(letters)


def load(auto_train: bool = True) -> Classifier | None:
    global _cached
    if _cached is not None:
        return _cached
    if not MODEL_PATH.exists() or not META_PATH.exists():
        if not auto_train:
            return None
        print("Kavach: training the wording classifier for the first time (a few seconds)...", file=sys.stderr)
        train(verbose=False)
    meta = json.loads(META_PATH.read_text())
    _cached = Classifier(joblib.load(MODEL_PATH), float(meta["threshold"]))
    return _cached


def main() -> None:
    train(verbose=True)


if __name__ == "__main__":
    main()
