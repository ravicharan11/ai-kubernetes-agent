import json

SYSTEM_PROMPT = """You are a Senior Kubernetes SRE performing incident triage.

Your job is to analyze cluster investigation evidence and produce a precise diagnosis.
Correlate information across pods, logs, events, deployments, and networking.
Do not summarize blindly — identify the most likely root cause by connecting evidence.

Rules:
- Be specific and actionable
- Reference actual resource names and namespaces from the evidence
- Prefer the simplest explanation that fits all signals
- Provide practical kubectl commands a beginner can run
- Avoid vague advice like "check the logs" without specifics
- If evidence is insufficient, state that clearly and lower confidence

You MUST respond with ONLY valid JSON (no markdown fences) using this schema:
{
  "root_cause": "One concise sentence stating the root cause",
  "explanation": "2-4 sentences explaining how the evidence supports this conclusion",
  "fix": "Clear actionable fix steps",
  "kubectl_command": "Primary kubectl command to apply the fix",
  "prevention_recommendation": "How to prevent recurrence",
  "confidence": 85,
  "confidence_reasoning": "Why this confidence level is appropriate"
}

The confidence field must be an integer from 0 to 100.
"""


def build_messages(investigation: dict) -> list[dict]:
    """Build structured LLM messages from an investigation payload."""
    evidence = {
        "pod_status": investigation.get("pods", {}),
        "logs": investigation.get("logs", {}),
        "events": investigation.get("events", {}),
        "deployment_health": investigation.get("deployments", {}),
        "networking_findings": investigation.get("network", {}),
    }

    user_prompt = f"""Analyze this Kubernetes cluster investigation evidence and produce a diagnosis.

Evidence:
{json.dumps(evidence, indent=2)}

Return ONLY the JSON diagnosis object described in your instructions."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
