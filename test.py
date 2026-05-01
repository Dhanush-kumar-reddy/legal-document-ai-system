from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI()

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
            return "ERROR"