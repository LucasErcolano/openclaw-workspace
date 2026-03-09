class LLMRouter:
    def __init__(self):
        pass

    def execute_llm_json(self, prompt: str, task: str):
        return {"fallback_depth": 0, "text": ""}

    def route(self, prompt: str, task: str):
        return {"fallback_depth": 0, "text": ""}
