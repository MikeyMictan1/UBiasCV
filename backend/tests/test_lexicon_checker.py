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
        feedback = "The reviewer described the candidate as aggressive and collaborative."

        result = strategy.analyse("", feedback)

        self.assertGreaterEqual(result.score, 90)
        self.assertTrue(any("aggressive" in item.lower() for item in result.evidence))
        self.assertTrue(any("collaborative" in item.lower() for item in result.evidence))


if __name__ == "__main__":
    unittest.main()
