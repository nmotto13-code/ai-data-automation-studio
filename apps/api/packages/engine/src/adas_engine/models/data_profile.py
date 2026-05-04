from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


class ColumnProfile(BaseModel):
    name: str
    inferred_type: Literal["string", "integer", "float", "boolean", "date", "mixed", "unknown"]
    null_count: int
    null_pct: float        # 0.0–1.0
    distinct_count: int
    sample_values: list[Any]   # up to 5 non-null samples


class DataProfile(BaseModel):
    row_count: int
    column_count: int
    duplicate_row_count: int
    columns: list[ColumnProfile]
    profiled_at: datetime
