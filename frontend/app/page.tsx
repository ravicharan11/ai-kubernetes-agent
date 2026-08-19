"use client";

import { useState } from "react";
import { InvestigateButton } from "@/components/InvestigateButton";
import { InvestigationProgress } from "@/components/InvestigationProgress";
import { RootCauseCard } from "@/components/RootCauseCard";
import { InvestigationHistory } from "@/components/InvestigationHistory";
import { ClusterSelector } from "@/components/ClusterSelector";
import { investigateCluster, type InvestigationResponse } from "@/services/api";
import { addToInvestigationHistory } from "@/components/InvestigationHistory";

export default function HomePage() {
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [diagnosis, setDiagnosis] = useState<InvestigationResponse["diagnosis"] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedCluster, setSelectedCluster] = useState<string | null>(null);

  const handleInvestigate = async () => {
    setIsInvestigating(true);
    setDiagnosis(null);
    setError(null);

    try {
      const result = await investigateCluster(selectedCluster || undefined);
      setDiagnosis(result.diagnosis);

      // Add to history only if there were issues
      if (result.diagnosis.root_cause !== "No issues detected") {
        addToInvestigationHistory({
          id: Date.now().toString(),
          timestamp: new Date().toISOString(),
          rootCause: result.diagnosis.root_cause,
          confidence: result.diagnosis.confidence,
          status: "completed",
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Investigation failed");
    } finally {
      setIsInvestigating(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-900/50 p-10 text-center shadow-xl">
        <h1 className="text-3xl font-bold tracking-tight text-white">
          AI Kubernetes Agent
        </h1>
        <p className="mt-3 text-slate-400">
          Troubleshoot Kubernetes with AI
        </p>

        <ClusterSelector 
          selectedCluster={selectedCluster}
          onClusterSelect={setSelectedCluster}
        />

        <div className="mt-8">
          <InvestigateButton 
            onInvestigate={handleInvestigate}
            disabled={isInvestigating || !selectedCluster}
          />
        </div>

        {error && (
          <div className="mt-6 rounded-lg border border-red-900/50 bg-red-900/20 p-4 text-red-400">
            {error}
          </div>
        )}

        <InvestigationProgress isRunning={isInvestigating} />

        <RootCauseCard 
          diagnosis={diagnosis} 
          isHealthy={diagnosis?.root_cause === "No issues detected"}
        />

        <div className="mt-8 border-t border-slate-800 pt-6">
          <InvestigationHistory />
        </div>
      </div>
    </main>
  );
}
