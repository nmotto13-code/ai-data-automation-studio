"""
Smoke test: verifies adas_engine can profile a CSV without any running services.
Run with: pytest tests/ from the repo root (after installing adas-engine).
"""
from pathlib import Path
import sys

# Allow running from repo root without installing the package
ENGINE_SRC = Path(__file__).parent.parent / "packages" / "engine" / "src"
if ENGINE_SRC.exists() and str(ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(ENGINE_SRC))

from adas_engine import profile_file

SAMPLE_CSV = Path(__file__).parent.parent / "packages" / "engine" / "tests" / "fixtures" / "sample.csv"


def test_engine_profiles_sample_csv():
    assert SAMPLE_CSV.exists(), f"Fixture not found: {SAMPLE_CSV}"
    profile = profile_file(SAMPLE_CSV, "csv")
    assert profile.row_count == 5
    assert profile.column_count == 3
    assert profile.duplicate_row_count == 1
    assert len(profile.columns) == 3
    column_names = [c.name for c in profile.columns]
    assert "id" in column_names
    assert "name" in column_names
    assert "value" in column_names


def test_engine_null_detection():
    profile = profile_file(SAMPLE_CSV, "csv")
    value_col = next(c for c in profile.columns if c.name == "value")
    assert value_col.null_count == 1
    assert 0.0 < value_col.null_pct < 1.0


def test_engine_type_inference():
    profile = profile_file(SAMPLE_CSV, "csv")
    col_map = {c.name: c for c in profile.columns}
    assert col_map["id"].inferred_type == "integer"
    assert col_map["name"].inferred_type == "string"
    assert col_map["value"].inferred_type == "float"
