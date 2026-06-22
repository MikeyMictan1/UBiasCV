from ..strategy_base import BiasStrategy, BiasStrategyOutput

class CareerGapPenalty(BiasStrategy):
    """
    CareerGapPenalty is a strategy that evaluates the career gap penalty in a given text.
    """

    def analyse(self, text: str) -> BiasStrategyOutput:
        """
        Analyse the given text and return a BiasStrategyOutput object.

        Args:
            text (str): The text to be analysed.
        """
        # Placeholder implementation for career gap penalty evaluation
        score = 0  # Replace with actual scoring logic
        evidence = []  # Replace with actual evidence collection logic

        return BiasStrategyOutput(strategy="CareerGapPenalty", score=score, evidence=evidence)