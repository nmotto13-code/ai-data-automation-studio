from pathlib import Path

import polars as pl

from adas_engine.readers.base import FileReader


class XlsxReader(FileReader):
    def read(self, path: Path) -> pl.DataFrame:
        """Read the first sheet of an XLSX file."""
        return pl.read_excel(path, sheet_id=1)
