def calculate_confidence(diagnosis: dict, investigation: dict) -> dict:
    """
    Normalize confidence score and enrich with reasoning.

    Uses LLM-provided confidence when valid, with light adjustment
    based on available evidence quality.
    """
    raw_confidence = diagnosis.get("confidence")
    confidence_reasoning = diagnosis.get("confidence_reasoning", "")

    confidence = _normalize_score(raw_confidence)
    evidence_boost = _evidence_quality_score(investigation)

    if confidence is None:
        confidence = evidence_boost
        if not confidence_reasoning:
            confidence_reasoning = _default_reasoning(investigation, confidence)
    elif evidence_boost >= 70 and confidence < 50:
        confidence = min(confidence + 10, 100)
    elif evidence_boost <= 30 and confidence > 80:
        confidence = max(confidence - 15, 0)

    if not confidence_reasoning:
        confidence_reasoning = _default_reasoning(investigation, confidence)

    return {
        "confidence": confidence,
        "confidence_reasoning": confidence_reasoning,
    }


def _normalize_score(value) -> int | None:
    if value is None:
        return None

    try:
        score = int(float(value))
    except (TypeError, ValueError):
        return None

    return max(0, min(score, 100))


def _evidence_quality_score(investigation: dict) -> int:
    """Estimate confidence from investigation evidence richness."""
    score = 30

    pods = investigation.get("pods", {})
    if pods.get("problematic_pods"):
        score += 20

    logs = investigation.get("logs", {}).get("pod_logs", {})
    if logs:
        score += 20

    events = investigation.get("events", {}).get("findings", [])
    if events:
        score += 15

    deployments = investigation.get("deployments", {}).get("unhealthy_deployments", [])
    if deployments:
        score += 10

    network = investigation.get("network", {}).get("findings", [])
    if network:
        score += 5

    return min(score, 95)


def _default_reasoning(investigation: dict, confidence: int) -> str:
    reasons = []

    pods = investigation.get("pods", {})
    if pods.get("problematic_pods"):
        pod = pods["problematic_pods"][0]
        reasons.append(f"Pod {pod['name']} is in {pod['status']} state")

    logs = investigation.get("logs", {}).get("pod_logs", {})
    if logs:
        reasons.append("Application logs contain relevant error signals")

    events = investigation.get("events", {}).get("findings", [])
    if events:
        reasons.append(f"{len(events)} Kubernetes warning events support the diagnosis")

    if confidence >= 80:
        prefix = "High confidence because:"
    elif confidence >= 50:
        prefix = "Moderate confidence because:"
    else:
        prefix = "Low confidence because:"

    if not reasons:
        reasons.append("Limited evidence available from the cluster investigation")

    return f"{prefix}\n- " + "\n- ".join(reasons)
