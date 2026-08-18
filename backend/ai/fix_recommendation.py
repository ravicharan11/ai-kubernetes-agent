def build_fix_recommendation(diagnosis: dict) -> dict:
    """
    Extract and normalize actionable fix recommendations.

    Ensures kubectl commands are practical and Kubernetes-specific.
    """
    kubectl_command = diagnosis.get("kubectl_command", "").strip()
    fix = diagnosis.get("fix", "").strip()

    if kubectl_command and not kubectl_command.startswith("kubectl"):
        kubectl_command = f"kubectl {kubectl_command.lstrip()}"

    return {
        "fix": fix or "Review the identified root cause and apply the recommended changes.",
        "kubectl_command": kubectl_command or "kubectl get pods -A",
        "prevention_recommendation": diagnosis.get("prevention_recommendation", "").strip()
        or "Add monitoring and validation to catch similar failures early.",
    }
