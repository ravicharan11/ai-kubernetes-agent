"""Backward-compatible re-exports for the Kubernetes investigation layer."""

from kubernetes.deployment_inspector import inspect_deployments
from kubernetes.events_analyzer import analyze_events
from kubernetes.pod_inspector import inspect_pods

__all__ = ["inspect_pods", "inspect_deployments", "analyze_events"]
