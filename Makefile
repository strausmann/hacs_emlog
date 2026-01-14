.PHONY: help mock-up mock-down mock-logs ha-up ha-down ha-logs test test-api clean full-clean dev-up dev-down dev-logs lint status version

help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║  Emlog HA Integration - Entwicklungsumgebung               ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📚 REPOSITORY STRUKTUR:"
	@echo "  custom_components/emlog/   → HACS Integration"
	@echo "  docs/                      → Dokumentation"
	@echo "  tools/                     → Entwicklungswerkzeuge"
	@echo "  tests/                     → Tests & Mock Server"
	@echo ""
	@echo "🚀 VERFÜGBARE BEFEHLE:"
	@echo ""
	@echo "Dev-Umgebung:"
	@echo "  make dev-up                Starte komplette Dev-Umgebung"
	@echo "  make dev-down              Stoppe Dev-Umgebung"
	@echo "  make dev-logs              Zeige alle Logs"
	@echo ""
	@echo "Einzelne Services:"
	@echo "  make mock-up               Starte Mock Server"
	@echo "  make mock-down             Stoppe Mock Server"
	@echo "  make mock-logs             Mock Server Logs"
	@echo "  make ha-up                 Starte Home Assistant"
	@echo "  make ha-down               Stoppe Home Assistant"
	@echo "  make ha-logs               Home Assistant Logs"
	@echo ""
	@echo "Testing & Validierung:"
	@echo "  make test                  Führe Tests durch"
	@echo "  make test-api              Teste Mock API"
	@echo "  make lint                  Code-Qualität prüfen"
	@echo ""
	@echo "Wartung:"
	@echo "  make status                Service Status"
	@echo "  make clean                 Cleanup (down)"
	@echo "  make full-clean            Vollständiges Cleanup"
	@echo "  make version               Zeige Version"

mock-up:
	@echo "🚀 Starte Mock Server..."
	docker-compose -f tools/docker/compose.yml up -d emlog-mock
	@sleep 2 && echo "✅ http://localhost:8080"

mock-down:
	docker-compose -f tools/docker/compose.yml down emlog-mock

mock-logs:
	docker-compose -f tools/docker/compose.yml logs -f emlog-mock

ha-up: update-ha-config
	@echo "🏠 Home Assistant starten..."
	docker-compose -f tools/docker/compose.yml up homeassistant

ha-down:
	docker-compose -f tools/docker/compose.yml down homeassistant

ha-logs:
	docker-compose -f tools/docker/compose.yml logs -f homeassistant

update-ha-config:
	@python3 tools/scripts/update_ha_config.py

dev-up: update-ha-config
	@echo "🚀 Starte Dev-Umgebung..."
	docker-compose -f tools/docker/compose.yml up -d
	@sleep 3 && echo "✅ HA: http://localhost:8123"

dev-down:
	docker-compose -f tools/docker/compose.yml down

dev-logs:
	docker-compose -f tools/docker/compose.yml logs -f

test:
	@bash tools/scripts/test.sh

test-api:
	@echo "🔍 Teste Mock API..."
	@curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=1" | python3 -m json.tool | head -15

lint:
	@echo "🔍 Prüfe Code..."
	@find custom_components -name "*.py" -exec python3 -m py_compile {} \; && echo "✅ Python OK"

clean:
	@echo "🧹 Cleanup..."
	docker-compose -f tools/docker/compose.yml down

full-clean: clean
	docker-compose -f tools/docker/compose.yml down -v --rmi local 2>/dev/null || true
	rm -rf tests/config/.storage tests/config/*.db*

status:
	docker-compose -f tools/docker/compose.yml ps

version:
	@echo "Version: $$(git describe --tags --abbrev=0 2>/dev/null || echo 'unreleased')"
	@git status --short | head -5
