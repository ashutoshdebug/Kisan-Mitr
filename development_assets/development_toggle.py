import json

class DevelopmentPhase:
    def __init__(self):
        pass

    def developmentResult(self):
        with open("development_assets/result.json", "r", encoding="utf-8") as file:
            result = json.load(file)
            return result