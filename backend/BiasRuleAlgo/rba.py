from .strategies.lexicon_checker import LexiconChecker
from .strategies.hidden_ceiling import HiddenCeilingEngine
from .strategies.omission_penalty import OmissionPenalty
from .strategies.actionability_classifier import ActionabilityClassifier
from .strategies.career_gap import CareerGapPenalty

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
