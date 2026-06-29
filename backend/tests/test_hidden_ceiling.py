import unittest

from BiasRuleAlgo.strategies.hidden_ceiling import HiddenCeilingEngine



class HiddenCeilingEngineTests(unittest.TestCase):
    def test_flags_hidden_ceiling_bias(self):
        strategy = HiddenCeilingEngine()
        cv_text = (
            "Top grades, two internships, research experience, and student leadership "
            "roles suggest a high-achieving candidate."
        )
        feedback = (
            "Despite this strong background, the applicant should consider an entry-level "
            "support role or junior coordinator position before aiming for leadership."
        )

        result = strategy.analyse(cv_text, feedback)

        self.assertGreater(result.score, 0)
        self.assertTrue(
            any("cv qualification signals" in item.lower() for item in result.evidence)
        )
        self.assertTrue(
            any("down-level role language" in item.lower() for item in result.evidence)
        )

    def test_ignores_neutral_feedback(self):
        strategy = HiddenCeilingEngine()
        cv_text = "Excellent grades and internships."

        result = strategy.analyse(
            cv_text,
            "Strong candidate for advanced research and leadership opportunities.",
        )

        self.assertEqual(result.score, 0)
        self.assertEqual(result.evidence, [])


if __name__ == "__main__":
    unittest.main()
