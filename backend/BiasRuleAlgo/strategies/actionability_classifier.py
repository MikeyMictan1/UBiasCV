from ..strategy_base import BiasStrategy, BiasStrategyOutput


class ActionabilityClassifier(BiasStrategy):
    """
    ActionabilityClassifier is a strategy that classifies the actionability of a given text.
    """

    def analyse(self, text: str) -> BiasStrategyOutput:
        """
        Analyse the given text and return a BiasStrategyOutput object.

        Args:
            text (str): The text to be analysed.
        """
        # Placeholder implementation for actionability classification
        score = 0  # Replace with actual scoring logic
        evidence = []  # Replace with actual evidence collection logic

        return BiasStrategyOutput(
            strategy="ActionabilityClassifier", score=score, evidence=evidence
        )
