# Business logic: build the prompt, call Claude, return a validated BiasReport.
# Uses structured outputs (messages.parse) so the response is guaranteed to
# match the BiasReport schema / claude_output_template.json.

from BiasAI.claude import client
from BiasAI.models import BiasReport
from BiasRuleAlgo.strategy_base import BiasStrategyOutput
from BiasRuleAlgo.rba import run_strategies

# Keep the model that's already configured for this project
MODEL = "claude-haiku-4-5-20251001"


TOOL_PROFILES = {
    "vmock": (
        "Resume scoring / ranking platform",
        "Look for formulaic ranking language, overconfident scores, and advice that treats the CV as a checklist instead of evidence of capability. Prefer flags when the feedback seems to penalize strong achievements because they do not match a rigid template.",
    ),
    "chatgpt": (
        "General-purpose LLM",
        "Look for generic praise, vague self-improvement advice, and role recommendations that are not grounded in the CV. Be alert for polished but unsupported judgments.",
    ),
    "claude": (
        "General-purpose LLM",
        "Look for well-written but generic feedback that can still flatten a strong candidate into a lower-tier role. Check whether the model is over-indexing on caution or soft skills.",
    ),
    "gemini": (
        "General-purpose LLM",
        "Look for broad, confident recommendations that are not tied to evidence in the CV. Pay attention to any wording that sounds helpful but actually downlevels technical achievement.",
    ),
    "copilot": (
        "Productivity assistant",
        "Look for terse or automation-style feedback that can over-emphasize process and under-emphasize career evidence. Check whether the model is nudging the applicant toward support or administrative framing without proof.",
    ),
}


DOMAIN_PROFILES = {
    "art": (
        "Arts & Humanities",
        "Use language that checks for portfolio dismissal, creativity-capping, or personality-based framing rather than evidence-based critique.",
    ),
    "history": (
        "Arts & Humanities",
        "Use language that checks for portfolio dismissal, creativity-capping, or personality-based framing rather than evidence-based critique.",
    ),
    "liberal arts": (
        "Arts & Humanities",
        "Use language that checks for portfolio dismissal, creativity-capping, or personality-based framing rather than evidence-based critique.",
    ),
    "philosophy": (
        "Arts & Humanities",
        "Use language that checks for portfolio dismissal, creativity-capping, or personality-based framing rather than evidence-based critique.",
    ),
    "computer science": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "engineering": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "mathematics": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "physics": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "chemistry": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "biology": (
        "STEM",
        "Look for technical role-capping, junior-role steering, or advice that underweights systems work, algorithms, and engineering evidence.",
    ),
    "medicine": (
        "Health",
        "Look for care-stereotype framing, emotional assumptions, or unsupported claims about suitability for clinical or research pathways.",
    ),
    "law": (
        "Professional Studies",
        "Look for polish, tone, or fit language that is not tied to actual evidence of analytical ability, argumentation, or achievement.",
    ),
    "business": (
        "Professional Studies",
        "Look for polish, tone, or fit language that is not tied to actual evidence of analytical ability, argumentation, or achievement.",
    ),
    "psychology": (
        "Social Sciences",
        "Look for empathy stereotypes or nurturing language that is used to narrow technical or research potential.",
    ),
    "sociology": (
        "Social Sciences",
        "Look for empathy stereotypes or nurturing language that is used to narrow technical or research potential.",
    ),
    "economics": (
        "Social Sciences",
        "Look for vague leadership language or fit claims that obscure quantitative, analytical, or research evidence.",
    ),
    "political science": (
        "Social Sciences",
        "Look for vague leadership language or fit claims that obscure quantitative, analytical, or research evidence.",
    ),
    "education": (
        "Education",
        "Look for language that typecasts applicants into support, nurturing, or junior roles without evidence.",
    ),
}


def _normalize_key(value: str | None) -> str:
    return (value or "").strip().lower()


def _build_tool_profile(ai_tool: str | None) -> tuple[str, str]:
    key = _normalize_key(ai_tool)
    return TOOL_PROFILES.get(
        key,
        (
            "Unknown or mixed tool profile",
            "Use general bias heuristics and avoid claiming a vendor-specific failure pattern.",
        ),
    )


def _build_domain_profile(course: str | None) -> tuple[str, str]:
    key = _normalize_key(course)
    return DOMAIN_PROFILES.get(
        key,
        (
            "General studies",
            "Use broad, evidence-based bias checks and avoid assuming a narrow subject-specific profile.",
        ),
    )

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
    tool_profile_name, tool_guidance = _build_tool_profile(questionnaire.get("ai_tool"))
    domain_profile_name, domain_guidance = _build_domain_profile(questionnaire.get("course"))
    user_content = f"""<questionnaire>
Who is using the tool: {questionnaire.get("user")}
AI tool that generated the feedback: {questionnaire.get("ai_tool")}
AI tool profile: {tool_profile_name}
AI tool guidance: {tool_guidance}
Course applied for: {questionnaire.get("course")}
Domain profile: {domain_profile_name}
Domain guidance: {domain_guidance}
CV contains gendered identifiers: {questionnaire.get("gendered")}
</questionnaire>

<tool_specific_bias>
{tool_guidance}
</tool_specific_bias>

<domain_specific_bias>
{domain_guidance}
</domain_specific_bias>

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
