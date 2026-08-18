from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
from typing import List, Dict, Optional

from ai.reasoning import generate_diagnosis
from core.config import settings
from kubernetes.cluster_manager import ClusterManager
from models.investigation import (
    DiagnosisPayload,
    InvestigationPayload,
    InvestigationResponse,
)
from services.investigation import run_investigation

router = APIRouter(tags=["investigation"])


class ClusterInfo(BaseModel):
    name: str
    type: str
    source: str
    region: Optional[str] = ""
    endpoint: Optional[str] = ""


class ClustersResponse(BaseModel):
    clusters: List[ClusterInfo]


class InvestigateRequest(BaseModel):
    cluster_name: Optional[str] = None


@router.get("/clusters", response_model=ClustersResponse)
def get_clusters() -> ClustersResponse:
    """Get all available Kubernetes clusters from kubeconfig and AWS EKS."""
    try:
        clusters = ClusterManager.get_all_clusters(settings.kubeconfig_path)
        return ClustersResponse(
            clusters=[ClusterInfo(**cluster) for cluster in clusters]
        )
    except Exception as exc:
        logger.exception("Failed to get clusters")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve clusters: {exc}",
        ) from exc


@router.post("/investigate", response_model=InvestigationResponse)
def investigate_cluster(request: InvestigateRequest = InvestigateRequest()) -> InvestigationResponse:
    """
    Investigate the Kubernetes cluster and return evidence plus AI diagnosis.

    Flow:
        Collect Evidence → AI Reasoning → Root Cause → Suggested Fix
    """
    # Switch to specified cluster context if provided
    if request.cluster_name:
        success = ClusterManager.use_cluster_context(request.cluster_name, settings.kubeconfig_path)
        if not success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to switch to cluster context: {request.cluster_name}",
            )
        logger.info(f"Investigating cluster: {request.cluster_name}")

    try:
        investigation_data = run_investigation()
    except Exception as exc:
        logger.exception("Investigation failed with unexpected error")
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {exc}",
        ) from exc

    diagnosis_data = generate_diagnosis(investigation_data)

    has_investigation_errors = any(
        section.get("error")
        for section in investigation_data.values()
        if isinstance(section, dict)
    )
    diagnosis_unavailable = not diagnosis_data.get("available", False)

    if has_investigation_errors and diagnosis_unavailable:
        status = "partial"
    elif has_investigation_errors or diagnosis_unavailable:
        status = "partial"
    else:
        status = "success"

    return InvestigationResponse(
        status=status,
        investigation=InvestigationPayload(**investigation_data),
        diagnosis=DiagnosisPayload(**diagnosis_data),
    )
