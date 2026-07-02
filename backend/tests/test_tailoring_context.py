import unittest

from BiasAI.ubiasai import build_tailoring_context


class TailoringContextTests(unittest.TestCase):
    def test_resolves_common_course_and_tool_aliases(self):
        context = build_tailoring_context(
            {
                "user": "Student",
                "course": "CS and Engineering",
                "ai_tool": "ChatGPT-4o",
                "gendered": "Unsure",
            }
        )

        self.assertEqual(context.domain, "STEM rubric")
        self.assertEqual(context.ai_tool, "ChatGPT")
        self.assertIn("generic praise", context.tool_profile.lower())

    def test_falls_back_to_general_profiles_for_unknown_values(self):
        context = build_tailoring_context(
            {
                "user": "Tool Developer",
                "course": "Interdisciplinary Studies",
                "ai_tool": "Local model",
                "gendered": "No",
            }
        )

        self.assertEqual(context.domain, "General studies")
        self.assertEqual(context.ai_tool, "Local model")
        self.assertIn("unknown or mixed tool", context.tool_profile.lower())


if __name__ == "__main__":
    unittest.main()
