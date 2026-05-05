import sys
import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Make the project root importable so "from routes import ..." works no matter
# from where the user starts the script.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from routes import bugs, runs, simulator, test_cases, traceability  # noqa: E402

app = FastAPI(title="Laser Test Companion", version="1.0")

# Static assets for the SPA — Tailwind and Alpine come from a CDN, the only
# local file is app.js with the Alpine components.
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

# Register every router so the API is reachable under /api/...
app.include_router(test_cases.router)
app.include_router(bugs.router)
app.include_router(runs.router)
app.include_router(traceability.router)
app.include_router(simulator.router)


# Serve the single-page app. The Alpine components inside index.html drive
# the navigation between the five views.
@app.get("/")
def index():
    return FileResponse(str(ROOT / "templates" / "index.html"))


# Tiny helper that opens the browser ~1 second after uvicorn boots —
# saves the user from copy-pasting the URL.
def _open_browser():
    threading.Timer(1.0, lambda: webbrowser.open("http://localhost:8000")).start()


if __name__ == "__main__":
    _open_browser()
    uvicorn.run(app, host="0.0.0.0", port=8000)
