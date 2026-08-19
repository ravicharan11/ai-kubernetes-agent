"use client";

import { useEffect, useState } from "react";

interface InvestigationProgressProps {
  isRunning: boolean;
}

const STEPS = [
  { label: "Checking Pods", description: "Inspecting pod status across all namespaces" },
  { label: "Reading Logs", description: "Collecting logs from problematic pods" },
  { label: "Analyzing Events", description: "Reviewing recent cluster events" },
  { label: "Inspecting Deployments", description: "Checking deployment health and replicas" },
  { label: "Checking Networking", description: "Analyzing services and network policies" },
  { label: "AI Reasoning", description: "Processing evidence with AI model", isAI: true },
  { label: "Root Cause Found", description: "Generating diagnosis and recommendations" },
];

export function InvestigationProgress({ isRunning }: InvestigationProgressProps) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!isRunning) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < STEPS.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning]);

  if (!isRunning) return null;

  return (
    <div className="mt-8 rounded-lg border border-slate-800 bg-slate-900/50 p-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Investigation Status</h3>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 animate-pulse rounded-full bg-blue-400" />
          <span className="text-sm text-slate-400">In Progress</span>
        </div>
      </div>
      <div className="mt-4 space-y-3">
        {STEPS.map((step, index) => {
          const isCompleted = index <= currentStep;
          const isCurrent = index === currentStep;

          return (
            <div
              key={step.label}
              className={`rounded-lg border p-3 transition ${
                isCompleted
                  ? "border-green-900/50 bg-green-900/10"
                  : isCurrent
                  ? step.isAI
                  ? "border-purple-500/50 bg-purple-900/10"
                  : "border-blue-900/50 bg-blue-900/10"
                  : "border-slate-800 bg-slate-800/30"
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={`text-lg ${isCompleted ? "text-green-400" : isCurrent ? (step.isAI ? "text-purple-400" : "text-blue-400") : "text-slate-600"}`}>
                  {isCompleted ? "✓" : isCurrent ? (step.isAI ? "🤖" : "→") : "○"}
                </span>
                <div className="flex-1">
                  <p className={`text-sm font-medium ${isCurrent ? "text-white" : "text-slate-400"}`}>
                    {step.label}
                  </p>
                  {isCurrent && (
                    <div className="mt-1">
                      <p className="text-xs text-slate-500">{step.description}</p>
                      {step.isAI && (
                        <div className="mt-2 flex items-center gap-2">
                          <div className="h-2 w-2 animate-pulse rounded-full bg-purple-400" />
                          <span className="text-xs text-purple-300">AI model analyzing evidence...</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
