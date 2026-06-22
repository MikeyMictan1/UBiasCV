from strategies.lexicon_checker import LexiconChecker
from strategies.hidden_ceiling import HiddenCeilingEngine
from strategies.omission_penalty import OmissionPenalty
from strategies.actionability_classifier import ActionabilityClassifier
from strategies.career_gap import CareerGapPenalty

modules = [
    LexiconChecker(),
    HiddenCeilingEngine(),
    OmissionPenalty(),
    ActionabilityClassifier(),
    CareerGapPenalty(),
]


# Runs the strategies on the given text, will change as needed. Can plug in any strategies as needed as we are loosely coupled strategies with the strategy pattern.
def run_strategies(cv_text: str, feedback_text: str):
    results = []
    for module in modules:
        result = module.analyse(cv_text, feedback_text)
        results.append(result)
    return results


# Old data, to be moved to json
"""
flagged_words_leadership = {
    "assertive": 80,
    "aggressive": 90,
    "ambitious": 60,
    "dominant": 90,
    "confident": 60,
    "nurturing": 80,
    "compassionate": 70,
    "collaborative": 50,
    "supportive": 60,
}

flagged_words_achievement = {
    "brilliant": 70,
    "genius": 80,
    "logical": 60,
    "hardworking": 40,
    "diligent": 40,
    "organized": 40,
}

flagged_words_appearance = {
    "beautiful": 90,
    "pretty": 90,
    "strong": 50,
    "powerful": 60,
    "attractive": 80,
}
"""
