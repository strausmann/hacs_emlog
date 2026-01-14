.PHONY: help mock-up mock-down mock-logs ha-up ha-down ha-logs ha-reload test test-api clean full-clean dev-up dev-down dev-logs lint status version release-dry-run release-notes release release-github

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
	@echo "  make ha-reload             Kopiere Integration & starte HA neu"
	@echo ""
	@echo "Testing & Validierung:"
	@echo "  make test                  Führe Tests durch"
	@echo "  make test-api              Teste Mock API"
	@echo "  make lint                  Code-Qualität prüfen"
	@echo ""
	@echo "Release Management:"
	@echo "  make release-dry-run       Teste Release (ohne zu pushen)"
	@echo "  make release-notes         Zeige generierte Release Notes"
	@echo "  make release               Führe manuellen Release aus (lokal, mit Bestätigung)"
	@echo "  make release-github        Triggere GitHub Actions Release (remote auf GitHub)"
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

ha-reload:
	@echo "🔄 Kopiere Integration ins Test-Verzeichnis..."
	@mkdir -p tests/config/custom_components
	@cp -r custom_components/emlog tests/config/custom_components/
	@echo "✅ Integration kopiert"
	@echo "🔄 Starte Home Assistant neu..."
	@docker restart docker-homeassistant-1 || (echo "⚠️  Container-Name nicht gefunden, versuche mit compose..." && docker-compose -f tools/docker/compose.yml restart homeassistant)
	@sleep 5
	@echo "✅ Home Assistant neugestartet"
	@echo "📊 Prüfe Integration..."
	@docker logs docker-homeassistant-1 2>&1 | grep -i "emlog" | tail -5 || echo "⚠️  Keine Emlog-Logs gefunden"

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

release-dry-run:
	@echo "🚀 Teste Semantic Release (Dry-Run)..."
	@echo ""
	@semantic-release --dry-run 2>&1 | grep -E "✔|✘|The (next|release|Repository)" || true

release-notes:
	@echo "📝 Generierte Release Notes:"
	@echo ""
	@semantic-release --dry-run 2>&1 | grep -A 50 "Release note for version" | head -60

release:
	@echo "🚀 Führe Semantic Release aus..."
	@echo ""
	@echo "⚠️  Dies wird:"
	@echo "   • Commits analysieren"
	@echo "   • Version berechnen"
	@echo "   • CHANGELOG.md aktualisieren"
	@echo "   • Git Tag erstellen"
	@echo "   • GitHub Release veröffentlichen"
	@echo "   • Änderungen zu Git pushen"
	@echo ""
	@read -p "Fortfahren? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		CI=true semantic-release; \
	else \
		echo "Release abgebrochen."; \
	fi

release-github:
	@echo "🚀 Triggere GitHub Actions Release Workflow..."
	@echo ""
	@gh workflow run release.yml --repo strausmann/hacs_emlog && \
	echo "✅ Workflow getriggert!" && \
	echo "" && \
	echo "📊 Workflow Status anzeigen:" && \
	echo "   make status: gh run list --workflow=release.yml --limit 3" && \
	echo "" && \
	echo "🌐 Im Browser öffnen:" && \
	echo "   https://github.com/strausmann/hacs_emlog/actions/workflows/release.yml" || \
	echo "❌ Fehler beim Triggern. Siehe CONTRIBUTING.md für PAT Setup-Anleitung."
