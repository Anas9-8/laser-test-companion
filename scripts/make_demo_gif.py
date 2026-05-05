"""
Headless GIF-Recorder für den Laser Test Companion.

Macht in einem Rutsch:
  1. Startet uvicorn im Hintergrund (Port 8765, damit Port 8000 frei bleibt).
  2. Öffnet eine headless Chromium-Instanz.
  3. Klickt durch alle 5 Seiten.
  4. Schießt regelmäßig Screenshots.
  5. Baut daraus mit Pillow eine animierte GIF-Datei.

Output:
  assets/demo.gif

Aufruf:
  python scripts/make_demo_gif.py
  (oder einfach:  make gif)
"""

from __future__ import annotations

import io
import socket
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "demo.gif"
PORT = 8765
URL = f"http://localhost:{PORT}"

# Smaller frame size keeps the GIF reasonable. 960x540 lands well under
# the friendly 5 MB threshold that GitHub READMEs render quickly.
WIDTH, HEIGHT = 960, 540
# Frames per second of the final GIF. 4 fps keeps the file small.
FPS = 4
FRAME_DURATION_MS = int(1000 / FPS)
# Number of colors in the adaptive palette — lower is smaller
PALETTE_COLORS = 96


# Wait until the uvicorn worker actually accepts TCP connections
def _wait_for_port(port: int, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(("127.0.0.1", port))
                return
            except OSError:
                time.sleep(0.2)
    raise RuntimeError(f"Server kam auf Port {port} nicht hoch.")


# Capture one screenshot of the current page state and append it to frames
def _capture(page, frames: list[Image.Image]) -> None:
    png_bytes = page.screenshot(type="png")
    img = Image.open(io.BytesIO(png_bytes)).convert("P", palette=Image.ADAPTIVE, colors=PALETTE_COLORS)
    frames.append(img)


# Capture multiple frames over a duration so animations and the live console
# in the Squish simulator are visible in the recording
def _record_seconds(page, frames: list[Image.Image], seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        _capture(page, frames)
        time.sleep(1.0 / FPS)


def _walkthrough(page, frames: list[Image.Image]) -> None:
    # 1. Overview & Pipeline — landing page
    page.goto(URL)
    page.wait_for_load_state("networkidle")
    time.sleep(0.8)
    _record_seconds(page, frames, 3.0)
    # Scroll the big pipeline diagram into view
    page.evaluate("window.scrollBy(0, 400)")
    _record_seconds(page, frames, 2.5)
    page.evaluate("window.scrollBy(0, 600)")
    _record_seconds(page, frames, 2.5)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.4)

    # 2. Test Case Manager
    page.click("text=Test Case Manager")
    time.sleep(0.6)
    _record_seconds(page, frames, 3.5)
    # Open the first test case detail modal so the script preview is visible
    page.locator("button:has-text('Details anzeigen')").first.click()
    _record_seconds(page, frames, 4.0)
    # Close modal: click the × button in the top right of the modal
    page.locator(".modal button").filter(has_text="×").first.click()
    time.sleep(0.4)

    # 3. Squish Simulator — the centerpiece
    page.click("text=Squish Simulator")
    time.sleep(0.6)
    _record_seconds(page, frames, 2.5)
    # Run TC-1042 → PASS, capture the live console animation
    page.click("button:has-text('Test ausführen')")
    _record_seconds(page, frames, 6.0)
    # Use the specific Alpine model attribute to disambiguate from filter-selects
    page.locator('select[x-model="squishSelected"]').select_option("TC-1203")
    time.sleep(0.3)
    page.click("button:has-text('Test ausführen')")
    _record_seconds(page, frames, 6.0)

    # 4. Bug Tracking
    page.click("text=Bug Tracking")
    time.sleep(0.6)
    _record_seconds(page, frames, 3.0)
    page.evaluate("window.scrollBy(0, 500)")
    _record_seconds(page, frames, 2.5)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.3)

    # 5. Traceability & Sprint
    page.click("text=Traceability")
    time.sleep(0.6)
    _record_seconds(page, frames, 3.0)
    page.evaluate("window.scrollBy(0, 500)")
    _record_seconds(page, frames, 3.0)
    page.evaluate("window.scrollBy(0, 500)")
    _record_seconds(page, frames, 3.0)
    page.evaluate("window.scrollTo(0, 0)")

    # Closing shot back on the overview
    page.click("text=Übersicht")
    time.sleep(0.5)
    _record_seconds(page, frames, 2.5)


def main() -> int:
    print("→ Starte uvicorn auf Port", PORT, "...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "127.0.0.1", "--port", str(PORT), "--log-level", "warning"],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_port(PORT)
        print("→ Server läuft. Starte headless Chromium...")

        frames: list[Image.Image] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT})
            page = context.new_page()
            try:
                _walkthrough(page, frames)
            finally:
                browser.close()

        if not frames:
            print("✗ Keine Frames aufgenommen.", file=sys.stderr)
            return 2

        print(f"→ {len(frames)} Frames aufgenommen. Baue GIF...")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        # Pillow's save with append_images writes an animated GIF. optimize+loop
        # keep the file size reasonable for a GitHub README.
        frames[0].save(
            OUTPUT,
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_DURATION_MS,
            loop=0,
            optimize=True,
            disposal=2,
        )
        size_mb = OUTPUT.stat().st_size / (1024 * 1024)
        print(f"✓ Fertig: {OUTPUT.relative_to(ROOT)} ({size_mb:.1f} MB, {len(frames)} Frames)")
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=4)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    sys.exit(main())
