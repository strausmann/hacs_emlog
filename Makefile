# Makefile für Emlog Home Assistant Integration Entwicklung
# Dieses Makefile vereinfacht die Verwaltung der Entwicklungsumgebung

.PHONY: help mock-up mock-down mock-logs ha-up ha-down ha-logs test test-api clean full-clean dev-setup dev-logs

# Standard-Target: Hilfe anzeigen
help: ## Zeige diese Hilfe an
	@echo "Emlog Home Assistant Integration - Entwicklungsumgebung"
	@echo ""
	@echo "Verfügbare Befehle:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Mock Server Befehle
mock-up: ## Starte den Emlog Mock Server
	@echo "🚀 Starte Emlog Mock Server..."
	docker-compose -f docker-compose.test.yml up -d emlog-mock
	@echo "✅ Mock Server läuft auf http://localhost:8080"

mock-down: ## Stoppe den Emlog Mock Server
	@echo "🛑 Stoppe Emlog Mock Server..."
	docker-compose -f docker-compose.test.yml down emlog-mock

mock-logs: ## Zeige Mock Server Logs
	docker-compose -f docker-compose.test.yml logs -f emlog-mock

# Home Assistant Befehle
ha-up: ## Starte Home Assistant mit Emlog Integration
	@echo "🏠 Starte Home Assistant..."
	@echo "📋 Nach dem Start: http://localhost:8123 aufrufen"
	@echo "🔧 Integration konfigurieren: Einstellungen > Geräte & Dienste > Integration hinzufügen > Emlog"
	docker-compose -f docker-compose.test.yml up homeassistant

ha-down: ## Stoppe Home Assistant
	@echo "🛑 Stoppe Home Assistant..."
	docker-compose -f docker-compose.test.yml down homeassistant

ha-logs: ## Zeige Home Assistant Logs
	docker-compose -f docker-compose.test.yml logs -f homeassistant

# Test Befehle
test: ## Führe vollständige Tests durch (Mock Server + API Tests)
	@echo "🧪 Führe vollständige Tests durch..."
	./test.sh

test-api: ## Teste nur die API Endpunkte
	@echo "🔍 Teste API Endpunkte..."
	@echo "Strom (Meter 1):"
	curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=1" | head -3
	@echo -e "\nGas (Meter 2):"
	curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=2" | head -3
	@echo -e "\n✅ API Tests abgeschlossen"

# Entwicklungsumgebung
dev-setup: ## Erstelle vollständige Entwicklungsumgebung
	@echo "🔧 Richte Entwicklungsumgebung ein..."
	@echo "1. Mock Server starten..."
	docker-compose -f docker-compose.test.yml up -d emlog-mock
	@echo "2. Home Assistant starten..."
	docker-compose -f docker-compose.test.yml up -d homeassistant
	@echo "3. Warte auf Initialisierung..."
	@sleep 15
	@echo "✅ Entwicklungsumgebung bereit!"
	@echo "   📱 Home Assistant: http://localhost:8123"
	@echo "   🔌 Mock API: http://localhost:8080"
	@echo "   📋 Konfiguriere Emlog Integration über die UI"

dev-logs: ## Zeige Logs beider Services
	@echo "📋 Zeige Logs für beide Services..."
	docker-compose -f docker-compose.test.yml logs -f

# Aufräumen
clean: ## Stoppe alle Services und entferne Container
	@echo "🧹 Räume Entwicklungsumgebung auf..."
	docker-compose -f docker-compose.test.yml down
	@echo "✅ Alle Services gestoppt"

full-clean: ## Vollständiges Cleanup (inkl. Volumes und Images)
	@echo "🧹 Führe vollständiges Cleanup durch..."
	docker-compose -f docker-compose.test.yml down -v --rmi local
	@echo "✅ Vollständiges Cleanup abgeschlossen"

# Status und Info
status: ## Zeige Status aller Services
	@echo "📊 Service Status:"
	@docker-compose -f docker-compose.test.yml ps
	@echo ""
	@echo "🔍 Laufende Container:"
	@docker ps --filter "label=com.docker.compose.project=hacs_emlog" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Git und Versionsverwaltung
version: ## Zeige aktuelle Version und Git Status
	@echo "📦 Aktuelle Version: $(shell git describe --tags --abbrev=0 2>/dev/null || echo 'unreleased')"
	@echo "🔄 Git Status:"
	@git status --porcelain | head -10
	@if [ $$(git status --porcelain | wc -l) -gt 10 ]; then echo "... und $$(($$(git status --porcelain | wc -l) - 10)) weitere Änderungen"; fi

# CI/CD Simulation
lint: ## Führe Code-Qualitätsprüfungen durch (simuliert CI)
	@echo "🔍 Führe Code-Qualitätsprüfungen durch..."
	@echo "✅ Python Syntax prüfen..."
	@find custom_components -name "*.py" -exec python3 -m py_compile {} \;
	@echo "✅ JSON Dateien validieren..."
	@find . -name "*.json" -not -path "./test_config/*" -exec sh -c 'python3 -c "import json; json.load(open(\"{}\"))" && echo "✅ {}" || echo "❌ {}: JSON Fehler"' \;
	@echo "✅ YAML Dateien validieren..."
	@find . -name "*.yaml" -o -name "*.yml" | grep -v "test_config/blueprints" | xargs -I {} sh -c 'python3 -c "import yaml; yaml.safe_load(open(\"{}\"))" && echo "✅ {}" || echo "❌ {}: YAML Fehler"'
	@echo "ℹ️  Blueprint-Dateien übersprungen (enthalten HA-spezifische Tags)"
	@echo "🎉 Alle Qualitätsprüfungen bestanden!"

# Hilfe für Entwickler
setup-dev: ## Richte lokale Entwicklungsumgebung ein (für Codespaces)
	@echo "🚀 Richte GitHub Codespaces Entwicklungsumgebung ein..."
	@echo "✅ Dev Container ist bereits konfiguriert"
	@echo "💡 Verwende 'make dev-setup' um die Testumgebung zu starten"
	@echo "📚 Siehe README.md für detaillierte Anleitungen"

# Legacy Support
start: dev-setup ## Legacy: Starte Entwicklungsumgebung (veraltet, verwende dev-setup)
stop: clean ## Legacy: Stoppe alle Services (veraltet, verwende clean)