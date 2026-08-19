import time

from groq import Groq
from loguru import logger

from core.config import settings


class LLMClientError(Exception):
    """Raised when the LLM client fails after retries."""


def list_available_models() -> list[str]:
    """List all available Groq models."""
    try:
        client = Groq(api_key=settings.groq_api_key)
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        logger.info(f"Available Groq models: {model_ids}")
        return model_ids
    except Exception as exc:
        logger.error(f"Failed to list Groq models: {exc}")
        return []


def chat_completion(messages: list[dict]) -> str:
    """
    Send a chat completion request to Groq.

    Uses Groq SDK with timeout handling and simple retry logic.
    """
    if not settings.groq_api_key:
        raise LLMClientError(
            "GROQ_API_KEY is not configured. "
            "Get your free API key from https://console.groq.com/keys and add it to backend/.env"
        )

    model = settings.groq_model or "gemma2-9b-it"
    last_error = "Unknown error"

    for attempt in range(1, settings.groq_max_retries + 1):
        try:
            logger.info(f"Groq request attempt {attempt}/{settings.groq_max_retries} with model: {model}")

            client = Groq(api_key=settings.groq_api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                timeout=settings.groq_timeout,
            )

            content = response.choices[0].message.content.strip()

            if not content:
                raise LLMClientError("Groq returned an empty response")

            logger.info("Groq request succeeded")
            return content

        except Exception as exc:
            last_error = f"Groq error: {exc}"
            logger.warning(f"{last_error} (attempt {attempt})")
            
            # If it's a model not found error, try to get available models
            if "model" in str(exc).lower() and "not found" in str(exc).lower():
                available_models = list_available_models()
                if available_models:
                    logger.info(f"Available models: {available_models}")
                    last_error = f"Model '{model}' not found. Available models: {available_models[:5]}"

        if attempt < settings.groq_max_retries:
            time.sleep(attempt)

    raise LLMClientError(last_error)
