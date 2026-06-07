# DESIGNING THE RULE-BASED ALGORITHM:
# Rule Based Algo -> Very Basic Bias Detection | It also gets passed into the API after for better context.

# 1) Words with weights in a dictionary,
# words from the AI response get flagged + depending on context questions answered.

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
