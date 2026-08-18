from kubernetes.kubectl_executor import run_kubectl_json

UNHEALTHY_WAITING_REASONS = {
    "CrashLoopBackOff",
    "ImagePullBackOff",
    "ErrImagePull",
    "CreateContainerConfigError",
    "InvalidImageName",
    "CreateContainerError",
    "ContainerCreating",
}

UNHEALTHY_TERMINATED_REASONS = {
    "OOMKilled",
    "Error",
}


def _get_container_statuses(pod: dict) -> list[dict]:
    statuses = []
    for key in ("containerStatuses", "initContainerStatuses"):
        statuses.extend(pod.get("status", {}).get(key) or [])
    return statuses


def _detect_pod_issue(pod: dict) -> str | None:
    phase = pod.get("status", {}).get("phase", "Unknown")

    if phase == "Pending":
        return "Pending"

    if phase == "Failed":
        return "Error"

    for container in _get_container_statuses(pod):
        state = container.get("state", {})
        waiting = state.get("waiting", {})
        terminated = state.get("terminated", {})

        if waiting.get("reason") in UNHEALTHY_WAITING_REASONS:
            return waiting["reason"]

        if terminated.get("reason") in UNHEALTHY_TERMINATED_REASONS:
            return terminated["reason"]

        last_state = container.get("lastState", {}).get("terminated", {})
        if last_state.get("reason") in UNHEALTHY_TERMINATED_REASONS:
            return last_state["reason"]

        if waiting.get("reason") == "CrashLoopBackOff":
            return "CrashLoopBackOff"

    return None


def inspect_pods() -> dict:
    """Get pod status and detect unhealthy pods across all namespaces."""
    data, result = run_kubectl_json(["get", "pods", "-A"])

    if data is None:
        return {
            "healthy": None,
            "total_pods": 0,
            "problematic_pods": [],
            "error": result.stderr or "Failed to fetch pods",
        }

    items = data.get("items", [])
    problematic_pods = []

    for pod in items:
        issue = _detect_pod_issue(pod)
        if issue:
            metadata = pod.get("metadata", {})
            problematic_pods.append(
                {
                    "name": metadata.get("name", "unknown"),
                    "namespace": metadata.get("namespace", "default"),
                    "status": issue,
                    "phase": pod.get("status", {}).get("phase", "Unknown"),
                }
            )

    return {
        "healthy": len(problematic_pods) == 0,
        "total_pods": len(items),
        "problematic_pods": problematic_pods,
    }
