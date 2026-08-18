import json
import subprocess
from dataclasses import dataclass

from loguru import logger

from core.config import settings


@dataclass
class KubectlResult:
    success: bool
    stdout: str
    stderr: str
    return_code: int
    command: str


def run_kubectl(args: list[str], timeout: int = 60) -> KubectlResult:
    """Execute a kubectl command and return structured output."""
    command_parts = ["kubectl"]

    if settings.kubeconfig_path:
        command_parts.extend(["--kubeconfig", settings.kubeconfig_path])

    command_parts.extend(args)
    command_str = " ".join(command_parts)

    logger.info(f"Running: {command_str}")

    try:
        result = subprocess.run(
            command_parts,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        logger.error("kubectl not found in PATH")
        return KubectlResult(
            success=False,
            stdout="",
            stderr="kubectl not found. Ensure kubectl is installed and in PATH.",
            return_code=127,
            command=command_str,
        )
    except subprocess.TimeoutExpired:
        logger.error(f"kubectl command timed out: {command_str}")
        return KubectlResult(
            success=False,
            stdout="",
            stderr=f"Command timed out after {timeout}s",
            return_code=124,
            command=command_str,
        )

    if result.returncode != 0:
        logger.warning(
            f"kubectl exited with code {result.returncode}: {result.stderr.strip()}"
        )
    else:
        logger.debug(f"kubectl succeeded: {command_str}")

    return KubectlResult(
        success=result.returncode == 0,
        stdout=result.stdout,
        stderr=result.stderr,
        return_code=result.returncode,
        command=command_str,
    )


def run_kubectl_json(args: list[str], timeout: int = 60) -> tuple[dict | list | None, KubectlResult]:
    """Run kubectl with JSON output and parse the response."""
    json_args = [*args, "-o", "json"]
    result = run_kubectl(json_args, timeout=timeout)

    if not result.success or not result.stdout.strip():
        return None, result

    try:
        return json.loads(result.stdout), result
    except json.JSONDecodeError as exc:
        logger.error(f"Failed to parse kubectl JSON output: {exc}")
        result.stderr = f"{result.stderr}\nJSON parse error: {exc}".strip()
        return None, result
