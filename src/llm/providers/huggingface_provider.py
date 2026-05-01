from huggingface_hub import InferenceClient
from llm.providers.base import BaseLLM
from utils.config import HF_API_KEY, HF_MODEL

class HuggingFaceProvider(BaseLLM):
    def __init__(self):
        self.client = InferenceClient(
            model=HF_MODEL,
            token=HF_API_KEY
        )

    def invoke(self, prompt: str) -> str:
        response = self.client.text_generation(
            prompt,
            max_new_tokens=512
        )
        return response