import axios from "axios";

const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function fetchHealth() {
  const response = await apiClient.get<{ status: string; service: string }>(
    "/health"
  );
  return response.data;
}

export interface InvestigationResponse {
  status: string;
  investigation: {
    pods: any;
    logs: any;
    events: any;
    deployments: any;
    network: any;
  };
  diagnosis: {
    root_cause: string;
    explanation: string;
    fix: string;
    kubectl_command: string;
    prevention_recommendation: string;
    confidence: number;
    confidence_reasoning: string;
    llm_duration_seconds?: number;
  };
}

export async function investigateCluster(clusterName?: string) {
  const response = await apiClient.post<InvestigationResponse>("/investigate", {
    cluster_name: clusterName,
  });
  return response.data;
}

export interface ClusterInfo {
  name: string;
  type: string;
  source: string;
  cluster?: string;
  user?: string;
  is_current?: boolean;
}

export interface ClustersResponse {
  clusters: ClusterInfo[];
}

export async function getClusters() {
  const response = await apiClient.get<ClustersResponse>("/clusters");
  return response.data;
}
