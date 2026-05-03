from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from adas_engine import FileTooLargeError, UnsupportedFormatError, profile_file
from adas_engine.profiler import MAX_FILE_SIZE_BYTES

FIXTURES = Path(__file__).parent / "fixtures"
CSV_PATH = FIXTURES / "sample.csv"
XLSX_PATH = FIXTURES / "sample.xlsx"


# ---------------------------------------------------------------------------
# CSV tests
# ---------------------------------------------------------------------------


def test_csv_row_count():
    profile = profile_file(CSV_PATH, "csv")
    assert profile.row_count == 5


def test_csv_column_count():
    profile = profile_file(CSV_PATH, "csv")
    assert profile.column_count == 3


def test_csv_null_detection():
    profile = profile_file(CSV_PATH, "csv")
    value_col = next(c for c in profile.columns if c.name == "value")
    assert value_col.null_count == 1


def test_csv_type_inference():
    profile = profile_file(CSV_PATH, "csv")
    col_map = {c.name: c for c in profile.columns}

    assert col_map["id"].inferred_type == "integer"
    assert col_map["name"].inferred_type == "string"
    assert col_map["value"].inferred_type == "float"


def test_csv_duplicate_count():
    profile = profile_file(CSV_PATH, "csv")
    assert profile.duplicate_row_count == 1


def test_csv_sample_values_populated():
    profile = profile_file(CSV_PATH, "csv")
    for col in profile.columns:
        assert len(col.sample_values) >= 1, (
            f"Column {col.name!r} has no sample values"
        )


# ---------------------------------------------------------------------------
# XLSX tests
# ---------------------------------------------------------------------------


def test_xlsx_profile():
    profile = profile_file(XLSX_PATH, "xlsx")
    assert profile is not None
    assert profile.row_count >= 1
    assert profile.column_count >= 1


# ---------------------------------------------------------------------------
# Error-path tests
# ---------------------------------------------------------------------------


def test_file_too_large():
    stat_result = MagicMock()
    stat_result.st_size = MAX_FILE_SIZE_BYTES + 1

    with patch("adas_engine.profiler.Path.stat", return_value=stat_result):
        with pytest.raises(FileTooLargeError):
            profile_file(CSV_PATH, "csv")


def test_unsupported_format():
    with pytest.raises(UnsupportedFormatError):
        profile_file(CSV_PATH, "json")  # type: ignore[arg-type]
