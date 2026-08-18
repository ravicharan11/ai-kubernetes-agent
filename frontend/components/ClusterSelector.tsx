"use client";

import { useEffect, useState } from "react";
import { getClusters, type ClusterInfo } from "@/services/api";

interface ClusterSelectorProps {
  selectedCluster: string | null;
  onClusterSelect: (clusterName: string) => void;
}

export function ClusterSelector({ selectedCluster, onClusterSelect }: ClusterSelectorProps) {
  const [clusters, setClusters] = useState<ClusterInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadClusters();
  }, []);

  const loadClusters = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getClusters();
      setClusters(data.clusters);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load clusters");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/50 p-4">
        <p className="text-sm text-slate-400">Loading clusters...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-4 rounded-lg border border-red-900/50 bg-red-900/20 p-4">
        <p className="text-sm text-red-400">{error}</p>
        <button
          onClick={loadClusters}
          className="mt-2 text-sm text-red-300 hover:text-red-200"
        >
          Retry
        </button>
      </div>
    );
  }

  if (clusters.length === 0) {
    return (
      <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/50 p-4">
        <p className="text-sm text-slate-400">No clusters found. Configure kubeconfig or AWS CLI.</p>
      </div>
    );
  }

  return (
    <div className="mt-4 rounded-lg border border-slate-800 bg-slate-900/50 p-4">
      <h3 className="text-sm font-medium text-slate-300">Select Cluster</h3>
      <div className="mt-3 space-y-2">
        {clusters.map((cluster) => (
          <button
            key={cluster.name}
            onClick={() => onClusterSelect(cluster.name)}
            className={`w-full rounded border p-3 text-left transition ${
              selectedCluster === cluster.name
                ? "border-blue-500 bg-blue-900/20 text-white"
                : "border-slate-700 bg-slate-800/50 text-slate-300 hover:border-slate-600 hover:bg-slate-800"
            }`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">{cluster.name}</p>
                <div className="mt-1 flex items-center gap-2 text-xs text-slate-400">
                  <span className="rounded bg-slate-700 px-2 py-0.5">{cluster.type}</span>
                  {cluster.region && <span>{cluster.region}</span>}
                </div>
              </div>
              {selectedCluster === cluster.name && (
                <span className="text-blue-400">✓</span>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
