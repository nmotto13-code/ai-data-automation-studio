"use client";

import type { DataProfile } from "@/types/profile";

interface ProfileSummaryCardsProps {
  profile: DataProfile;
}

interface SummaryCard {
  label: string;
  value: string;
}

export default function ProfileSummaryCards({ profile }: ProfileSummaryCardsProps) {
  const avgNullPct =
    profile.columns.length > 0
      ? profile.columns.reduce((sum, col) => sum + col.null_pct, 0) / profile.columns.length
      : 0;

  const cards: SummaryCard[] = [
    {
      label: "Total Rows",
      value: profile.row_count.toLocaleString(),
    },
    {
      label: "Columns",
      value: String(profile.column_count),
    },
    {
      label: "Duplicate Rows",
      value: profile.duplicate_row_count.toLocaleString(),
    },
    {
      label: "Avg Null Rate",
      value: `${(avgNullPct * 100).toFixed(1)}%`,
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-4"
        >
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
            {card.label}
          </p>
          <p className="text-2xl font-bold text-gray-900">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
