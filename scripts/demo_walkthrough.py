"""
Automatischer Demo-Walkthrough für den Laser Test Companion.

Was macht dieses Skript?
    Es öffnet einen Browser und klickt selbstständig durch alle 5 Seiten
    der Anwendung. Pausen sind eingebaut, damit ein Bildschirm-Recorder
    (z.B. Peek, ScreenToGif, OBS) sauber mitschneiden kann.

Voraussetzungen:
    1. Server läuft schon (`make run` in einem zweiten Terminal).
    2. Playwright ist installiert (`make gif-deps` einmalig).

Aufruf:
    python scripts/demo_walkthrough.py
    oder einfach:  make demo

Aufnahme-Tipp:
    1. Recorder starten und Browser-Fenster auswählen.
    2. Dieses Skript laufen lassen.
    3. Recorder stoppen, als GIF exportieren nach assets/demo.gif.
"""

import asyncio
import sys

from playwright.async_api import async_playwright

URL = "http://localhost:8000"


# Helper that waits and prints what is happening so you know
# what to focus the recorder on.
async def step(page, message: str, seconds: float = 3.0) -> None:
    print(f"  → {message}")
    await asyncio.sleep(seconds)


async def run_walkthrough() -> None:
    async with async_playwright() as p:
        # Open a real Chromium window so the recorder can capture it
        browser = await p.chromium.launch(
            headless=False,
            args=["--window-size=1440,900", "--window-position=0,0"],
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("\n  ▶ Demo startet — bitte den Recorder laufen lassen.\n")

        # Open the SPA — landing page is the overview view
        await page.goto(URL)
        await page.wait_for_load_state("networkidle")
        await step(page, "Seite 1: Übersicht & Pipeline (Statistikkarten + großes Diagramm)", 6)

        # Page 2 — Test Case Manager
        await page.click("text=Test Case Manager")
        await step(page, "Seite 2: Test Case Manager (4 Testfälle)", 5)
        # Open the detail modal of the first test case for variety
        await page.click("text=Details anzeigen >> nth=0")
        await step(page, "  · Detail-Modal mit Schritten und Squish-Skript", 5)
        await page.keyboard.press("Escape")
        await page.click('button:has-text("×")', timeout=1500) if await page.locator('button:has-text("×")').count() else None
        await asyncio.sleep(1)

        # Page 3 — Squish Simulator (the centerpiece)
        await page.click("text=Squish Simulator")
        await step(page, "Seite 3: Squish Simulator", 3)
        # Run TC-1042 (PASS scenario) — let the live console fill up
        await page.click('button:has-text("Test ausführen")')
        await step(page, "  · Live-Lauf TC-1042 → PASS (animiert, 350 ms pro Schritt)", 7)
        # Switch to TC-1203 and run again to show FAIL + auto-bug
        await page.select_option("select", value="TC-1203")
        await asyncio.sleep(0.5)
        await page.click('button:has-text("Test ausführen")')
        await step(page, "  · Live-Lauf TC-1203 → FAIL + automatischer Bug BUG-887", 7)

        # Page 4 — Bug Tracking
        await page.click("text=Bug Tracking")
        await step(page, "Seite 4: Bug Tracking (Kanban + Workflow + Statistik)", 6)
        # Scroll down so the bug-report form is visible in the recording
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await step(page, "  · Bug-Report-Formular (Beschreibung in Englisch)", 4)
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(1)

        # Page 5 — Traceability & Sprint
        await page.click("text=Traceability")
        await step(page, "Seite 5: Traceability & Sprint", 3)
        await step(page, "  · RTM-Tabelle (Klasse C rot)", 4)
        await page.evaluate("window.scrollBy(0, 400)")
        await step(page, "  · IEC 62304 Lebenszyklus-Kreis (Schritt 7 pulsiert)", 4)
        await page.evaluate("window.scrollBy(0, 400)")
        await step(page, "  · Sprint-14-Backlog + Scrum-Zeitlinie", 5)

        # Back to overview to close the loop visually
        await page.evaluate("window.scrollTo(0, 0)")
        await page.click("text=Übersicht")
        await step(page, "Zurück zur Übersicht — Demo fertig.", 4)

        print("\n  ✓ Walkthrough beendet. Recorder stoppen und als assets/demo.gif speichern.\n")
        await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_walkthrough())
    except Exception as exc:
        print(f"\n  ✗ Fehler: {exc}", file=sys.stderr)
        print("    Hinweis: Läuft der Server? Mach in einem anderen Terminal: make run", file=sys.stderr)
        sys.exit(1)
