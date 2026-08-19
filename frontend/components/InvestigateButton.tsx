"use client";

interface InvestigateButtonProps {
  onInvestigate: () => void;
  disabled?: boolean;
}

export function InvestigateButton({ onInvestigate, disabled }: InvestigateButtonProps) {
  return (
    <button
      type="button"
      onClick={onInvestigate}
      disabled={disabled}
      className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-400 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-slate-900"
    >
      {disabled ? "Investigating..." : "Investigate"}
    </button>
  );
}
