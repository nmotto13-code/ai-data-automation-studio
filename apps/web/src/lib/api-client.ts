import type { FileAssetResponse } from "@/types/profile";

const API_BASE = "/api/v1";

export async function uploadFile(file: File): Promise<FileAssetResponse> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/files/`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(error.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}

export async function getFile(id: string): Promise<FileAssetResponse> {
  const res = await fetch(`${API_BASE}/files/${id}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
