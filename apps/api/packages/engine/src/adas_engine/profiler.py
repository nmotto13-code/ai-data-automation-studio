from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import polars as pl

from adas_engine.exceptions import FileTooLargeError, UnsupportedFormatError
from adas_engine.models.data_profile import ColumnProfile, DataProfile
from adas_engine.readers.csv_reader import CsvReader
from adas_engine.readers.xlsx_reader import XlsxReader

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

# Integer base-type classes (includes unsigned variants)
_INTEGER_BASE_TYPES = (pl.Int8, pl.Int16, pl.Int32, pl.Int64,
                       pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64)

# Float base-type classes
_FLOAT_BASE_TYPES = (pl.Float32, pl.Float64)


def _infer_type(dtype: pl.PolarsDataType) -> Literal["string", "integer", "float", "boolean", "date", "mixed", "unknown"]:
    """Map a Polars dtype to our canonical type literal."""
    # isinstance checks work correctly with Polars dtype hierarchy and aliases
    if isinstance(dtype, _INTEGER_BASE_TYPES):
        return "integer"
    if isinstance(dtype, _FLOAT_BASE_TYPES):
        return "float"
    # pl.Utf8 is an alias for pl.String in Polars v1; both match here
    if isinstance(dtype, pl.String):
        return "string"
    if isinstance(dtype, pl.Boolean):
        return "boolean"
    if isinstance(dtype, (pl.Date, pl.Datetime)):
        return "date"
    if isinstance(dtype, pl.Null):
        return "unknown"
    return "mixed"


def _profile_column(df: pl.DataFrame, col: str) -> ColumnProfile:
    """Compute profile statistics for a single column."""
    series = df[col]
    n_rows = len(df)

    null_count = series.null_count()
    null_pct = null_count / n_rows if n_rows > 0 else 0.0
    distinct_count = series.n_unique()
    sample_values: list = series.drop_nulls().head(5).to_list()
    inferred_type = _infer_type(series.dtype)

    return ColumnProfile(
        name=col,
        inferred_type=inferred_type,
        null_count=null_count,
        null_pct=null_pct,
        distinct_count=distinct_count,
        sample_values=sample_values,
    )


def profile_file(file_path: str | Path, format: Literal["csv", "xlsx"]) -> DataProfile:
    """Profile a CSV or XLSX file.

    Parameters
    ----------
    file_path:
        Path to the file on disk.
    format:
        File format — ``"csv"`` or ``"xlsx"``.

    Raises
    ------
    FileTooLargeError
        If the file exceeds ``MAX_FILE_SIZE_BYTES`` (100 MB).
    UnsupportedFormatError
        If *format* is not ``"csv"`` or ``"xlsx"``.
    """
    path = Path(file_path)

    # 1. Size guard
    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(
            f"{path.name} exceeds the 100 MB limit "
            f"({path.stat().st_size / 1_048_576:.1f} MB)."
        )

    # 2. Dispatch to the appropriate reader
    if format == "csv":
        reader = CsvReader()
    elif format == "xlsx":
        reader = XlsxReader()
    else:
        raise UnsupportedFormatError(
            f"Format {format!r} is not supported. Use 'csv' or 'xlsx'."
        )

    df: pl.DataFrame = reader.read(path)

    # 3. Per-column profiles
    columns = [_profile_column(df, col) for col in df.columns]

    # 4. Duplicate row count — rows that appear more than once
    duplicate_row_count = len(df) - df.unique().shape[0]

    # 5. Assemble and return
    return DataProfile(
        row_count=len(df),
        column_count=len(df.columns),
        duplicate_row_count=duplicate_row_count,
        columns=columns,
        profiled_at=datetime.now(timezone.utc),
    )
