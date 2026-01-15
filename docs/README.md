# 📚 Dokumentation - Emlog Home Assistant Integration

Willkommen zur Dokumentation der Emlog HACS Integration. Diese Seite bietet einen Überblick über alle verfügbaren Ressourcen.

## 📖 Dokumentationsbereiche

### 🚀 [Guides](./guides/)

Praktische Anleitungen für Anfänger und Entwickler:

- **[Getting Started](./guides/README.md)** - Erste Schritte mit der Integration
- **[Codespaces Setup](./guides/README-Codespaces.md)** - Development in GitHub Codespaces
- **[Zugriff & Konfiguration](./guides/CODESPACES-ACCESS.md)** - Konfigurationsübersicht

### 🏗️ [Architektur](./architecture/)

Technische Dokumentation und Design-Entscheidungen:

- Systemarchitektur und Datenfluss
- Komponenten-Übersicht
- API-Integration mit Emlog Geräten

### 🔌 [API-Referenz](./api/)

Vollständige API-Dokumentation:

- Emlog API Endpoints
- Request/Response Beispiele
- Mock-Server Simulation

## 📁 Repository-Struktur

```
hacs_emlog/
├── custom_components/emlog/     # HACS Integration (Produktion)
│   ├── __init__.py
│   ├── config_flow.py             # Konfigurations-UI
│   ├── coordinator.py             # Daten-Polling
│   ├── sensor.py                  # Sensor-Entities
│   ├── const.py                   # Konstanten
│   ├── manifest.json              # Integration-Metadaten
│   └── translations/              # Mehrsprachigkeit
│
├── package/
│   └── emlog.yaml                 # Legacy YAML Package
│
├── docs/                          # Dokumentation
│   ├── guides/                    # Getting Started & Setup
│   ├── architecture/              # Technische Architektur
│   └── api/                       # API Referenz
│
├── tools/                         # Entwicklungswerkzeuge
│   ├── scripts/                   # Test & Setup Scripts
│   └── helpers/                   # Helper-Module
│
├── tests/                         # Tests & Mock
│   ├── mock/                      # Mock Server
│   │   ├── mock_server.py         # Flask API Server
│   │   ├── mock_data/             # Test-Daten
│   │   └── Dockerfile            # Container-Definition
│   └── config/                    # HA Test-Konfiguration
│       ├── configuration.yaml     # HA Config
│       ├── secrets.yaml           # Test-Secrets
│       └── ui-lovelace.yaml       # Dashboard
│
└── .github/                       # GitHub-spezifisch
    ├── workflows/                 # CI/CD Actions
    └── copilot-instructions.md    # AI Coding Guidelines
```

## 🛠️ Entwicklung

Für Entwicklung und Testing stehen diese Tools bereit:

### Quick Start

```bash
# Dev-Umgebung starten
make dev-up

# Logs anschauen
make dev-logs

# Mock API testen
make test-api

# Cleanup
make dev-down
```

### Verfügbare Make-Targets

```bash
make help              # Zeige alle Befehle
make mock-up           # Nur Mock Server
make ha-up             # Nur Home Assistant
make test              # Integrationstests
make lint              # Code-Qualität prüfen
```

## 📝 Sicherheit

- **[Security Policy](../SECURITY.md)** - Vulnerability Reporting
- **[Dependabot Config](./.github/dependabot.yml)** - Automatische Dependency-Updates (npm, GitHub Actions, Docker)
- **[Security Advisories](../SECURITY.md#known-vulnerabilities)** - Bekannte Schwachstellen

## 📋 Contributing

Wenn du zum Projekt beitragen möchtest:

1. Lies [CONTRIBUTING.md](./guides/CONTRIBUTING.md)
2. Befolge das [Commit Format](./guides/CONTRIBUTING.md#commit-format)
3. Starte mit `make dev-up` zur Entwicklung
4. Schreibe Tests für neue Features
5. Öffne einen Pull Request

## 🚀 Releases

Diese Integration verwendet **Semantic Release** für automatisierte Versionierung:

- Commits werden automatisch analysiert
- Version und CHANGELOG werden automatisch generiert
- Tags werden erstellt und Releases auf GitHub veröffentlicht

Siehe [.releaserc.json](../.releaserc.json) für Konfiguration.

## 🔗 Nützliche Links

- [GitHub Repository](https://github.com/strausmann/hacs_emlog)
- [Issue Tracker](https://github.com/strausmann/hacs_emlog/issues)
- [Home Assistant Docs](https://developers.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [Emlog Homepage](https://www.emlog.de/)

## 📧 Support

- 💬 GitHub Discussions für Fragen
- 🐛 GitHub Issues für Bug Reports
- 📖 Siehe [FAQ](./guides/FAQ.md) (in Arbeit)

---

**Zuletzt aktualisiert:** 2025-01-15  
**Version:** 0.1.0  
**Status:** Aktive Entwicklung
