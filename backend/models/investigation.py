from pydantic import BaseModel, Field


class InvestigationPayload(BaseModel):
    pods: dict = Field(default_factory=dict)
    logs: dict = Field(default_factory=dict)
    events: dict = Field(default_factory=dict)
    deployments: dict = Field(default_factory=dict)
    network: dict = Field(default_factory=dict)


class DiagnosisPayload(BaseModel):
    root_cause: str = ""
    explanation: str = ""
    fix: str = ""
    kubectl_command: str = ""
    prevention_recommendation: str = ""
    confidence: int = 0
    confidence_reasoning: str = ""
    available: bool = True
    error: str | None = None


class InvestigationResponse(BaseModel):
    status: str
    investigation: InvestigationPayload
    diagnosis: DiagnosisPayload
