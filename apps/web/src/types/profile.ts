export type InferredType =
  | "string"
  | "integer"
  | "float"
  | "boolean"
  | "date"
  | "mixed"
  | "unknown";

export interface ColumnProfile {
  name: string;
  inferred_type: InferredType;
  null_count: number;
  null_pct: number; // 0.0–1.0
  distinct_count: number;
  sample_values: unknown[];
}

export interface DataProfile {
  row_count: number;
  column_count: number;
  duplicate_row_count: number;
  columns: ColumnProfile[];
  profiled_at: string; // ISO datetime string
}

export interface FileAssetResponse {
  id: string;
  original_filename: string;
  format: string;
  size_bytes: number;
  status: "uploaded" | "profiling" | "profiled" | "error";
  profile: DataProfile | null;
  error_message: string | null;
  created_at: string;
}
