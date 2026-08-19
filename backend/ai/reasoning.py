import time
from loguru import logger

from ai.confidence_engine import calculate_confidence
from ai.fix_recommendation import build_fix_recommendation
from ai.llm_client import LLMClientError, chat_completion
from ai.prompt_builder import build_messages
from ai.root_cause_analyzer import analyze_root_cause


def is_cluster_healthy(investigation: dict) -> bool:
    """Check if the cluster has no issues."""
    pods = investigation.get("pods", {})
    logs = investigation.get("logs", {})
    events = investigation.get("events", {})
    deployments = investigation.get("deployments", {})
    network = investigation.get("network", {})

    # Check for problematic pods
    if pods.get("problematic_pods"):
        return False

    # Check for logs with errors
    if logs.get("pod_logs"):
        return False

    # Check for warning events
    if events.get("findings"):
        return False

    # Check for unhealthy deployments
    if deployments.get("unhealthy_deployments"):
        return False

    # Check for network issues
    if network.get("findings"):
        return False

    return True


def generate_diagnosis(investigation: dict) -> dict:
    """
    Run the full AI reasoning pipeline on investigation evidence.

    Flow:
        Check Health → Build Prompt → LLM Reasoning → Root Cause → Fix → Confidence
    """
    logger.info("Starting AI diagnosis")

    # Check if cluster is healthy
    if is_cluster_healthy(investigation):
        logger.info("Cluster is healthy, no issues detected")
        return {
            "available": True,
            "root_cause": "No issues detected",
            "explanation": "The Kubernetes cluster appears to be healthy with no critical issues found.",
            "fix": "No action required",
            "kubectl_command": "kubectl get pods --all-namespaces",
            "prevention_recommendation": "Continue monitoring the cluster regularly",
            "confidence": 100,
            "confidence_reasoning": "High confidence because no problematic pods, errors, events, or unhealthy deployments were found during investigation.",
        }

    messages = build_messages(investigation)

    try:
        logger.info("Calling LLM for AI reasoning...")
        llm_start_time = time.time()
        raw_response = chat_completion(messages)
        llm_duration = time.time() - llm_start_time
        logger.info(f"LLM response received in {llm_duration:.2f}s")
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
        "llm_duration_seconds": round(llm_duration, 2),
    }

    logger.info(
        f"AI diagnosis complete (confidence: {diagnosis['confidence']}%, LLM time: {llm_duration:.2f}s)"
    )
    return diagnosis
