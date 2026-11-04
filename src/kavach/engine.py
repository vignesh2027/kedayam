"""Combine rule findings and the classifier into one of three results.

* danger: any critical rule (weight 3), or rule weights adding up to 4+.
* caution: rule weights adding up to 2 or 3.
* none: nothing found. Kavach never says "safe".

The wording classifier is computed for English text and shown as a hint in
the details, but it does not change the result. On the hand-written holdout
set it flagged 16 of 35 ordinary bank alerts and service messages, because
the "ham" class in its public training data is personal chat, so every
business SMS looks unusual to it (see eval/HISTORY.md).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import classifier as clf
from .rules import RULES, Rule
from .textutil import Message, parse

DANGER_SCORE = 4
CAUTION_SCORE = 2
MAX_CHARS = 4000
# Below this share of Latin letters the classifier is out of its depth.
MIN_LATIN_SHARE = 0.6


@dataclass
class Finding:
    rule: Rule
    evidence: list[str]

    @property
    def id(self) -> str:
        return self.rule.id

    @property
    def weight(self) -> int:
        return self.rule.weight


@dataclass
class ClassifierResult:
    used: bool
    score: float | None = None
    flagged: bool = False


@dataclass
class Result:
    level: str
    score: int
    findings: list[Finding]
    tips: list[Finding]
    actions: list[str]
    classifier: ClassifierResult
    message: Message = field(repr=False, default=None)  # type: ignore[assignment]


def run_rules(m: Message) -> list[Finding]:
    out = []
    for r in RULES:
        ev = r.check(m)
        if ev:
            out.append(Finding(r, ev))
    return out


def analyse(text: str, sender: str = "", *, use_classifier: bool = True) -> Result:
    m = parse(text[:MAX_CHARS], sender)
    hits = run_rules(m)
    findings = sorted([f for f in hits if f.weight > 0], key=lambda f: -f.weight)
    tips = [f for f in hits if f.weight == 0]
    score = sum(f.weight for f in findings)
    critical = any(f.weight >= 3 for f in findings)

    cres = ClassifierResult(used=False)
    if use_classifier and clf.latin_share(m.raw) >= MIN_LATIN_SHARE:
        model = clf.load()
        if model is not None:
            s = model.score(m.raw)
            cres = ClassifierResult(used=True, score=s, flagged=s >= model.threshold)

    if critical or score >= DANGER_SCORE:
        level = "danger"
    elif score >= CAUTION_SCORE:
        level = "caution"
    else:
        level = "none"

    actions: list[str] = []
    # With no warning, tips are shown on their own under "Good to know".
    for f in findings:
        for a in f.rule.actions:
            if a not in actions:
                actions.append(a)
    if level != "none":
        if "tell_family" not in actions:
            actions.append("tell_family")
    return Result(level, score, findings, tips, actions, cres, m)
