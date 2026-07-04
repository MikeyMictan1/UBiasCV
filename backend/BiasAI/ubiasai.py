# Business logic: build the prompt, call Claude, return a validated BiasReport.
# Uses structured outputs (messages.parse) so the response is guaranteed to
# match the BiasReport schema / claude_output_template.json.

import re

from BiasAI.claude import client
from BiasAI.models import AnalysisReport, BiasReport, TailoringContext
from BiasRuleAlgo.strategy_base import BiasStrategyOutput
from BiasRuleAlgo.rba import run_strategies

# Keep the model that's already configured for this project
MODEL = "claude-haiku-4-5-20251001"


DOMAIN_PROFILES = [
    (
        "art",
        "Arts and design rubric",
        "Look for language that narrows creative potential, dismisses portfolio evidence, or shifts from critique to character judgment.",
        ("art", "arts", "design", "fine art", "graphic design", "visual arts"),
    ),
    (
        "history",
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
        ("history", "historical studies", "art history"),
    ),
    (
        "liberal arts",
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
        ("liberal arts", "liberal studies", "humanities", "arts and humanities"),
    ),
    (
        "computer science",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        (
            "computer science",
            "cs",
            "comp sci",
            "computing",
            "software engineering",
            "computer engineering",
            "information technology",
            "informatics",
        ),
    ),
    (
        "engineering",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        (
            "engineering",
            "mechanical engineering",
            "electrical engineering",
            "civil engineering",
            "chemical engineering",
            "industrial engineering",
        ),
    ),
    (
        "medicine",
        "Healthcare rubric",
        "Look for language that overweights care stereotypes, emotional framing, or unsupported assumptions about pressure or suitability.",
        ("medicine", "medical", "health", "healthcare", "health sciences", "nursing"),
    ),
    (
        "law",
        "Professional studies rubric",
        "Look for language that overweights polish, tone, or social fit over evidence of analytical ability and achievement.",
        ("law", "legal studies", "jurisprudence"),
    ),
    (
        "business",
        "Business rubric",
        "Look for generic leadership framing, hierarchy bias, or advice that narrows ambition without evidence.",
        (
            "business",
            "management",
            "commerce",
            "finance",
            "accounting",
            "marketing",
            "mba",
        ),
    ),
    (
        "psychology",
        "Social science rubric",
        "Look for language that confuses empathy stereotypes with evidence of capability or leadership.",
        ("psychology", "psycho"),
    ),
    (
        "sociology",
        "Social science rubric",
        "Look for language that confuses empathy stereotypes with evidence of capability or leadership.",
        ("sociology", "social work"),
    ),
    (
        "economics",
        "Quantitative social science rubric",
        "Look for language that underplays analytical rigor, quantitative skill, or research potential.",
        ("economics", "econ", "econometrics"),
    ),
    (
        "political science",
        "Social science rubric",
        "Look for language that overweights confidence style or polish instead of reasoning and evidence.",
        ("political science", "politics", "poli sci", "international relations"),
    ),
    (
        "philosophy",
        "Humanities rubric",
        "Look for vague professionalism language, stereotype-driven feedback, or advice that ignores evidence-based scholarly strengths.",
        ("philosophy", "ethics", "logic"),
    ),
    (
        "mathematics",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        ("mathematics", "math", "maths", "statistics", "applied mathematics"),
    ),
    (
        "physics",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        ("physics", "physical sciences"),
    ),
    (
        "chemistry",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        ("chemistry", "chemical sciences"),
    ),
    (
        "biology",
        "STEM rubric",
        "Look for role-capping language that undercuts technical achievement, leadership, or research potential.",
        ("biology", "biological sciences", "life sciences"),
    ),
    (
        "education",
        "Education rubric",
        "Look for language that typecasts applicants into support, nurturing, or junior roles without evidence.",
        ("education", "teaching", "teacher education", "pedagogy"),
    ),
]


TOOL_PROFILES = [
    (
        "vmock",
        "VMock",
        "Resume-scoring platform",
        "Check for formulaic, rank-driven feedback that overstates gaps or underweights context.",
        ("vmock", "v mock", "v-mock"),
    ),
    (
        "chatgpt",
        "ChatGPT",
        "General-purpose LLM",
        "Check for generic praise, vague self-improvement language, or ungrounded role recommendations.",
        ("chatgpt", "chat gpt", "openai", "gpt 4", "gpt4", "gpt 4o", "gpt-4", "gpt-4o"),
    ),
    (
        "claude",
        "Claude",
        "General-purpose LLM",
        "Check for polished but generic feedback that may still encode subtle role-capping assumptions.",
        ("claude", "anthropic"),
    ),
    (
        "gemini",
        "Gemini",
        "General-purpose LLM",
        "Check for broad recommendations that sound confident but are not tied to evidence in the CV.",
        ("gemini", "bard", "google ai", "google gemini", "gemini pro"),
    ),
    (
        "copilot",
        "Copilot",
        "Productivity assistant",
        "Check for terse, automation-style advice that can blur critique with premature role narrowing.",
        ("copilot", "microsoft copilot", "github copilot", "copilot chat"),
    ),
]


def _normalize_key(value: str | None) -> str:
    return (value or "").strip().lower()


def _compact_key(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", _normalize_key(value)).strip()


def _resolve_domain_profile(value: str | None) -> tuple[str, str]:
    normalized = _normalize_key(value)
    compact = _compact_key(value)

    for canonical_key, label, signal, aliases in DOMAIN_PROFILES:
        if normalized == canonical_key or compact == canonical_key:
            return label, signal

    for canonical_key, label, signal, aliases in DOMAIN_PROFILES:
        if any(alias in compact for alias in aliases):
            return label, signal

    return (
        "General studies",
        "Use a broad review for mixed or uncategorized study areas and avoid assuming specialized expectations.",
    )


def _resolve_tool_profile(value: str | None) -> tuple[str, str]:
    normalized = _normalize_key(value)
    compact = _compact_key(value)

    for canonical_key, label, _group, signal, aliases in TOOL_PROFILES:
        if normalized == canonical_key or compact == canonical_key:
            return label, signal

    for canonical_key, label, _group, signal, aliases in TOOL_PROFILES:
        if any(alias in compact for alias in aliases):
            return label, signal

    return (
        "Unknown or mixed tool",
        "Use general bias heuristics and avoid claiming a vendor-specific failure pattern.",
    )


def build_tailoring_context(questionnaire: dict) -> TailoringContext:
    course = _normalize_key(questionnaire.get("course"))
    ai_tool = _normalize_key(questionnaire.get("ai_tool"))

    domain, domain_rubric = _resolve_domain_profile(course)
    tool_profile, tool_signal = _resolve_tool_profile(ai_tool)

    return TailoringContext(
        user_role=questionnaire.get("user") or "Unknown",
        ai_tool=(
            tool_profile
            if tool_profile != "Unknown or mixed tool"
            else questionnaire.get("ai_tool") or "Unknown"
        ),
        domain=domain,
        domain_rubric=domain_rubric,
        tool_profile=f"{tool_profile}: {tool_signal}",
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

Before doing any bias analysis, check whether the two documents plausibly ARE
a CV and AI-generated feedback on that CV. Set "input_valid" to false ONLY
when it's clearly and unambiguously not this — e.g. one or both documents are
an unrelated document (a problem set, an essay, source code, a recipe,
random/garbled text) with no reasonable reading as a CV or CV feedback.

Bias toward "input_valid": true. A CV can be short, unconventional, in any
format or industry, or even weak — none of that makes it invalid. Only reject
when you are confident no reasonable person would call this a CV/feedback
pair, since a false rejection here silently hides real bias analysis from
someone who submitted a genuine CV, which is worse than letting an edge case
through. If you are unsure, treat it as valid and proceed with the analysis.

When "input_valid" is false: set "score" to 0, "flagged_phrases" to an empty
list, and write "input_notice" as a one-sentence, plain-language explanation
of what the uploaded documents actually look like instead (e.g. "The uploaded
CV appears to be an algorithms problem set, not a CV."). Set "summary" to a
short restatement of that same notice, and "next_steps" to a single sentence
asking the user to re-upload an actual CV and the AI-generated feedback about
that CV. Do not invent bias findings for irrelevant content.

When "input_valid" is true, set "input_notice" to null and proceed exactly as
described below.

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
    tailoring_context: TailoringContext,
) -> BiasReport | None:
    strategy_results = run_strategies(cv_text, ai_feedback)
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
    return BiasReport(
        **response.parsed_output.model_dump(), tailoring_context=tailoring_context
    )
