"use client";

import type { ColumnProfile, InferredType } from "@/types/profile";

interface ColumnProfileTableProps {
  columns: ColumnProfile[];
}

const TYPE_BADGE_CLASSES: Record<InferredType, string> = {
  integer: "bg-blue-100 text-blue-800",
  float: "bg-green-100 text-green-800",
  string: "bg-gray-100 text-gray-800",
  boolean: "bg-yellow-100 text-yellow-800",
  date: "bg-purple-100 text-purple-800",
  mixed: "bg-orange-100 text-orange-800",
  unknown: "bg-red-100 text-red-800",
};

function truncate(value: string, maxLen: number): string {
  return value.length > maxLen ? `${value.slice(0, maxLen)}…` : value;
}

function formatSampleValues(samples: unknown[]): string {
  return samples
    .slice(0, 3)
    .map((v) => truncate(String(v), 40))
    .join(", ");
}

export default function ColumnProfileTable({ columns }: ColumnProfileTableProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
      <table className="min-w-full divide-y divide-gray-200 bg-white text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Name
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Type
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Nulls
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Null %
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Distinct
            </th>
            <th
              scope="col"
              className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide"
            >
              Sample Values
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {columns.map((col) => (
            <tr key={col.name} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-3 font-medium text-gray-900 whitespace-nowrap">
                {col.name}
              </td>
              <td className="px-4 py-3 whitespace-nowrap">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${TYPE_BADGE_CLASSES[col.inferred_type]}`}
                >
                  {col.inferred_type}
                </span>
              </td>
              <td className="px-4 py-3 text-right text-gray-700 tabular-nums">
                {col.null_count.toLocaleString()}
              </td>
              <td className="px-4 py-3 text-right text-gray-700 tabular-nums">
                {(col.null_pct * 100).toFixed(1)}%
              </td>
              <td className="px-4 py-3 text-right text-gray-700 tabular-nums">
                {col.distinct_count.toLocaleString()}
              </td>
              <td className="px-4 py-3 text-gray-600 max-w-xs">
                <code className="text-xs bg-gray-50 px-1 py-0.5 rounded">
                  {formatSampleValues(col.sample_values)}
                </code>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
