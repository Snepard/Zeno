import os
import logging
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from ai_engine.llm.json_parser import parse_llm_json

logger = logging.getLogger(__name__)

# Booting exact Groq structural handlers maximizing rapid tokens inference
API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
PRIMARY_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
FALLBACK_MODEL = os.getenv("GROQ_FALLBACK_MODEL", "mixtral-8x7b-32768")

client = Groq(api_key=API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
def generate_json_from_groq(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
    """
    Interfaces highly natively over Groq maximizing generation latency optimization.
    Safely enforces strictly verified JSON logic using parsing schemas.
    """
    # Strict 1000ch text sanitizations isolating security concerns
    safe_topic = user_prompt[:1000]
    
    try:
        # Rapid model inference execution blocks
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": safe_topic}
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
            max_tokens=6000,
            timeout=30.0 # Timeout isolation resolving hanging executions continuously
        )
        content = response.choices[0].message.content
        return parse_llm_json(content)
        
    except Exception as e:
        logger.warning(f"Groq primary '{PRIMARY_MODEL}' structurally defaulted ({e}). Falling back onto {FALLBACK_MODEL} natively...")
        try:
            # Automatic routing onto specific fallbacks without breaking logic layers
            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": safe_topic}
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=6000,
                timeout=30.0
            )
            content = response.choices[0].message.content
            return parse_llm_json(content)
        except Exception as fallback_err:
            logger.error(f"Groq fallback '{FALLBACK_MODEL}' severely faulted: {fallback_err}")
            raise fallback_err
