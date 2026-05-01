from utils.config import LLM_PROVIDER
from llm.providers.openai_provider import OpenAIProvider
from llm.providers.huggingface_provider import HuggingFaceProvider

def get_llm():
    if LLM_PROVIDER == "openai":
        return OpenAIProvider()
    elif LLM_PROVIDER == "huggingface":
        return HuggingFaceProvider()
    else:
        raise ValueError("Invalid LLM provider")