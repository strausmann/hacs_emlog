# Emlog (Electronic Meter Log) – Home Assistant Integration (HACS)

Diese Integration liest Daten aus dem Emlog-Endpoint (z. B. `getinformation.php?export&meterindex=...`).

## 📚 Dokumentation

Ausführliche Dokumentation findest du unter [docs/](docs/):

- **[Getting Started](docs/guides/)** - Installation und erste Schritte
- **[Architektur](docs/architecture/)** - Technisches Design und Systemübersicht
- **[API Referenz](docs/api/)** - Emlog API und Datenstrukturen
- **[Entwicklung](docs/guides/README-Codespaces.md)** - Setup für Entwicklung

## ⚡ Schnellstart

### Installation (HACS)

1. HACS → Integrationen → Menü (⋮) → **Custom Repositories**
2. Repo-URL eintragen: `https://github.com/strausmann/hacs_emlog`
3. Kategorie: **Integration**
4. Installieren → Home Assistant neu starten
5. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → **Emlog**

### Konfiguration

Im UI-Setup eingeben:
- **Host**: IP-Adresse des Emlog Geräts (z.B. 192.168.1.100)
- **Strom Meterindex**: Normalerweise `1`
- **Gas Meterindex**: Normalerweise `2`
- **Scan-Intervall**: Polling-Frequenz in Sekunden (Default: 30)

## 📊 Verfügbare Sensoren

### Strom (Electricity)
- Zählerstand (kWh)
- Tarif 1 & 2 Zählerstände
- Aktuelle Leistung (W)
- Tagesverbrauch (kWh)

### Gas (Gas)
- Zählerstand (m³)
- Aktuelle Leistung (W)
- Tagesverbrauch (kWh)

Siehe [docs/api/](docs/api/) für vollständige Sensor-Liste.

## 🛠️ Entwicklung

### Entwicklungsumgebung starten

Mit Make-Befehlen:

```bash
# Alle verfügbaren Befehle anzeigen
make help

# Vollständige Entwicklungsumgebung starten
make dev-up

# Home Assistant unter http://localhost:8123 öffnen
# Mock Server unter http://localhost:8080 erreichbar

# Tests durchführen
make test              # Vollständige Tests
make test-api          # Nur API Tests
make lint              # Code-Qualität prüfen

# Cleanup
make dev-down          # Stoppe alle Services
make full-clean        # Vollständiges Cleanup mit Volumes
```

### Repository-Struktur

```
hacs_emlog/
├── custom_components/emlog/    # HACS Integration (Produktion)
│   ├── coordinator.py          # Daten-Polling
│   ├── sensor.py               # Sensor-Entities
│   ├── config_flow.py          # Konfigurations-UI
│   └── manifest.json           # Integration-Metadaten
│
├── docs/                       # 📚 Dokumentation
│   ├── guides/                 # Getting Started & Setup
│   ├── architecture/           # Technisches Design
│   ├── api/                    # API Referenz
│   └── README.md              # Dokumentations-Übersicht
│
├── tools/                      # 🛠️ Entwicklungswerkzeuge
│   └── scripts/                # Test & Setup Scripts
│
├── tests/                      # 🧪 Tests & Mock
│   ├── mock/                   # Flask Mock Server
│   └── config/                 # HA Test-Konfiguration
│
├── package/
│   └── emlog.yaml             # Legacy YAML Package
│
└── Makefile                    # Development Task Runner
```

### Lokale Entwicklungsumgebung

Das Projekt enthält eine vollständige Entwicklungsumgebung:

- **Dev Container**: Vollständige Python/Home Assistant Umgebung
- **Mock Server**: Simuliert Emlog API ohne echte Hardware ([tests/mock/](tests/mock/))
- **Test Scripts**: Automatisierte Tests für API und Integration ([tools/scripts/](tools/scripts/))

### Mit Mock Server testen

Für Tests ohne echte Hardware:

```bash
# Dev-Umgebung mit Mock Server starten
make dev-up

# Dann im Browser öffnen:
# Home Assistant: http://localhost:8123
# Mock API: http://localhost:8080
```

Integration konfigurieren:
- **Host**: `emlog-mock`
- **Strom Meterindex**: `1`
- **Gas Meterindex**: `2`
- **Scan-Intervall**: `30`

### Mit echter Emlog Hardware

Bei echter Hardware:
1. Stelle sicher, dass der Emlog Server im gleichen Netzwerk erreichbar ist
2. Verwende die echte IP-Adresse in der Konfiguration
3. Bei Bedarf Tailscale oder VPN für Remote-Zugriff einrichten

## Releases & Versionierung

Dieses Projekt verwendet [Semantic Release](https://semantic-release.gitbook.io/) für automatisierte Versionierung und Releases:

- **Automatische Releases**: Bei jedem Push zu `main` wird automatisch ein neues Release erstellt
- **Conventional Commits**: Bitte verwenden Sie [Conventional Commits](https://www.conventionalcommits.org/) Format
- **Versionierung**: Semantic Versioning (MAJOR.MINOR.PATCH) basierend auf Commit-Typen:
  - `feat:` → Minor-Version erhöhen
  - `fix:` → Patch-Version erhöhen
  - `BREAKING CHANGE:` → Major-Version erhöhen

### Interaktive Commits
Verwenden Sie `npm run commit` für eine interaktive Commit-Erstellung mit deutschen Prompts:

```bash
npm run commit
```

Dies führt Sie durch:
- Auswahl des Commit-Typs (feat, fix, docs, etc.)
- Scope der Änderung
- Betreff und Beschreibung
- Breaking Changes
- Issue-Referenzen

### Code-Formatierung
Das Projekt verwendet **Prettier** für konsistente Code-Formatierung:

```bash
npm run prettier      # Überprüfen der Formatierung
npm run prettier-fix  # Automatische Formatierung
```

### Commitlint
Alle Commits werden automatisch auf Conventional Commits Format validiert.

### Changelog
Alle Änderungen werden automatisch in der [CHANGELOG.md](CHANGELOG.md) dokumentiert.

## Contributing

Möchten Sie zur Weiterentwicklung beitragen? Schauen Sie sich unsere [Contributing Guidelines](docs/guides/CONTRIBUTING.md) an!

Dort finden Sie:
- Detaillierte Anleitungen für die Entwicklungsumgebung
- Informationen zur Architektur und Datenflüssen
- Test-Strategien und Qualitätsstandards
- Richtlinien für Pull Requests

## Support
Issues/Feature Requests bitte über GitHub Issues.
