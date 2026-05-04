import subprocess
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def pytest_configure(config):
    """Auto-generate sample.xlsx fixture if it does not exist."""
    xlsx_path = FIXTURES_DIR / "sample.xlsx"
    if not xlsx_path.exists():
        script = FIXTURES_DIR / "create_fixtures.py"
        subprocess.run(
            ["python", str(script)],
            check=True,
            cwd=str(FIXTURES_DIR),
        )
