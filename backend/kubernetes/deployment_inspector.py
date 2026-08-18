from kubernetes.kubectl_executor import run_kubectl_json


def _inspect_deployment(deployment: dict) -> dict | None:
    metadata = deployment.get("metadata", {})
    spec = deployment.get("spec", {})
    status = deployment.get("status", {})

    desired = spec.get("replicas", 0)
    available = status.get("availableReplicas", 0) or 0
    unavailable = status.get("unavailableReplicas", 0) or 0
    ready = status.get("readyReplicas", 0) or 0

    conditions = []
    for condition in status.get("conditions", []):
        conditions.append(
            {
                "type": condition.get("type"),
                "status": condition.get("status"),
                "reason": condition.get("reason"),
                "message": condition.get("message"),
            }
        )

    unhealthy = available < desired or unavailable > 0 or any(
        c.get("type") == "Available" and c.get("status") != "True" for c in conditions
    )

    if not unhealthy:
        return None

    rollout_failed = any(
        c.get("type") == "Progressing"
        and c.get("status") == "False"
        and c.get("reason") == "ProgressDeadlineExceeded"
        for c in conditions
    )

    return {
        "name": metadata.get("name", "unknown"),
        "namespace": metadata.get("namespace", "default"),
        "desired_replicas": desired,
        "available_replicas": available,
        "ready_replicas": ready,
        "unavailable_replicas": unavailable,
        "rollout_failed": rollout_failed,
        "conditions": conditions,
    }


def inspect_deployments() -> dict:
    """Inspect deployments for replica and rollout issues."""
    data, result = run_kubectl_json(["get", "deployments", "-A"])

    if data is None:
        return {
            "healthy": None,
            "total_deployments": 0,
            "unhealthy_deployments": [],
            "error": result.stderr or "Failed to fetch deployments",
        }

    items = data.get("items", [])
    unhealthy_deployments = []

    for deployment in items:
        issue = _inspect_deployment(deployment)
        if issue:
            unhealthy_deployments.append(issue)

    return {
        "healthy": len(unhealthy_deployments) == 0,
        "total_deployments": len(items),
        "unhealthy_deployments": unhealthy_deployments,
    }
