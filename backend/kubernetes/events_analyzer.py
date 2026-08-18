from kubernetes.kubectl_executor import run_kubectl_json

WATCHED_EVENT_REASONS = {
    "FailedScheduling",
    "BackOff",
    "FailedMount",
    "FailedPull",
    "ErrImagePull",
    "Unhealthy",
}


def _summarize_event(event: dict) -> dict:
    involved = event.get("involvedObject", {})
    return {
        "reason": event.get("reason", "Unknown"),
        "type": event.get("type", "Unknown"),
        "message": event.get("message", ""),
        "namespace": event.get("metadata", {}).get("namespace", "default"),
        "object_kind": involved.get("kind", ""),
        "object_name": involved.get("name", ""),
        "count": event.get("count", 1),
        "last_timestamp": event.get("lastTimestamp")
        or event.get("eventTime")
        or event.get("firstTimestamp"),
    }


def analyze_events() -> dict:
    """Read cluster events and summarize troubleshooting-relevant findings."""
    data, result = run_kubectl_json(["get", "events", "-A", "--sort-by=.lastTimestamp"])

    if data is None:
        return {
            "total_events": 0,
            "findings": [],
            "error": result.stderr or "Failed to fetch events",
        }

    items = data.get("items", [])
    findings = []

    for event in items:
        reason = event.get("reason", "")
        if reason in WATCHED_EVENT_REASONS or event.get("type") == "Warning":
            if reason in WATCHED_EVENT_REASONS or _is_relevant_warning(event):
                findings.append(_summarize_event(event))

    # Keep the most recent findings concise
    findings = findings[-20:]

    return {
        "total_events": len(items),
        "relevant_findings": len(findings),
        "findings": findings,
    }


def _is_relevant_warning(event: dict) -> bool:
    message = (event.get("message") or "").lower()
    keywords = ("failed", "error", "back-off", "unhealthy", "pull", "mount", "schedule")
    return any(keyword in message for keyword in keywords)
