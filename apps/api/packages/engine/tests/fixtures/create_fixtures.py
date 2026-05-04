"""Run this script to generate sample.xlsx for engine tests."""
from pathlib import Path
import openpyxl

def create_sample_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"

    # Header row
    ws.append(["id", "name", "score"])

    # Data rows
    ws.append([1, "Alice", 95.5])
    ws.append([2, "Bob", None])   # null in score column
    ws.append([3, "Charlie", 78.0])
    ws.append([1, "Alice", 95.5])  # duplicate of row 1

    out = Path(__file__).parent / "sample.xlsx"
    wb.save(out)
    print(f"Created {out}")

if __name__ == "__main__":
    create_sample_xlsx()
