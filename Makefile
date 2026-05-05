# Laser Test Companion — Makefile
# Einfache Befehle für das ganze Projekt.
# Schreib einfach `make` oder `make help` für die Liste.

PYTHON ?= python3
PIP    ?= $(PYTHON) -m pip
PORT   ?= 8000

.DEFAULT_GOAL := help

# -----------------------------------------------------------------------------
# Hilfe-Anzeige
# -----------------------------------------------------------------------------

.PHONY: help
help: ## Zeige diese Hilfe
	@echo ""
	@echo "  Laser Test Companion — verfügbare Befehle:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Beispiele:"
	@echo "    make install    # Abhängigkeiten installieren"
	@echo "    make run        # UI starten und Browser öffnen"
	@echo "    make test       # alle 16 pytest-Tests laufen"
	@echo ""

# -----------------------------------------------------------------------------
# Installation und Start
# -----------------------------------------------------------------------------

.PHONY: install
install: ## Python-Abhängigkeiten installieren
	$(PIP) install --quiet fastapi uvicorn pydantic python-dateutil pytest httpx
	@echo "✓ Abhängigkeiten installiert."

.PHONY: run
run: ## UI starten und Browser öffnen (http://localhost:8000)
	@echo "→ Starte Server auf http://localhost:$(PORT) ..."
	$(PYTHON) main.py

.PHONY: dev
dev: ## Server mit Auto-Reload starten (für Entwicklung)
	$(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port $(PORT)

.PHONY: open
open: ## Nur den Browser öffnen (Server muss schon laufen)
	@xdg-open http://localhost:$(PORT) 2>/dev/null || \
	 open http://localhost:$(PORT) 2>/dev/null || \
	 echo "Bitte manuell öffnen: http://localhost:$(PORT)"

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

.PHONY: test
test: ## Alle 16 pytest-Tests ausführen
	$(PYTHON) -m pytest tests/ -v

.PHONY: test-quiet
test-quiet: ## Tests ohne -v
	$(PYTHON) -m pytest tests/

.PHONY: smoke
smoke: ## Schneller Smoke-Test der API (ohne Server zu starten)
	@$(PYTHON) -c "import sys; sys.path.insert(0,'.'); \
	from fastapi.testclient import TestClient; from main import app; c = TestClient(app); \
	print('GET /              ->', c.get('/').status_code); \
	print('GET /api/stats     ->', c.get('/api/stats').status_code); \
	print('GET /api/test-cases->', c.get('/api/test-cases').status_code, '('+str(len(c.get('/api/test-cases').json()))+' Testfälle)'); \
	print('GET /api/bugs      ->', c.get('/api/bugs').status_code, '('+str(len(c.get('/api/bugs').json()))+' Bugs)'); \
	print('POST /api/run TC-1042 ->', c.post('/api/run', json={'test_case_id':'TC-1042'}).json()['result']); \
	print('POST /api/run TC-1203 ->', c.post('/api/run', json={'test_case_id':'TC-1203'}).json()['result']); \
	print('✓ Smoke-Test erfolgreich.')"

# -----------------------------------------------------------------------------
# Aufräumen
# -----------------------------------------------------------------------------

.PHONY: clean
clean: ## Cache-Dateien aufräumen (__pycache__, .pytest_cache)
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "✓ Aufgeräumt."

.PHONY: tree
tree: ## Projektstruktur anzeigen
	@find . -type f -not -path '*/__pycache__/*' -not -path '*/.pytest_cache/*' -not -path '*/.git/*' | sort
