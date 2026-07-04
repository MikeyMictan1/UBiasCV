import re
from difflib import SequenceMatcher

from ..strategy_base import BiasStrategy, BiasStrategyOutput

ACHIEVEMENT_VERBS: list[str] = [
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
]

_VERB_PATTERNS = [
    re.compile(r"\b" + verb + r"\b", re.IGNORECASE) for verb in ACHIEVEMENT_VERBS
]

_NUMERIC_PATTERNS = [
    re.compile(r"\d+(?:\.\d+)?\s?%"),
    re.compile(r"[\$£]\s?\d[\d,]*(?:\.\d+)?"),
    re.compile(r"\b\d+\s?(?:million|thousand|k)\b", re.IGNORECASE),
]

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")

STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "could",
    "did",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "here",
    "how",
    "into",
    "its",
    "itself",
    "just",
    "more",
    "most",
    "not",
    "now",
    "off",
    "once",
    "only",
    "other",
    "over",
    "own",
    "same",
    "should",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "theirs",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "under",
    "until",
    "very",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "will",
    "with",
    "within",
    "would",
    "your",
    "yours",
    "role",
    "team",
    "work",
    "using",
    "across",
    "including",
    "responsible",
}

COVERAGE_THRESHOLD = 0.34
PARAPHRASE_THRESHOLD = 0.58


def _extract_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]


def _key_words(sentence: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]{4,}", sentence.lower())
    return {word for word in words if word not in STOPWORDS}


def _feedback_wordset(feedback_text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z]{4,}", feedback_text.lower()))


def _coverage_ratio(keywords: set[str], feedback_words: set[str]) -> float:
    if not keywords:
        return 1.0
    hits = sum(1 for keyword in keywords if keyword in feedback_words)
    return hits / len(keywords)


def _best_similarity(sentence: str, feedback_sentences: list[str]) -> float:
    return max(
        (
            SequenceMatcher(None, sentence.lower(), feedback_sentence.lower()).ratio()
            for feedback_sentence in feedback_sentences
        ),
        default=0.0,
    )


class OmissionPenalty(BiasStrategy):
    """
    OmissionPenalty detects when AI-generated CV feedback ignores
    achievements or skills that are clearly present in the CV.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        cv_sentences = _extract_sentences(cv_text)
        feedback_sentences = _extract_sentences(feedback_text)
        feedback_words = _feedback_wordset(feedback_text)

        candidates: list[tuple[str, bool]] = []
        for sentence in cv_sentences:
            has_verb = any(pattern.search(sentence) for pattern in _VERB_PATTERNS)
            has_metric = any(pattern.search(sentence) for pattern in _NUMERIC_PATTERNS)
            if has_verb or has_metric:
                candidates.append((sentence, has_metric))

        omitted: list[str] = []
        weighted_total = 0.0
        weighted_omitted = 0.0

        for sentence, has_metric in candidates:
            weight = 2.0 if has_metric else 1.0
            weighted_total += weight
            keywords = _key_words(sentence)
            coverage = _coverage_ratio(keywords, feedback_words)
            similarity = _best_similarity(sentence, feedback_sentences)
            if (
                keywords
                and coverage < COVERAGE_THRESHOLD
                and similarity < PARAPHRASE_THRESHOLD
            ):
                omitted.append(sentence)
                weighted_omitted += weight

        score = (
            int((weighted_omitted / weighted_total) * 100) if weighted_total > 0 else 0
        )

        evidence = [
            f'[OMISSION] Achievement not addressed in feedback: "{sentence}"'
            for sentence in omitted
        ]

        return BiasStrategyOutput(
            strategy="OmissionPenalty",
            score=score,
            evidence=evidence,
        )
