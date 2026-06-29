import re

from ..strategy_base import BiasStrategy, BiasStrategyOutput

QUALIFICATION_TERMS = {
    "high grades",
    "top grades",
    "excellent grades",
    "strong grades",
    "honours",
    "honors",
    "awards",
    "scholarship",
    "internship",
    "internships",
    "research",
    "publication",
    "publications",
    "leadership",
    "captain",
    "president",
    "founder",
    "projects",
    "project outcomes",
    "academic excellence",
    "distinction",
}

DOWNLEVEL_ROLE_TERMS = {
    "support role",
    "support roles",
    "support position",
    "assistant",
    "administrative",
    "clerical",
    "junior",
    "entry level",
    "entry-level",
    "non-leadership",
    "non leadership",
    "back office",
    "back-office",
    "coordinator",
    "technician",
    "operational support",
    "lower tier",
    "lower-tier",
    "routine role",
}

UPWARD_ROLE_TERMS = {
    "lead",
    "leadership",
    "manager",
    "senior",
    "advanced",
    "research",
    "strategy",
    "ownership",
    "initiative",
    "impact",
}

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")


def _contains_any(text: str, terms: set[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


class HiddenCeilingEngine(BiasStrategy):
    """
    HiddenCeilingEngine flags feedback that caps a strong candidate at lower-tier roles.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        """
        Detect a mismatch between objective achievement signals in the CV and
        reduced-status role recommendations in the feedback.
        """
        qualification_hits = _contains_any(cv_text, QUALIFICATION_TERMS)
        feedback_downlevel_hits = _contains_any(feedback_text, DOWNLEVEL_ROLE_TERMS)
        feedback_upward_hits = _contains_any(feedback_text, UPWARD_ROLE_TERMS)

        if not qualification_hits or not feedback_downlevel_hits:
            return BiasStrategyOutput(
                strategy="HiddenCeilingEngine", score=0, evidence=[]
            )

        sentences = _sentences(feedback_text)
        matched_sentences = [
            sentence
            for sentence in sentences
            if _contains_any(sentence, DOWNLEVEL_ROLE_TERMS)
        ]

        base_score = 35.0
        base_score += min(25.0, len(qualification_hits) * 6.0)
        base_score += min(20.0, len(feedback_downlevel_hits) * 8.0)
        base_score += 10.0 if len(qualification_hits) >= 2 else 0.0
        base_score += 10.0 if len(feedback_downlevel_hits) >= 2 else 0.0
        base_score += 8.0 if not feedback_upward_hits else -8.0

        score = _clamp(base_score)

        evidence = []
        if matched_sentences:
            evidence.extend(matched_sentences[:3])
        evidence.append(
            "CV qualification signals: "
            + (
                ", ".join(sorted(set(qualification_hits)))
                if qualification_hits
                else "none"
            )
        )
        evidence.append(
            "Down-level role language: "
            + (
                ", ".join(sorted(set(feedback_downlevel_hits)))
                if feedback_downlevel_hits
                else "none"
            )
        )
        evidence.append(
            "Upward role language present: "
            + (
                ", ".join(sorted(set(feedback_upward_hits)))
                if feedback_upward_hits
                else "none"
            )
        )

        return BiasStrategyOutput(
            strategy="HiddenCeilingEngine", score=score, evidence=evidence
        )
