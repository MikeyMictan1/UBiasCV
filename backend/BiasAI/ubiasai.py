# Business logic: build the prompt, call Claude, return a validated BiasReport.
# Uses structured outputs (messages.parse) so the response is guaranteed to
# match the BiasReport schema / claude_output_template.json.

from BiasAI.claude import client
from BiasAI.models import BiasReport
from BiasRuleAlgo.strategy_base import BiasStrategyOutput
from BiasRuleAlgo.rba import run_strategies

# Keep the model that's already configured for this project
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You detect bias in AI-generated feedback on university \
admissions documents (CVs).

You are given:
1. The applicant's CV.
2. AI-generated feedback on that CV, produced by a third-party AI tool.
3. Context from a short questionnaire.
4. Automated bias-detection rule checks, including a "hidden ceiling" flag \
that detects when strong qualifications (grades, internships, leadership) in \
the CV are paired with down-level role recommendations (support, junior, \
administrative) in the feedback.

Analyse the AI feedback (not the CV itself) for bias — gender, racial, \
socioeconomic, cultural, age, or other. Identify the specific phrases in the \
AI feedback that are biased, vague, or could lead to unfair treatment, and \
explain why each is a problem.

Treat career gaps, maternity leave, caregiving, parental leave, and flexible \
working as neutral unless the feedback ties the critique to objective, \
job-related evidence.

Pay special attention to the hidden ceiling flag: it points to cases where the \
AI system artificially caps a strong candidate's trajectory despite their \
objective achievements.

Set "score" from 0 to 100, where 0 means no detectable bias and 100 means \
severe, pervasive bias.

Write "next_steps" as concrete guidance for two audiences: students (how to \
interpret this feedback) and the tool's creators (what to review or fix).

Be concise throughout. Keep "summary" to 2-3 sentences. List only the most \
significant flagged phrases (at most 5), with a one-sentence reason for each — \
do not flag minor or borderline cases. Keep "next_steps" to 2-3 short \
sentences per audience. Prefer plain, direct wording over elaboration."""


def _format_strategy_results(strategy_results: list[BiasStrategyOutput]) -> str:
    if not strategy_results:
        return "None"

    lines = []
    for result in strategy_results:
        evidence = "; ".join(result.evidence) if result.evidence else "none"
        lines.append(
            f"- {result.strategy}: score={result.score:.0f}; evidence={evidence}"
        )
    return "\n".join(lines)


def generate_bias_report(
    cv_text: str, ai_feedback: str, questionnaire: dict
) -> BiasReport | None:
    strategy_results = run_strategies(cv_text, ai_feedback)
    user_content = f"""<questionnaire>
Who is using the tool: {questionnaire.get("user")}
AI tool that generated the feedback: {questionnaire.get("ai_tool")}
Course applied for: {questionnaire.get("course")}
CV contains gendered identifiers: {questionnaire.get("gendered")}
</questionnaire>

<rule_checks>
{_format_strategy_results(strategy_results)}
</rule_checks>

<cv>
{cv_text}
</cv>

<ai_feedback>
{ai_feedback}
</ai_feedback>

Analyse the AI feedback for bias and produce a structured report."""

    response = client.messages.parse(
        model=MODEL,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        output_format=BiasReport,
    )
    return response.parsed_output
