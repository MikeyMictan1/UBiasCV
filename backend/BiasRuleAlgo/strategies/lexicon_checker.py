import re
from ..strategy_base import BiasStrategy, BiasStrategyOutput

LEADERSHIP_TERMS = {
    "assertive": 80,
    "aggressive": 90,
    "ambitious": 60,
    "dominant": 90,
    "confident": 60,
    "nurturing": 80,
    "compassionate": 70,
    "collaborative": 50,
    "supportive": 60,
    "abrasive": 90,
    "bossy": 90,
    "pushy": 80,
    "emotional": 65,
    "too soft": 65,
}

ACHIEVEMENT_TERMS = {
    "brilliant": 70,
    "genius": 80,
    "logical": 60,
    "hardworking": 40,
    "diligent": 40,
    "organized": 40,
    "organised": 40,
    "talented": 55,
    "smart": 50,
    "gifted": 65,
    "high potential": 55,
    "high-potential": 55,
    "natural leader": 85,
}

APPEARANCE_TERMS = {
    "beautiful": 90,
    "pretty": 90,
    "strong": 50,
    "powerful": 60,
    "attractive": 80,
    "young": 70,
    "feminine": 75,
    "masculine": 75,
    "soft-spoken": 70,
}

TERM_CATEGORIES = {
    "leadership": LEADERSHIP_TERMS,
    "achievement": ACHIEVEMENT_TERMS,
    "appearance": APPEARANCE_TERMS,
}

META_TERMS = (
    "the term ",
    "the word ",
    "phrase ",
    "used to describe",
    "often called",
    "so-called",
    "for example",
    "for instance",
    "such as",
)


class LexiconChecker(BiasStrategy):
    """
    LexiconChecker is a strategy that checks the presence of specific lexicons in a given text.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        feedback_lower = feedback_text.lower()
        evidence = []

        category_hits: dict[str, list[int]] = {name: [] for name in TERM_CATEGORIES}

        for category, words in TERM_CATEGORIES.items():
            for word, severity in words.items():
                match = self._find_match(feedback_lower, word)
                if match and not self._is_contextually_neutral(
                    feedback_lower, match.start(), word
                ):
                    category_hits[category].append(severity)
                    evidence.append(self._snippet(feedback_text, word))

        severities = [max(values) for values in category_hits.values() if values]

        score = self._compute_score(severities)
        return BiasStrategyOutput(
            strategy="LexiconChecker", score=score, evidence=evidence
        )

    def _find_match(self, text: str, word: str) -> re.Match[str] | None:
        pattern = r"\b" + re.escape(word) + r"\b"
        return re.search(pattern, text)

    def _is_contextually_neutral(
        self, text: str, idx: int, word: str, window: int = 36
    ) -> bool:
        preceding = text[max(0, idx - window) : idx]
        following = text[idx : min(len(text), idx + len(word) + window)]

        if re.search(
            rf'["\'“”‘’][^"\'“”‘’]{{0,40}}\b{re.escape(word)}\b[^"\'“”‘’]{{0,40}}["\'“”‘’]',
            text,
        ):
            return True

        if any(term in preceding for term in META_TERMS):
            return True

        if re.search(
            rf"\b(not|isn't|wasn't|never|no longer|hardly|barely|without)\b[^.?!\n]{{0,20}}\b{re.escape(word)}\b",
            preceding + following,
        ):
            return True

        return False

    def _snippet(self, text: str, word: str, window: int = 40) -> str:
        idx = text.lower().find(word)
        if idx == -1:
            return word
        start = max(0, idx - window)
        end = min(len(text), idx + len(word) + window)
        return f"...{text[start:end]}..."

    def _is_negated(self, text: str, idx: int, window: int = 24) -> bool:
        preceding = text[max(0, idx - window) : idx]
        return bool(re.search(r"\b(not|isn't|wasn't|never|no longer)\b", preceding))

    def _compute_score(self, severities: list) -> int:
        if not severities:
            return 0
        base = max(severities)
        category_bonus = min(12, (len(severities) - 1) * 3)
        repeated_hit_bonus = min(
            8, sum(1 for severity in severities if severity >= 80) * 2
        )
        return min(100, round(base + category_bonus + repeated_hit_bonus))
