import unittest

from BiasRuleAlgo.strategies.actionability_classifier import ActionabilityClassifier


class ActionabilityClassifierTests(unittest.TestCase):
    def test_scores_sentence_level_bias_risk(self):
        strategy = ActionabilityClassifier()
        feedback = (
            "Apply for junior data analyst roles at fintech firms. "
            "Consider negotiating a salary in the 60k to 70k range. "
            "You seem like a natural leader. "
            "Stay positive and keep going."
        )

        result = strategy.analyse("", feedback)

        self.assertEqual(result.score, 50)
        self.assertTrue(
            any(
                "specific career opportunity" in item.lower()
                for item in result.evidence
            )
        )
        self.assertTrue(
            any("salary advice" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any("personality critique" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any("vague encouragement" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any(
                "bias-signaled sentences: 2/4" in item.lower()
                for item in result.evidence
            )
        )

    def test_ignores_purely_actionable_feedback(self):
        strategy = ActionabilityClassifier()
        feedback = (
            "Apply for junior data analyst roles. "
            "Negotiate a salary in the 60k to 70k range."
        )

        result = strategy.analyse("", feedback)

        self.assertEqual(result.score, 0)
        self.assertTrue(
            any("actionable sentences: 2/2" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any(
                "bias-signaled sentences: 0/2" in item.lower()
                for item in result.evidence
            )
        )

    def test_full_bias_language_scores_high(self):
        strategy = ActionabilityClassifier()
        feedback = "You seem like a natural leader. " "Stay positive and keep going."

        result = strategy.analyse("", feedback)

        self.assertEqual(result.score, 100)
        self.assertTrue(
            any("personality critique" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any("vague encouragement" in item.lower() for item in result.evidence)
        )


if __name__ == "__main__":
    unittest.main()
