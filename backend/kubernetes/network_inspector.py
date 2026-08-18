from kubernetes.kubectl_executor import run_kubectl_json


def _build_endpoint_map(endpoints_data: dict | None) -> dict[tuple[str, str], list[str]]:
    """Map (namespace, service-name) to endpoint addresses."""
    endpoint_map: dict[tuple[str, str], list[str]] = {}

    if not endpoints_data:
        return endpoint_map

    for item in endpoints_data.get("items", []):
        metadata = item.get("metadata", {})
        namespace = metadata.get("namespace", "default")
        name = metadata.get("name", "")
        addresses = []

        for subset in item.get("subsets", []):
            for address in subset.get("addresses", []):
                addresses.append(address.get("ip", ""))
            for not_ready in subset.get("notReadyAddresses", []):
                addresses.append(f"{not_ready.get('ip', '')} (not ready)")

        endpoint_map[(namespace, name)] = [addr for addr in addresses if addr]

    return endpoint_map


def _check_service(service: dict, endpoint_map: dict) -> dict | None:
    metadata = service.get("metadata", {})
    spec = service.get("spec", {})
    namespace = metadata.get("namespace", "default")
    name = metadata.get("name", "unknown")

    selector = spec.get("selector") or {}
    service_type = spec.get("type", "ClusterIP")
    endpoints = endpoint_map.get((namespace, name), [])

    issues = []

    if selector and not endpoints and service_type != "ExternalName":
        issues.append("missing_endpoints")

    if not selector and service_type == "ClusterIP":
        issues.append("no_selector_defined")

    if not issues:
        return None

    finding = {
        "service": name,
        "namespace": namespace,
        "type": service_type,
        "selector": selector,
        "endpoint_count": len(endpoints),
        "issues": issues,
    }

    if "missing_endpoints" in issues:
        finding["detail"] = (
            "Service has selectors but no ready endpoints — possible selector mismatch "
            "or backing pods are not running."
        )

    if service_type == "ClusterIP" and not endpoints:
        finding["dns_note"] = (
            f"Service {name}.{namespace}.svc.cluster.local may not resolve to any pods."
        )

    return finding


def inspect_network() -> dict:
    """Inspect services and endpoints for networking issues."""
    services_data, services_result = run_kubectl_json(["get", "svc", "-A"])
    endpoints_data, _ = run_kubectl_json(["get", "endpoints", "-A"])

    if services_data is None:
        return {
            "healthy": None,
            "total_services": 0,
            "findings": [],
            "error": services_result.stderr or "Failed to fetch services",
        }

    endpoint_map = _build_endpoint_map(endpoints_data)
    items = services_data.get("items", [])
    findings = []

    for service in items:
        issue = _check_service(service, endpoint_map)
        if issue:
            findings.append(issue)

    return {
        "healthy": len(findings) == 0,
        "total_services": len(items),
        "findings": findings,
    }
