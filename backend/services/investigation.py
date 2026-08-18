from loguru import logger

from kubernetes.deployment_inspector import inspect_deployments
from kubernetes.events_analyzer import analyze_events
from kubernetes.logs_collector import collect_logs
from kubernetes.network_inspector import inspect_network
from kubernetes.pod_inspector import inspect_pods


def run_investigation() -> dict:
    """
    Orchestrate the full Kubernetes evidence-gathering flow.

    Flow:
        Check Pods → Collect Logs → Analyze Events → Inspect Deployments → Check Networking
    """
    logger.info("Starting Kubernetes investigation")

    investigation = {
        "pods": {},
        "logs": {},
        "events": {},
        "deployments": {},
        "network": {},
    }

    # Inspect pods
    try:
        pods = inspect_pods()
        logger.info(
            f"Pod inspection complete: {pods.get('total_pods', 0)} pods, "
            f"{len(pods.get('problematic_pods', []))} problematic"
        )
        investigation["pods"] = pods
    except Exception as e:
        logger.error(f"Pod inspection failed: {e}")
        investigation["pods"] = {
            "error": "Failed to inspect pods",
            "message": "Unable to connect to Kubernetes cluster. Please verify kubeconfig path and cluster access.",
            "total_pods": 0,
            "problematic_pods": [],
        }

    # Collect logs
    try:
        logs = collect_logs(investigation["pods"].get("problematic_pods", []))
        logger.info(f"Log collection complete: {logs.get('collected', 0)} pods")
        investigation["logs"] = logs
    except Exception as e:
        logger.error(f"Log collection failed: {e}")
        investigation["logs"] = {
            "error": "Failed to collect logs",
            "message": "Unable to retrieve pod logs. Check kubectl permissions.",
            "collected": 0,
            "logs": {},
        }

    # Analyze events
    try:
        events = analyze_events()
        logger.info(
            f"Event analysis complete: {events.get('relevant_findings', 0)} relevant findings"
        )
        investigation["events"] = events
    except Exception as e:
        logger.error(f"Event analysis failed: {e}")
        investigation["events"] = {
            "error": "Failed to analyze events",
            "message": "Unable to retrieve cluster events. Check kubectl permissions.",
            "relevant_findings": 0,
            "events": [],
        }

    # Inspect deployments
    try:
        deployments = inspect_deployments()
        logger.info(
            f"Deployment inspection complete: "
            f"{len(deployments.get('unhealthy_deployments', []))} unhealthy"
        )
        investigation["deployments"] = deployments
    except Exception as e:
        logger.error(f"Deployment inspection failed: {e}")
        investigation["deployments"] = {
            "error": "Failed to inspect deployments",
            "message": "Unable to retrieve deployment information. Check kubectl permissions.",
            "total_deployments": 0,
            "unhealthy_deployments": [],
        }

    # Inspect network
    try:
        network = inspect_network()
        logger.info(
            f"Network inspection complete: {len(network.get('findings', []))} findings"
        )
        investigation["network"] = network
    except Exception as e:
        logger.error(f"Network inspection failed: {e}")
        investigation["network"] = {
            "error": "Failed to inspect network",
            "message": "Unable to retrieve network information. Check kubectl permissions.",
            "findings": [],
        }

    logger.info("Kubernetes investigation complete")
    return investigation
