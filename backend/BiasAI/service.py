# Business logic: build the prompt, call Claude, return a validated BiasReport.
# Uses structured outputs (messages.parse) so the response is guaranteed to
# match the BiasReport schema / claude_output_template.json.

from BiasAI.claude import client
from BiasAI.models import BiasReport

# Keep the model that's already configured for this project (see claude.py).
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You detect bias in AI-generated feedback on university \
admissions documents (CVs).

You are given:
1. The applicant's CV.
2. AI-generated feedback on that CV, produced by a third-party AI tool.
3. Context from a short questionnaire.

Analyse the AI feedback (not the CV itself) for bias — gender, racial, \
socioeconomic, cultural, age, or other. Identify the specific phrases in the \
AI feedback that are biased, vague, or could lead to unfair treatment, and \
explain why each is a problem.

Set "score" from 0 to 100, where 0 means no detectable bias and 100 means \
severe, pervasive bias.

Write "next_steps" as concrete guidance for two audiences: students (how to \
interpret this feedback) and the tool's creators (what to review or fix).

Be concise throughout. Keep "summary" to 2-3 sentences. List only the most \
significant flagged phrases (at most 5), with a one-sentence reason for each — \
do not flag minor or borderline cases. Keep "next_steps" to 2-3 short \
sentences per audience. Prefer plain, direct wording over elaboration."""


def generate_bias_report(
    cv_text: str, ai_feedback: str, questionnaire: dict
) -> BiasReport | None:
    user_content = f"""<questionnaire>
Who is using the tool: {questionnaire.get("user")}
AI tool that generated the feedback: {questionnaire.get("ai_tool")}
Course applied for: {questionnaire.get("course")}
CV contains gendered identifiers: {questionnaire.get("gendered")}
</questionnaire>

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
