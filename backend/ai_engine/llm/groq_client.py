import logging
from groq import Groq, BadRequestError, RateLimitError
from ai_engine.llm.json_parser import parse_llm_json
from config.settings import settings

logger = logging.getLogger(__name__)

_HARD_FAIL = (BadRequestError, RateLimitError)


def _get_client(api_key: str) -> Groq:
    """Returns a Groq client for the given key, falling back to default if empty."""
    key = api_key.strip() if api_key and api_key.strip() else settings.GROQ_API_KEY
    return Groq(api_key=key)


def _call_model(client: Groq, model: str, system_prompt: str, user_prompt: str, temperature: float, expect_json: bool) -> str:
    """Single model call. Raises on any error. Returns raw string."""
    params = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": 4096,
        "timeout": 30.0
    }
    if expect_json:
        params["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**params)
    return response.choices[0].message.content


def _cascade(api_key: str, system_prompt: str, user_prompt: str, temperature: float, expect_json: bool) -> str:
    client = _get_client(api_key)
    safe_prompt = user_prompt[:2500]

    models = [
        settings.GROQ_MODEL,
        settings.GROQ_FALLBACK_MODEL,
        settings.GROQ_FALLBACK_MODEL_2,
    ]

    last_err = None
    for i, model in enumerate(models):
        try:
            logger.info(f"Groq: trying '{model}' (tier {i + 1}/{len(models)})")
            return _call_model(client, model, system_prompt, safe_prompt, temperature, expect_json)
        except _HARD_FAIL as e:
            logger.warning(f"Groq '{model}' hard-failed ({type(e).__name__}): cascading...")
            last_err = e
        except Exception as e:
            logger.warning(f"Groq '{model}' transient error ({e}): cascading...")
            last_err = e

    logger.error(f"All Groq tiers exhausted. Last error: {last_err}")
    raise last_err


# ── Public API ─────────────────────────────────────────────────────────────────

def generate_json_from_groq(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
    """Default / legacy — uses GROQ_API_KEY_CLASS."""
    return generate_class_completion(system_prompt, user_prompt, temperature)


def generate_class_completion(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
    logger.info("Groq: routing to CLASS client")
    raw = _cascade(settings.GROQ_API_KEY_CLASS, system_prompt, user_prompt, temperature, expect_json=True)
    return parse_llm_json(raw)


def generate_podcast_completion(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
    logger.info("Groq: routing to PODCAST client")
    raw = _cascade(settings.GROQ_API_KEY_PODCAST, system_prompt, user_prompt, temperature, expect_json=True)
    return parse_llm_json(raw)


def generate_video_completion(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
    logger.info("Groq: routing to VIDEO client")
    raw = _cascade(settings.GROQ_API_KEY_VIDEO, system_prompt, user_prompt, temperature, expect_json=True)
    return parse_llm_json(raw)


def generate_chat_completion(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Standard text reply for Chatbot / RAG queries (no JSON enforcement). Uses CLASS key quota."""
    logger.info("Groq: routing to CHATBOT text client")
    return _cascade(settings.GROQ_API_KEY_CLASS, system_prompt, user_prompt, temperature, expect_json=False)
