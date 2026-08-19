"use client";

import { useEffect, useState } from "react";

interface HistoryItem {
  id: string;
  timestamp: string;
  rootCause: string;
  confidence: number;
  status: string;
}

const STORAGE_KEY = "investigation_history";

export function addToInvestigationHistory(item: HistoryItem) {
  const stored = localStorage.getItem(STORAGE_KEY);
  const history: HistoryItem[] = stored ? JSON.parse(stored) : [];
  const updated = [item, ...history].slice(0, 10);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
}

export function InvestigationHistory() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [hiddenIds, setHiddenIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setHistory(JSON.parse(stored));
    }
  }, []);

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const hideItem = (id: string) => {
    setHiddenIds((prev) => new Set(prev).add(id));
  };

  const visibleHistory = history.filter((item) => !hiddenIds.has(item.id));

  if (visibleHistory.length === 0) {
    return null;
  }

  return (
    <div className="mt-8 rounded-lg border border-slate-800 bg-slate-900/50 p-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Recent Investigations</h3>
        <button
          onClick={clearHistory}
          className="text-sm text-slate-400 hover:text-white"
        >
          Clear
        </button>
      </div>
      
      <div className="mt-4 space-y-2">
        {visibleHistory.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between rounded border border-slate-800 bg-slate-800/50 p-3"
          >
            <div className="flex-1">
              <p className="text-sm font-medium text-white">{item.rootCause}</p>
              <p className="text-xs text-slate-400">{new Date(item.timestamp).toLocaleString()}</p>
            </div>
            <div className="ml-4 flex items-center gap-3">
              <span
                className={`inline-block rounded px-2 py-1 text-xs font-medium ${
                  item.confidence >= 80
                    ? "bg-green-900/50 text-green-400"
                    : item.confidence >= 60
                    ? "bg-yellow-900/50 text-yellow-400"
                    : "bg-red-900/50 text-red-400"
                }`}
              >
                {item.confidence}%
              </span>
              <button
                onClick={() => hideItem(item.id)}
                className="rounded p-1 text-slate-400 hover:text-red-400 hover:bg-red-900/20 transition"
                title="Hide from view"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
