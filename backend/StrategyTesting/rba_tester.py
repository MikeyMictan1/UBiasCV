import os

from BiasAI.extract import extract_text
from BiasRuleAlgo.strategies.actionability_classifier import ActionabilityClassifier
from BiasRuleAlgo.strategies.career_gap import CareerGapPenalty
from BiasRuleAlgo.strategies.hidden_ceiling import HiddenCeilingEngine
from BiasRuleAlgo.strategies.lexicon_checker import LexiconChecker
from BiasRuleAlgo.strategies.omission_penalty import OmissionPenalty

modules = [
    ActionabilityClassifier(),
    CareerGapPenalty(),
    HiddenCeilingEngine(),
    LexiconChecker(),
    OmissionPenalty(),
]


# Adapts a local file on disk to the UploadFile type that extract_text expects
class _LocalUpload:
    def __init__(self, filepath: str):
        self.filename = os.path.basename(filepath)
        self.file = open(filepath, "rb")

    def close(self) -> None:
        try:
            self.file.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

# The core strategy testing service
def test_strategies(strategies):
    # Formatting + Setup
    print("--------------------- RBA Strategy Tester ---------------------")
    test_num = int(input("Which Test is this (e.g. X in testXgender.pdf): "))
    print("---------------------------------------------------------------")
    print("1) Female")
    print("2) Male")
    print("3) Other")
    gender_val = int(input("What is the gender of the CV: "))
    print("---------------------------------------------------------------")
    print("1) Actionability Classifier")
    print("2) Career Gap Penalty")
    print("3) Hidden Ceiling Engine")
    print("4) Lexicon Checker")
    print("5) Omission Penalty")
    print("Any other int input for all strategies")
    strategy = int(input("What Strategy Would You Like To Test: "))

    # Filepath creation
    match gender_val:
        case 1:
            test_gender = "female"
        case 2:
            test_gender = "male"
        case _:
            test_gender = "other"

    cv_filepath = f"StrategyTesting/SampleCVFeedback/test{test_num}{test_gender}.pdf"
    feedback_filepath = (
        f"StrategyTesting/SampleCVFeedback/test{test_num}{test_gender}_feedback.txt"
    )

    # Strategy selection
    match strategy:
        case 1:
            strategies = [ActionabilityClassifier()]
        case 2:
            strategies = [CareerGapPenalty()]
        case 3:
            strategies = [HiddenCeilingEngine()]
        case 4:
            strategies = [LexiconChecker()]
        case 5:
            strategies = [OmissionPenalty()]
        case _:
            strategies = strategies

    # Getting the CV + feedback text from the files
    cv_text = extract_text(_LocalUpload(cv_filepath))
    feedback_text = extract_text(_LocalUpload(feedback_filepath))

    # Running the RBA strategies
    results = []
    for strategy in strategies:
        result = strategy.analyse(cv_text, feedback_text)
        results.append(result)
    return results


# Print strategy results
def print_results(results):
    for result in results:
        print(f"\n=== {result.strategy} (score: {result.score}) ===")
        if not result.evidence:
            print("  (no evidence flagged)")
        for line in result.evidence:
            print(f"  - {line}")


# --------- Running the tests ----------
print_results(test_strategies(modules))
