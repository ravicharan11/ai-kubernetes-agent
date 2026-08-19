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
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">
        <div className="flex items-center gap-3">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-500 border-t-transparent" />
          <p className="text-sm text-slate-400">Loading clusters...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-6 rounded-xl border border-red-900/50 bg-red-900/20 p-6">
        <p className="text-sm text-red-400">{error}</p>
        <button
          onClick={loadClusters}
          className="mt-3 rounded-lg bg-red-900/30 px-4 py-2 text-sm text-red-300 hover:bg-red-900/40"
        >
          Retry
        </button>
      </div>
    );
  }

  if (clusters.length === 0) {
    return (
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">
        <p className="text-sm text-slate-400">No clusters found. Configure kubeconfig.</p>
      </div>
    );
  }

  return (
    <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/50 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-slate-300">Select Cluster</h3>
          {selectedCluster && (
            <p className="mt-1 text-xs text-slate-500">
              Selected: <span className="text-blue-400">{selectedCluster}</span>
            </p>
          )}
        </div>
        <button
          onClick={loadClusters}
          className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs text-slate-400 hover:bg-slate-700 hover:text-slate-300"
        >
          Refresh
        </button>
      </div>
      
      <div className="mt-4 space-y-2">
        {clusters.map((cluster) => (
          <button
            key={cluster.name}
            onClick={() => onClusterSelect(cluster.name)}
            className={`w-full rounded-xl border p-4 text-left transition-all ${
              selectedCluster === cluster.name
                ? "border-blue-500 bg-gradient-to-r from-blue-900/30 to-blue-800/20 shadow-lg shadow-blue-500/10"
                : "border-slate-700 bg-slate-800/30 hover:border-slate-600 hover:bg-slate-800/50"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {selectedCluster === cluster.name ? (
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500">
                    <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                ) : (
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-700">
                    <svg className="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                )}
                <div>
                  <p className={`font-medium ${selectedCluster === cluster.name ? "text-white" : "text-slate-300"}`}>
                    {cluster.name}
                  </p>
                  <div className="mt-1 flex items-center gap-2">
                    <span className={`rounded-full px-2 py-0.5 text-xs ${
                      selectedCluster === cluster.name 
                        ? "bg-blue-500/20 text-blue-300" 
                        : "bg-slate-700 text-slate-400"
                    }`}>
                      {cluster.type}
                    </span>
                    <span className={`text-xs ${selectedCluster === cluster.name ? "text-blue-300" : "text-slate-500"}`}>
                      {cluster.source}
                    </span>
                  </div>
                </div>
              </div>
              {selectedCluster === cluster.name && (
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-blue-500 px-3 py-1 text-xs font-medium text-white">
                    Active
                  </span>
                </div>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
