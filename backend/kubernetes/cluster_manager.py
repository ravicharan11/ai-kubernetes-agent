import subprocess
import json
from pathlib import Path
from typing import List, Dict
from loguru import logger


class ClusterManager:
    """Manages Kubernetes cluster discovery from kubeconfig and AWS EKS."""

    @staticmethod
    def get_kubeconfig_clusters(kubeconfig_path: str) -> List[Dict[str, str]]:
        """Parse kubeconfig and return list of clusters."""
        try:
            kubeconfig = Path(kubeconfig_path)
            if not kubeconfig.exists():
                logger.warning(f"Kubeconfig not found at {kubeconfig_path}")
                return []

            # Use kubectl config view to get clusters
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
            clusters = []

            for cluster in config.get("clusters", []):
                cluster_name = cluster.get("name", "Unknown")
                cluster_info = {
                    "name": cluster_name,
                    "type": "kubeconfig",
                    "source": "local"
                }
                clusters.append(cluster_info)

            logger.info(f"Found {len(clusters)} clusters in kubeconfig")
            return clusters

        except subprocess.TimeoutExpired:
            logger.error("kubectl config view timed out")
            return []
        except Exception as e:
            logger.error(f"Error reading kubeconfig: {e}")
            return []

    @staticmethod
    def get_eks_clusters() -> List[Dict[str, str]]:
        """Get EKS clusters from AWS CLI."""
        try:
            result = subprocess.run(
                ["aws", "eks", "list-clusters", "--output", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.warning(f"AWS CLI failed: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            cluster_names = data.get("clusters", [])
            clusters = []

            for cluster_name in cluster_names:
                # Get cluster details
                detail_result = subprocess.run(
                    ["aws", "eks", "describe-cluster", "--name", cluster_name, "--output", "json"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                cluster_info = {
                    "name": cluster_name,
                    "type": "eks",
                    "source": "aws",
                    "region": "",
                    "endpoint": ""
                }

                if detail_result.returncode == 0:
                    detail_data = json.loads(detail_result.stdout)
                    cluster_info["region"] = detail_data.get("cluster", {}).get("arn", "").split(":")[3]
                    cluster_info["endpoint"] = detail_data.get("cluster", {}).get("endpoint", "")

                clusters.append(cluster_info)

            logger.info(f"Found {len(clusters)} EKS clusters")
            return clusters

        except subprocess.TimeoutExpired:
            logger.error("AWS CLI command timed out")
            return []
        except FileNotFoundError:
            logger.warning("AWS CLI not found")
            return []
        except Exception as e:
            logger.error(f"Error getting EKS clusters: {e}")
            return []

    @staticmethod
    def get_all_clusters(kubeconfig_path: str = "") -> List[Dict[str, str]]:
        """Get all clusters from both kubeconfig and AWS EKS."""
        clusters = []

        # Get kubeconfig clusters
        if kubeconfig_path:
            kubeconfig_clusters = ClusterManager.get_kubeconfig_clusters(kubeconfig_path)
            clusters.extend(kubeconfig_clusters)

        # Get EKS clusters
        eks_clusters = ClusterManager.get_eks_clusters()
        clusters.extend(eks_clusters)

        # Remove duplicates by name
        seen = set()
        unique_clusters = []
        for cluster in clusters:
            if cluster["name"] not in seen:
                seen.add(cluster["name"])
                unique_clusters.append(cluster)

        return unique_clusters

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
