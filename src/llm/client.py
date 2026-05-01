from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=api_key)

    def invoke(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:
            print("LLM CLIENT ERROR:", e)
            raise