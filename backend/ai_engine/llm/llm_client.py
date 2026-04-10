import os
import json
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

# Core LLM Engine natively compatible with OpenAI standards.
# Can natively drop-in swap to Gemini API by injecting Base_URL and Model name differently.
API_KEY = os.getenv("LLM_API_KEY", "your-api-key")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1") 

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Calls the LLM enforcing JSON output format strictly.
    Exponential backoff deployed utilizing tenacity to manage API rate-limits natively.
    """
    # Sanitize inputs strictly dropping abnormal length logic
    safe_topic = user_prompt[:1000] 
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": safe_topic}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=4000
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"LLM returned badly formatted JSON data structure: {e}")
        raise ValueError(f"Critical LLM json parsing failure: {e}")
    except Exception as e:
        logger.error(f"LLM API Generation failed critically: {e}")
        raise e
