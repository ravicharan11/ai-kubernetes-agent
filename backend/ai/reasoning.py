from loguru import logger

from ai.confidence_engine import calculate_confidence
from ai.fix_recommendation import build_fix_recommendation
from ai.llm_client import LLMClientError, chat_completion
from ai.prompt_builder import build_messages
from ai.root_cause_analyzer import analyze_root_cause


def generate_diagnosis(investigation: dict) -> dict:
    """
    Run the full AI reasoning pipeline on investigation evidence.

    Flow:
        Build Prompt → LLM Reasoning → Root Cause → Fix → Confidence
    """
    logger.info("Starting AI diagnosis")

    messages = build_messages(investigation)

    try:
        raw_response = chat_completion(messages)
    except LLMClientError as exc:
        logger.error(f"LLM client error: {exc}")
        return {
            "available": False,
            "error": str(exc),
        }

    try:
        parsed = analyze_root_cause(investigation, raw_response)
    except ValueError as exc:
        logger.error(f"Failed to parse AI diagnosis: {exc}")
        return {
            "available": False,
            "error": str(exc),
        }

    fix = build_fix_recommendation(parsed)
    confidence = calculate_confidence(parsed, investigation)

    diagnosis = {
        "available": True,
        "root_cause": parsed["root_cause"],
        "explanation": parsed["explanation"],
        "fix": fix["fix"],
        "kubectl_command": fix["kubectl_command"],
        "prevention_recommendation": fix["prevention_recommendation"],
        "confidence": confidence["confidence"],
        "confidence_reasoning": confidence["confidence_reasoning"],
    }

    logger.info(
        f"AI diagnosis complete (confidence: {diagnosis['confidence']}%)"
    )
    return diagnosis
