"use client";

import { useHealthCheck } from "@/hooks/useHealthCheck";

export function SystemStatus() {
  const { data, isLoading, isError } = useHealthCheck();

  let statusText = "Checking...";
  let statusColor = "text-slate-400";

  if (isLoading) {
    statusText = "Checking...";
    statusColor = "text-slate-400";
  } else if (isError) {
    statusText = "Unavailable";
    statusColor = "text-red-400";
  } else if (data?.status === "healthy") {
    statusText = "Ready";
    statusColor = "text-emerald-400";
  } else {
    statusText = "Unknown";
    statusColor = "text-amber-400";
  }

  return (
    <p className="text-sm text-slate-400">
      System Status:{" "}
      <span className={`font-medium ${statusColor}`}>{statusText}</span>
    </p>
  );
}
