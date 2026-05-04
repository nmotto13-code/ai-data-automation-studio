from pathlib import Path

import polars as pl

from adas_engine.readers.base import FileReader


class CsvReader(FileReader):
    def read(self, path: Path) -> pl.DataFrame:
        """Read a CSV file, trying UTF-8 first then falling back to latin-1."""
        try:
            return pl.read_csv(path, infer_schema_length=1000, ignore_errors=True)
        except UnicodeDecodeError:
            return pl.read_csv(
                path,
                infer_schema_length=1000,
                ignore_errors=True,
                encoding="latin-1",
            )
