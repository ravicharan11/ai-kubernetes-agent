import subprocess
import json
from pathlib import Path
from typing import List, Dict
from loguru import logger


class ClusterManager:
    """Manages Kubernetes cluster/context discovery from kubeconfig."""

    @staticmethod
    def get_clusters(kubeconfig_path: str) -> List[Dict[str, str]]:
        """Parse kubeconfig and return list of contexts (for switching)."""
        try:
            kubeconfig = Path(kubeconfig_path)
            if not kubeconfig.exists():
                logger.warning(f"Kubeconfig not found at {kubeconfig_path}")
                return []

            # Use kubectl config view to get contexts
            result = subprocess.run(
                ["kubectl", "config", "view", "-o", "json", f"--kubeconfig={kubeconfig_path}"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                logger.error(f"Failed to read kubeconfig: {result.stderr}")
                return []

            config = json.loads(result.stdout)
            contexts = []

            for context in config.get("contexts", []):
                context_name = context.get("name", "Unknown")
                context_info = {
                    "name": context_name,
                    "type": "kubeconfig",
                    "source": "local"
                }
                contexts.append(context_info)

            logger.info(f"Found {len(contexts)} contexts in kubeconfig")
            return contexts

        except subprocess.TimeoutExpired:
            logger.error("kubectl config view timed out")
            return []
        except Exception as e:
            logger.error(f"Error reading kubeconfig: {e}")
            return []

    @staticmethod
    def use_cluster_context(cluster_name: str, kubeconfig_path: str = "") -> bool:
        """Switch to the specified cluster context."""
        try:
            cmd = ["kubectl", "config", "use-context", cluster_name]
            if kubeconfig_path:
                cmd.append(f"--kubeconfig={kubeconfig_path}")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                logger.error(f"Failed to switch context: {result.stderr}")
                return False

            logger.info(f"Switched to cluster context: {cluster_name}")
            return True

        except subprocess.TimeoutExpired:
            logger.error("kubectl use-context timed out")
            return False
        except Exception as e:
            logger.error(f"Error switching context: {e}")
            return False
