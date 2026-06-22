from ..strategy_base import BiasStrategy, BiasStrategyOutput


class LexiconChecker(BiasStrategy):
    """
    LexiconChecker is a strategy that checks the presence of specific lexicons in a given text.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        """
        Analyse the given text and return a BiasStrategyOutput object.

        Args:
            text (str): The text to be analysed.
        """
        # Placeholder implementation for lexicon checking
        score = 0  # Replace with actual scoring logic
        evidence = []  # Replace with actual evidence collection logic

        return BiasStrategyOutput(
            strategy="LexiconChecker", score=score, evidence=evidence
        )
