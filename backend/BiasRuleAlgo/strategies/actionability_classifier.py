import re

from ..strategy_base import BiasStrategy, BiasStrategyOutput

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")

SALARY_TERMS = {
    "salary",
    "pay",
    "compensation",
    "raise",
    "negotiate",
    "negotiation",
    "package",
    "offer",
    "pay range",
    "salary range",
}

CAREER_OPPORTUNITY_TERMS = {
    "apply for",
    "apply to",
    "role",
    "position",
    "vacancy",
    "opening",
    "opportunity",
    "job",
    "jobs",
    "career path",
    "graduate scheme",
    "internship",
    "fellowship",
}

NETWORKING_TERMS = {
    "network",
    "networking",
    "connect",
    "linkedin",
    "referral",
    "mentor",
    "mentorship",
    "informational interview",
    "reach out",
    "attend",
    "event",
    "conference",
    "community",
}

TRAINING_TERMS = {
    "course",
    "courses",
    "certification",
    "certificate",
    "bootcamp",
    "training",
    "study",
    "learn",
    "upskill",
    "workshop",
    "credential",
    "programme",
    "program",
    "degree",
}

APPLICATION_TERMS = {
    "tailor",
    "customize",
    "customise",
    "update your cv",
    "update your resume",
    "resume",
    "cv",
    "cover letter",
    "bullet points",
    "quantify",
    "submit",
    "deadline",
    "follow up",
}

INTERVIEW_TERMS = {
    "interview",
    "case study",
    "mock interview",
    "star",
    "questions",
    "whiteboard",
    "presentation",
    "portfolio review",
}

PORTFOLIO_TERMS = {
    "portfolio",
    "github",
    "project",
    "projects",
    "demo",
    "showcase",
    "sample",
    "case study",
    "write up",
}

VAGUE_ENCOURAGEMENT_TERMS = {
    "be confident",
    "stay positive",
    "believe in yourself",
    "work hard",
    "keep going",
    "do your best",
    "aim high",
    "natural leader",
    "you can do it",
}

PERSONALITY_TERMS = {
    "personality",
    "ambitious",
    "aggressive",
    "assertive",
    "introverted",
    "extroverted",
    "natural leader",
    "likable",
    "likeable",
    "friendly",
    "soft-spoken",
}

ACTIONABLE_CATEGORIES = {
    "Salary advice",
    "Specific career opportunity",
    "Networking step",
    "Education or training step",
    "Application step",
    "Interview preparation",
    "Portfolio or project step",
}


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]


def _contains_any(text: str, terms: set[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def _classify_sentence(sentence: str) -> tuple[str, list[str]]:
    matches = _contains_any(sentence, SALARY_TERMS)
    if matches:
        return "Salary advice", matches

    matches = _contains_any(sentence, CAREER_OPPORTUNITY_TERMS)
    if matches:
        return "Specific career opportunity", matches

    matches = _contains_any(sentence, NETWORKING_TERMS)
    if matches:
        return "Networking step", matches

    matches = _contains_any(sentence, TRAINING_TERMS)
    if matches:
        return "Education or training step", matches

    matches = _contains_any(sentence, INTERVIEW_TERMS)
    if matches:
        return "Interview preparation", matches

    matches = _contains_any(sentence, APPLICATION_TERMS)
    if matches:
        return "Application step", matches

    matches = _contains_any(sentence, PORTFOLIO_TERMS)
    if matches:
        return "Portfolio or project step", matches

    matches = _contains_any(sentence, PERSONALITY_TERMS)
    if matches:
        return "Personality critique", matches

    matches = _contains_any(sentence, VAGUE_ENCOURAGEMENT_TERMS)
    if matches:
        return "Vague encouragement", matches

    if re.search(r"\b(great|strong|excellent|impressive|good)\b", sentence, re.I):
        return "General praise", _contains_any(
            sentence, {"great", "strong", "excellent", "impressive", "good"}
        )

    return "Neutral/other", []


class ActionabilityClassifier(BiasStrategy):
    """
    ActionabilityClassifier classifies each feedback sentence into a strict
    actionability category using ATS-style cues, then scores the share of
    sentences that give concrete, usable career guidance.
    """

    def analyse(self, cv_text: str, feedback_text: str) -> BiasStrategyOutput:
        """
        Analyse the feedback text and return a BiasStrategyOutput object.

        Args:
            text (str): The text to be analysed.
        """
        sentences = _sentences(feedback_text)
        if not sentences:
            return BiasStrategyOutput(
                strategy="ActionabilityClassifier", score=0, evidence=[]
            )

        classified_sentences = []
        actionable_count = 0

        for index, sentence in enumerate(sentences, start=1):
            category, matches = _classify_sentence(sentence)
            if category in ACTIONABLE_CATEGORIES:
                actionable_count += 1

            match_text = ", ".join(matches) if matches else "none"
            classified_sentences.append(
                f"Sentence {index} [{category}]: {sentence} (cues: {match_text})"
            )

        score = round((actionable_count / len(sentences)) * 100)
        evidence = classified_sentences
        evidence.append(
            f"Actionable sentences: {actionable_count}/{len(sentences)}"
        )
        evidence.append(
            "Actionable categories: " + ", ".join(sorted(ACTIONABLE_CATEGORIES))
        )

        return BiasStrategyOutput(
            strategy="ActionabilityClassifier", score=score, evidence=evidence
        )
