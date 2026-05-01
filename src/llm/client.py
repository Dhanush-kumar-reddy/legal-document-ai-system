from openai import OpenAI
import os
import streamlit as st


class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=api_key)

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content