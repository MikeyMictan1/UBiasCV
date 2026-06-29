"""
Integration test: verify hidden ceiling rule flows through the full pipeline.
"""
import unittest

from BiasRuleAlgo.rba import run_strategies


class HiddenCeilingIntegrationTest(unittest.TestCase):
    def test_hidden_ceiling_signal_in_strategy_results(self):
        """Verify the rule is called and produces output in the pipeline."""
        cv_text = (
            "Top grades, internships, leadership roles, and published research. "
            "High academic distinction."
        )
        feedback_text = (
            "The candidate should consider starting in a support or junior "
            "administrative role to gain experience before moving forward."
        )

        results = run_strategies(cv_text, feedback_text)

        # Find the hidden ceiling result
        hidden_ceiling_result = next(
            (r for r in results if r.strategy == "HiddenCeilingEngine"), None
        )

        self.assertIsNotNone(hidden_ceiling_result)
        self.assertGreater(hidden_ceiling_result.score, 0)
        self.assertTrue(len(hidden_ceiling_result.evidence) > 0)

        # Verify evidence contains both signals
        evidence_str = " ".join(hidden_ceiling_result.evidence).lower()
        self.assertIn("qualification", evidence_str)
        self.assertIn("down-level", evidence_str)

    def test_hidden_ceiling_does_not_flag_neutral_case(self):
        """Verify rule doesn't flag when feedback aligns with qualifications."""
        cv_text = "Excellent grades and strong internship experience."
        feedback_text = (
            "Strong candidate for advanced roles with leadership potential. "
            "Consider positions that leverage research and strategic thinking."
        )

        results = run_strategies(cv_text, feedback_text)

        hidden_ceiling_result = next(
            (r for r in results if r.strategy == "HiddenCeilingEngine"), None
        )

        self.assertIsNotNone(hidden_ceiling_result)
        self.assertEqual(hidden_ceiling_result.score, 0)
        self.assertEqual(hidden_ceiling_result.evidence, [])


if __name__ == "__main__":
    unittest.main()
