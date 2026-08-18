from kubernetes.kubectl_executor import run_kubectl

LOG_TAIL_LINES = 80
ERROR_KEYWORDS = (
    "error",
    "exception",
    "failed",
    "failure",
    "fatal",
    "panic",
    "connection refused",
    "connection reset",
    "timeout",
    "not found",
    "no such file",
    "permission denied",
    "env",
    "imagepull",
    "back-off",
    "crash",
)


def _filter_relevant_lines(lines: list[str], max_lines: int = 30) -> list[str]:
    """Keep error-related lines; fall back to the most recent lines."""
    relevant = [
        line
        for line in lines
        if any(keyword in line.lower() for keyword in ERROR_KEYWORDS)
    ]

    if relevant:
        return relevant[-max_lines:]

    return lines[-max_lines:]


def _fetch_pod_logs(namespace: str, pod_name: str, previous: bool = False) -> dict:
    args = ["logs", pod_name, "-n", namespace, f"--tail={LOG_TAIL_LINES}"]
    if previous:
        args.append("--previous")

    result = run_kubectl(args)

    if not result.success:
        return {
            "available": False,
            "lines": [],
            "error": result.stderr.strip() or "Failed to fetch logs",
        }

    lines = result.stdout.strip().splitlines()
    return {
        "available": True,
        "lines": _filter_relevant_lines(lines),
        "total_lines_fetched": len(lines),
    }


def collect_logs(problematic_pods: list[dict]) -> dict:
    """Fetch concise logs for failed or unhealthy pods."""
    if not problematic_pods:
        return {"collected": 0, "pod_logs": {}}

    pod_logs = {}

    for pod in problematic_pods:
        namespace = pod["namespace"]
        name = pod["name"]
        key = f"{namespace}/{name}"

        logs = _fetch_pod_logs(namespace, name)

        if pod.get("status") == "CrashLoopBackOff":
            previous_logs = _fetch_pod_logs(namespace, name, previous=True)
            if previous_logs["available"]:
                logs["previous_container"] = previous_logs

        pod_logs[key] = logs

    return {
        "collected": len(pod_logs),
        "pod_logs": pod_logs,
    }
