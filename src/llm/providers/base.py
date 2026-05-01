class BaseLLM:
    def invoke(self, prompt: str) -> str:
        raise NotImplementedError