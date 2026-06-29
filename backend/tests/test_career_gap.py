import unittest

from BiasRuleAlgo.strategies.career_gap import CareerGapPenalty


class CareerGapPenaltyTests(unittest.TestCase):
    def test_flags_gap_bias(self):
        strategy = CareerGapPenalty()
        feedback = (
            "The candidate's maternity leave creates a gap that may count against "
            "their progression and suggests lower commitment. The review does not "
            "tie this concern to any objective job requirement."
        )

        result = strategy.analyse("", feedback)

        self.assertGreater(result.score, 0)
        self.assertTrue(
            any("maternity leave" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any("discount factor" in item.lower() for item in result.evidence)
        )

    def test_ignores_neutral_feedback(self):
        strategy = CareerGapPenalty()

        result = strategy.analyse(
            "",
            "Strong technical assessment with clear project evidence.",
        )

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])


if __name__ == "__main__":
    unittest.main()
