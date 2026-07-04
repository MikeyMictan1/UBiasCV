import re
from ..strategy_base import BiasStrategy, BiasStrategyOutput


class LexiconChecker(BiasStrategy):
    """
    LexiconChecker is a strategy that checks the presence of specific lexicons in a given text.
    """

    FLAGGED_WORDS_LEADERSHIP = {
        "assertive": 80,
        "aggressive": 90,
        "ambitious": 60,
        "dominant": 90,
        "confident": 60,
        "nurturing": 80,
        "compassionate": 70,
        "collaborative": 50,
        "supportive": 60,
    }
    FLAGGED_WORDS_ACHIEVEMENT = {
        "brilliant": 70,
        "genius": 80,
        "logical": 60,
        "hardworking": 40,
        "diligent": 40,
        "organized": 40,
    }
    FLAGGED_WORDS_APPEARANCE = {
        "beautiful": 90,
        "pretty": 90,
        "strong": 50,
        "powerful": 60,
        "attractive": 80,
    }

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        feedback_lower = feedback_text.lower()
        evidence = []
        severities = []

        all_words = {
            **self.FLAGGED_WORDS_LEADERSHIP,
            **self.FLAGGED_WORDS_ACHIEVEMENT,
            **self.FLAGGED_WORDS_APPEARANCE,
        }

        for word, severity in all_words.items():
            pattern = r"\b" + re.escape(word) + r"\b"
            match = re.search(pattern, feedback_lower)
            if match and not self._is_negated(feedback_lower, match.start()):
                severities.append(severity)
                evidence.append(self._snippet(feedback_text, word))

        score = self._compute_score(severities)
        return BiasStrategyOutput(
            strategy="LexiconChecker", score=score, evidence=evidence
        )

    def _snippet(self, text: str, word: str, window: int = 40) -> str:
        idx = text.lower().find(word)
        if idx == -1:
            return word
        start = max(0, idx - window)
        end = min(len(text), idx + len(word) + window)
        return f"...{text[start:end]}..."

    def _is_negated(self, text: str, idx: int, window: int = 24) -> bool:
        preceding = text[max(0, idx - window):idx]
        return bool(re.search(r"\b(not|isn't|wasn't|never|no longer)\b", preceding))

    def _compute_score(self, severities: list) -> int:
        if not severities:
            return 0
        base = max(severities)
        bonus = min(15, (len(severities) - 1) * 4)  # extra flagged terms only ever push the score up
        return min(100, round(base + bonus))
