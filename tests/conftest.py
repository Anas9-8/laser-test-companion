import sys
from pathlib import Path

# Make the project root importable so tests can do "from routes import ..."
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
