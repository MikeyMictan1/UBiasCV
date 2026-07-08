import unittest

from BiasRuleAlgo.strategies.omission_penalty import OmissionPenalty


class OmissionPenaltyTests(unittest.TestCase):
    def test_scores_unaddressed_achievement_and_weights_metrics(self):
        strategy = OmissionPenalty()
        cv_text = (
            "Built a dashboard that reduced reporting time by 40%. "
            "Led a small team to improve onboarding across three regions."
        )
        feedback = (
<<<<<<< HEAD
            "Led team improve onboarding across regions. "
            "The dashboard was useful."
=======
            "Led team improve onboarding across regions. " "The dashboard was useful."
>>>>>>> 3128493874da1a22ebd2ff15ccfb0f491497dde7
        )

        result = strategy.analyse(cv_text, feedback)

        self.assertGreater(result.score, 0)
        self.assertTrue(
            any("built a dashboard" in item.lower() for item in result.evidence)
        )
        self.assertEqual(result.score, 66)

    def test_ignores_feedback_that_covers_the_achievement(self):
        strategy = OmissionPenalty()
        cv_text = "Launched a new intake process and improved onboarding speed."
<<<<<<< HEAD
        feedback = "The review noted the new intake process and onboarding speed improvements."
=======
        feedback = (
            "The review noted the new intake process and onboarding speed improvements."
        )

        result = strategy.analyse(cv_text, feedback)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])

    def test_recognizes_close_paraphrases_as_covered(self):
        strategy = OmissionPenalty()
        cv_text = "Built a dashboard that reduced reporting time by 40%."
        feedback = "The dashboard helped reduce reporting time by forty percent."
>>>>>>> 3128493874da1a22ebd2ff15ccfb0f491497dde7

        result = strategy.analyse(cv_text, feedback)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])


if __name__ == "__main__":
    unittest.main()
