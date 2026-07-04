import unittest

from BiasRuleAlgo.strategies.lexicon_checker import LexiconChecker


class LexiconCheckerTests(unittest.TestCase):
    def test_ignores_negated_flagged_language(self):
        strategy = LexiconChecker()
        feedback = "The candidate is not aggressive and is never dominant in meetings."

        result = strategy.analyse("", feedback)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])

    def test_uses_highest_severity_as_the_score_floor(self):
        strategy = LexiconChecker()
        feedback = (
            "The reviewer described the candidate as aggressive and collaborative."
        )

        result = strategy.analyse("", feedback)

        self.assertGreaterEqual(result.score, 90)
        self.assertTrue(any("aggressive" in item.lower() for item in result.evidence))
        self.assertTrue(
            any("collaborative" in item.lower() for item in result.evidence)
        )

    def test_scores_multiple_bias_categories_without_diluting_the_severe_signal(self):
        strategy = LexiconChecker()
        feedback = "The candidate is aggressive, brilliant, and attractive."

        result = strategy.analyse("", feedback)

        self.assertGreaterEqual(result.score, 100 if result.score == 100 else 96)
        self.assertTrue(any("aggressive" in item.lower() for item in result.evidence))
        self.assertTrue(any("brilliant" in item.lower() for item in result.evidence))
        self.assertTrue(any("attractive" in item.lower() for item in result.evidence))

    def test_ignores_meta_discussion_of_a_flagged_term(self):
        strategy = LexiconChecker()
        feedback = "The term aggressive is often used unfairly in performance reviews."

        result = strategy.analyse("", feedback)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])


if __name__ == "__main__":
    unittest.main()
