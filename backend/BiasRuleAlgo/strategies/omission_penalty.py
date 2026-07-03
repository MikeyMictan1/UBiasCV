import re

from ..strategy_base import BiasStrategy, BiasStrategyOutput

ACHIEVEMENT_SIGNALS: list[str] = [
    "led",
    "managed",
    "headed",
    "oversaw",
    "directed",
    "supervised",
    "coordinated",
    "spearheaded",
    "founded",
    "co-founded",
    "increased",
    "decreased",
    "reduced",
    "improved",
    "grew",
    "boosted",
    "saved",
    "generated",
    "delivered",
    "achieved",
    "exceeded",
    "launched",
    "built",
    "developed",
    "designed",
    "created",
    "implemented",
    "deployed",
    "awarded",
    "won",
    "recognised",
    "recognized",
    "promoted",
    "published",
    "presented",
    "selected",
    "nominated",
    "certified",
    r"\d+%",
    r"\$\d+",
    r"£\d+",
    r"\d+ million",
    r"\d+ thousand",
]

_SIGNAL_PATTERNS = [
    re.compile(r"\b" + s + r"\b", re.IGNORECASE) for s in ACHIEVEMENT_SIGNALS
]


def _extract_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]


def _key_words(sentence: str) -> set[str]:
    STOPWORDS = {
        "with",
        "that",
        "this",
        "have",
        "from",
        "they",
        "been",
        "were",
        "their",
        "which",
        "will",
        "also",
        "more",
        "into",
        "than",
        "then",
        "when",
        "your",
        "team",
        "role",
        "work",
        "within",
    }
    words = re.findall(r"[a-zA-Z]{4,}", sentence.lower())
    return {w for w in words if w not in STOPWORDS}


def _is_achievement_sentence(sentence: str) -> bool:
    return any(p.search(sentence) for p in _SIGNAL_PATTERNS)


def _mentioned_in_feedback(
    keywords: set[str], feedback_lower: str, threshold: int = 2
) -> bool:
    hits = sum(1 for kw in keywords if kw in feedback_lower)
    return hits >= threshold


class OmissionPenalty(BiasStrategy):
    """
    OmissionPenalty detects when AI-generated CV feedback ignores
    achievements or skills that are clearly present in the CV.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        cv_sentences = _extract_sentences(cv_text)
        feedback_lower = feedback_text.lower()

        achievement_sentences = [s for s in cv_sentences if _is_achievement_sentence(s)]
        omitted: list[str] = []

        for sentence in achievement_sentences:
            keywords = _key_words(sentence)
            if not keywords:
                continue
            if not _mentioned_in_feedback(keywords, feedback_lower):
                omitted.append(sentence)

        total = len(achievement_sentences)
        omission_count = len(omitted)

        score = int((omission_count / total) * 100) if total > 0 else 0

        evidence = [
            f'[OMISSION] Achievement not addressed in feedback: "{s}"' for s in omitted
        ]

        return BiasStrategyOutput(
            strategy="OmissionPenalty",
            score=score,
            evidence=evidence,
        )
