import json
import re

from loguru import logger


def parse_llm_diagnosis(raw_response: str) -> dict:
    """Parse structured diagnosis JSON from the LLM response."""
    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error(f"Failed to parse LLM JSON: {exc}")
        raise ValueError("LLM response was not valid JSON") from exc

    required_fields = ("root_cause", "explanation", "fix", "kubectl_command")
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        raise ValueError(f"LLM response missing required fields: {', '.join(missing)}")

    return {
        "root_cause": str(data["root_cause"]).strip(),
        "explanation": str(data["explanation"]).strip(),
        "fix": str(data["fix"]).strip(),
        "kubectl_command": str(data["kubectl_command"]).strip(),
        "prevention_recommendation": str(
            data.get("prevention_recommendation", "")
        ).strip(),
        "confidence": data.get("confidence"),
        "confidence_reasoning": str(data.get("confidence_reasoning", "")).strip(),
    }


def analyze_root_cause(investigation: dict, raw_llm_response: str) -> dict:
    """
    Parse and validate root cause analysis from LLM output.

    Ensures the diagnosis correlates with available investigation evidence.
    """
    diagnosis = parse_llm_diagnosis(raw_llm_response)

    evidence_summary = _summarize_evidence(investigation)
    if evidence_summary and diagnosis["root_cause"]:
        logger.info(
            f"Root cause identified: {diagnosis['root_cause'][:120]}"
        )
        logger.debug(f"Evidence summary: {evidence_summary}")

    return diagnosis


def _summarize_evidence(investigation: dict) -> str:
    """Build a short evidence summary for logging."""
    parts = []

    pods = investigation.get("pods", {})
    problematic = pods.get("problematic_pods", [])
    if problematic:
        parts.append(f"{len(problematic)} problematic pod(s)")

    events = investigation.get("events", {})
    if events.get("relevant_findings", 0):
        parts.append(f"{events['relevant_findings']} relevant event(s)")

    deployments = investigation.get("deployments", {})
    unhealthy = deployments.get("unhealthy_deployments", [])
    if unhealthy:
        parts.append(f"{len(unhealthy)} unhealthy deployment(s)")

    network = investigation.get("network", {})
    if network.get("findings"):
        parts.append(f"{len(network['findings'])} network finding(s)")

    return ", ".join(parts) if parts else "no major issues detected"
