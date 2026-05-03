from abc import ABC, abstractmethod
from pathlib import Path

import polars as pl


class FileReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> pl.DataFrame: ...
