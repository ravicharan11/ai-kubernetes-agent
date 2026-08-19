"use client";

interface Diagnosis {
  root_cause: string;
  explanation: string;
  fix: string;
  kubectl_command: string;
  prevention_recommendation: string;
  confidence: number;
  confidence_reasoning: string;
  llm_duration_seconds?: number;
}

interface RootCauseCardProps {
  diagnosis: Diagnosis | null;
  isHealthy?: boolean;
}

export function RootCauseCard({ diagnosis, isHealthy = false }: RootCauseCardProps) {
  if (isHealthy) {
    return (
      <div className="mt-8 rounded-lg border border-green-900/50 bg-green-900/20 p-6">
        <div className="flex items-center justify-center gap-3">
          <span className="text-4xl">✓</span>
          <div className="text-left">
            <h3 className="text-lg font-semibold text-green-400">Cluster is Healthy</h3>
            <p className="mt-1 text-sm text-green-300">
              No critical Kubernetes issues detected. Your cluster appears to be running normally.
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!diagnosis) return null;

  const confidenceColor = diagnosis.confidence >= 80 ? "text-green-400" : 
                          diagnosis.confidence >= 60 ? "text-yellow-400" : "text-red-400";

  return (
    <div className="mt-8 rounded-lg border border-slate-800 bg-slate-900/50 p-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Diagnosis</h3>
        {diagnosis.llm_duration_seconds && (
          <div className="flex items-center gap-2 rounded-lg bg-purple-900/20 px-3 py-1.5 border border-purple-500/30">
            <span className="text-lg">🤖</span>
            <span className="text-sm text-purple-300">
              AI: {diagnosis.llm_duration_seconds}s
            </span>
          </div>
        )}
      </div>
      
      <div className="mt-4 space-y-4">
        <div>
          <h4 className="text-sm font-medium text-slate-400">Root Cause</h4>
          <p className="mt-1 text-white">{diagnosis.root_cause}</p>
        </div>

        <div>
          <h4 className="text-sm font-medium text-slate-400">Explanation</h4>
          <p className="mt-1 text-white">{diagnosis.explanation}</p>
        </div>

        <div>
          <h4 className="text-sm font-medium text-slate-400">Suggested Fix</h4>
          <p className="mt-1 text-white">{diagnosis.fix}</p>
        </div>

        <div>
          <h4 className="text-sm font-medium text-slate-400">Command</h4>
          <code className="mt-1 block rounded bg-slate-800 p-3 text-sm text-green-400">
            {diagnosis.kubectl_command}
          </code>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-medium text-slate-400">Confidence</h4>
            <p className={`mt-1 text-2xl font-bold ${confidenceColor}`}>
              {diagnosis.confidence}%
            </p>
          </div>
          <div className="text-right">
            <h4 className="text-sm font-medium text-slate-400">Prevention</h4>
            <p className="mt-1 text-sm text-white">{diagnosis.prevention_recommendation}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
