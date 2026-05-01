import json
from src.llm.prompts import CLAUSE_CLASSIFICATION_PROMPT
from src.processing.validator import validate_classification
from src.utils.logger import get_logger

logger = get_logger()

import re
import json

import re
import json

def extract_json(text):
    try:
        # Remove markdown ```json ``` if present
        text = text.replace("```json", "").replace("```", "")

        # Extract JSON block
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)

    except Exception as e:
        print("JSON extraction failed:", e)

    raise ValueError("Invalid JSON from LLM")
    
def classify_clause(llm, clause_text, clause_id, domain):
    prompt = CLAUSE_CLASSIFICATION_PROMPT.format(
        domain=domain,
        clause_text=clause_text
    )
    print("\n===== PROMPT =====\n")
    print(prompt[:500])
    print("\n==================\n")
    response = llm.invoke(prompt)
    print("\n===== RAW RESPONSE =====\n")
    print(response)
    print("\n========================\n")
    result = extract_json(response)
    result["clause_id"] = clause_id
    result = validate_classification(result)
    return result