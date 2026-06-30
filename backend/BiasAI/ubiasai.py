# Business logic: build the prompt, call Claude, return a validated BiasReport.
# Uses structured outputs (messages.parse) so the response is guaranteed to
# match the BiasReport schema / claude_output_template.json.

from BiasAI.claude import client
from BiasAI.models import AnalysisReport, BiasReport, TailoringContext
from BiasRuleAlgo.strategy_base import BiasStrategyOutput

# Keep the model that's already configured for this project
MODEL = "claude-haiku-4-5-20251001"


DOMAIN_RUBRICS = {
    "art": (
        "Arts and design rubric",
        "Look for language that narrows creative potential, dismisses portfolio evidence, or shifts from critique to character judgment.",
    ),
    "history": (
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
    ),
    "liberal arts": (
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
    ),
    "computer science": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "engineering": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "medicine": (
        "Healthcare rubric",
        "Look for language that overweights care stereotypes, emotional framing, or unsupported assumptions about pressure or suitability.",
    ),
    "law": (
        "Professional studies rubric",
        "Look for language that overweights polish, tone, or social fit over evidence of analytical ability and achievement.",
    ),
    "business": (
        "Business rubric",
        "Look for generic leadership framing, hierarchy bias, or advice that narrows ambition without evidence.",
    ),
    "psychology": (
        "Social science rubric",
        "Look for language that confuses empathy stereotypes with evidence of capability or leadership.",
    ),
    "sociology": (
        "Social science rubric",
        "Look for language that confuses empathy stereotypes with evidence of capability or leadership.",
    ),
    "economics": (
        "Quantitative social science rubric",
        "Look for language that underplays analytical rigor, quantitative skill, or research potential.",
    ),
    "political science": (
        "Social science rubric",
        "Look for language that overweights confidence style or polish instead of reasoning and evidence.",
    ),
    "philosophy": (
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
    ),
    "mathematics": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "physics": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "chemistry": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "biology": (
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
    ),
    "education": (
        "Education rubric",
        "Look for language that typecasts applicants into support, nurturing, or junior roles without evidence.",
    ),
}


TOOL_SIGNATURES = {
    "vmock": (
        "Resume-scoring platform",
        "Check for formulaic, rank-driven feedback that overstates gaps or underweights context.",
    ),
    "chatgpt": (
        "General-purpose LLM",
        "Check for generic praise, vague self-improvement language, or ungrounded role recommendations.",
    ),
    "claude": (
        "General-purpose LLM",
        "Check for polished but generic feedback that may still encode subtle role-capping assumptions.",
    ),
    "gemini": (
        "General-purpose LLM",
        "Check for broad recommendations that sound confident but are not tied to evidence in the CV.",
    ),
    "copilot": (
        "Productivity assistant",
        "Check for terse, automation-style advice that can blur critique with premature role narrowing.",
    ),
}


def _normalize_key(value: str | None) -> str:
    return (value or "").strip().lower()


def build_tailoring_context(questionnaire: dict) -> TailoringContext:
    course = _normalize_key(questionnaire.get("course"))
    ai_tool = _normalize_key(questionnaire.get("ai_tool"))

    domain, domain_rubric = DOMAIN_RUBRICS.get(
        course,
        (
            "General studies rubric",
            "Use a broad review for mixed or uncategorized study areas and avoid assuming specialized expectations.",
        ),
    )
    tool_profile, _tool_signature = TOOL_SIGNATURES.get(
        ai_tool,
        (
            "Unknown or mixed tool profile",
            "Use general bias heuristics and avoid claiming a vendor-specific failure pattern.",
        ),
    )

    return TailoringContext(
        user_role=questionnaire.get("user") or "Unknown",
        ai_tool=questionnaire.get("ai_tool") or "Unknown",
        domain=domain,
        domain_rubric=domain_rubric,
        tool_profile=tool_profile,
        gendered_language=questionnaire.get("gendered") or "Unsure",
        review_depth="standard",
    )


def _role_tailoring(tailoring_context: TailoringContext) -> str:
    if tailoring_context.user_role == "Tool Developer":
        return """Developer mode:
- Write for someone improving the system.
- Emphasize bias patterns, failure modes, and how the tool should change.
- Prefer concrete implementation guidance over user-facing advice."""

    return """Student mode:
- Write for someone reading the feedback about their own CV.
- Keep the explanation plain and reassuring without minimizing the issue.
- Focus on what to trust, what to question, and what to do next."""

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

Write "next_steps" as concrete guidance for only the selected role.
Do not include advice for the other role.

Make the final report clearly role-aware:
- In student mode, "summary" should explain the finding in plain language and
    "next_steps" should focus on how to read the feedback safely and what to
    ignore or question.
- In developer mode, "summary" should emphasize the bias pattern and why it is
    likely happening, and "next_steps" should focus on implementation fixes,
    prompt changes, and rule adjustments.
- Keep the two modes distinct in wording, not just in tone.
- Keep "next_steps" to one audience only: students in student mode, tool
    creators in developer mode.

Use the tailoring object below as the source of truth for how to frame the
report. It is provided in the user message and already includes the selected
role, domain, tool profile, and sensitivity flag.

Use the AI tool name and the course/area of study as context for what kinds of
phrasing are likely to be misleading or overly restrictive. If the CV is marked
as containing gendered identifiers or language, treat that as a signal to look
carefully for gender-coded wording without making assumptions about the user's
identity.

Be concise throughout. Keep "summary" to 2-3 sentences. List only the most \
significant flagged phrases (at most 5), with a one-sentence reason for each — \
do not flag minor or borderline cases. Keep "next_steps" to 2-3 short \
sentences total, for the selected role only. Prefer plain, direct wording over \
elaboration.

Be evidence-backed and specific:
- For every item in "flagged_phrases", include an "evidence_snippet" copied
    from the AI feedback that triggered the flag.
- Set "confidence" to one of: low, medium, high.
- Prefer "high" only when the phrase is clearly biased or clearly down-leveling.
- If the evidence is weak or ambiguous, either lower the confidence or do not
    flag it.
"""


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
    cv_text: str,
    ai_feedback: str,
    strategy_results: list[BiasStrategyOutput],
    tailoring_context: TailoringContext,
) -> BiasReport | None:
    user_content = f"""<tailoring_context>
{tailoring_context.model_dump_json(indent=2)}
</tailoring_context>

<tailoring_guidance>
{_role_tailoring(tailoring_context)}

The report itself must reflect the selected role in the wording of the summary
and next_steps, not only in the introductory note.

Use the tailoring object to select the most relevant rubric and vocabulary. If
the AI tool or domain is unknown, use the general rubric and avoid inventing
vendor-specific or discipline-specific assumptions.
</tailoring_guidance>

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
        output_format=AnalysisReport,
    )
    return BiasReport(**response.parsed_output.model_dump(), tailoring_context=tailoring_context)
