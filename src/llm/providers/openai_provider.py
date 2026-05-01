from openai import OpenAI
from llm.providers.base import BaseLLM
from utils.config import OPENAI_API_KEY

class OpenAIProvider(BaseLLM):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content