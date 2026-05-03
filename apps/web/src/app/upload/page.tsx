"use client";

import { useState } from "react";
import FileDropzone from "@/components/upload/FileDropzone";
import ProfileSummaryCards from "@/components/profile/ProfileSummaryCards";
import ColumnProfileTable from "@/components/profile/ColumnProfileTable";
import { uploadFile } from "@/lib/api-client";
import type { FileAssetResponse } from "@/types/profile";

type UploadState = "idle" | "uploading" | "profiled" | "error";

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function UploadPage() {
  const [state, setState] = useState<UploadState>("idle");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState<FileAssetResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  async function handleUpload(file: File) {
    setSelectedFile(file);
    setState("uploading");
    try {
      const response = await uploadFile(file);
      setResult(response);
      setState("profiled");
    } catch (err) {
      const message = err instanceof Error ? err.message : "An unexpected error occurred.";
      setErrorMessage(message);
      setState("error");
    }
  }

  function handleReset() {
    setState("idle");
    setSelectedFile(null);
    setResult(null);
    setErrorMessage("");
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload &amp; Profile</h2>
      <p className="text-sm text-gray-500 mb-8">
        Upload a CSV or XLSX file to get an instant data profile and AI transformation suggestions.
      </p>

      {(state === "idle" || state === "uploading") && (
        <FileDropzone
          onUpload={handleUpload}
          isUploading={state === "uploading"}
        />
      )}

      {state === "error" && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 mb-6 flex items-start gap-3">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-red-500 mt-0.5 shrink-0"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm.75-11.25a.75.75 0 0 0-1.5 0v4.5a.75.75 0 0 0 1.5 0v-4.5Zm-.75 7.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"
              clipRule="evenodd"
            />
          </svg>
          <div className="flex-1">
            <p className="text-sm font-medium text-red-800">Upload failed</p>
            <p className="text-sm text-red-700 mt-0.5">{errorMessage}</p>
          </div>
          <button
            type="button"
            onClick={handleReset}
            className="text-sm font-medium text-red-700 hover:text-red-900 underline underline-offset-2 shrink-0"
          >
            Try again
          </button>
        </div>
      )}

      {state === "profiled" && result?.profile && (
        <div className="flex flex-col gap-6">
          {/* File summary line */}
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-3 text-sm text-gray-700">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 text-gray-400 shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.5}
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
                />
              </svg>
              <span className="font-medium">{result.original_filename}</span>
              <span className="text-gray-400" aria-hidden="true">·</span>
              <span className="text-gray-500">{formatBytes(result.size_bytes)}</span>
              <span className="text-gray-400" aria-hidden="true">·</span>
              <span className="text-gray-500 uppercase text-xs tracking-wide">{result.format}</span>
            </div>
            <button
              type="button"
              onClick={handleReset}
              className="text-sm text-gray-500 hover:text-gray-700 underline underline-offset-2"
            >
              Upload another file
            </button>
          </div>

          {/* Summary cards */}
          <ProfileSummaryCards profile={result.profile} />

          {/* Column detail table */}
          <div>
            <h3 className="text-base font-semibold text-gray-900 mb-3">Column Details</h3>
            <ColumnProfileTable columns={result.profile.columns} />
          </div>

          {/* Bottom reset */}
          <div className="pt-2 border-t border-gray-200">
            <button
              type="button"
              onClick={handleReset}
              className="px-6 py-2.5 rounded-lg text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 transition-colors"
            >
              Upload another file
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
