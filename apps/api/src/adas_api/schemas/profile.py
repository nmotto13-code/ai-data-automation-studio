from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ColumnProfileResponse(BaseModel):
    name: str
    inferred_type: str
    null_count: int
    null_pct: float
    distinct_count: int
    sample_values: list[Any]


class DataProfileResponse(BaseModel):
    row_count: int
    column_count: int
    duplicate_row_count: int
    columns: list[ColumnProfileResponse]
    profiled_at: datetime
