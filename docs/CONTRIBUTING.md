# Contributing to Emlog Home Assistant Integration

Willkommen bei der Emlog Home Assistant Integration! Vielen Dank für Ihr Interesse an der Weiterentwicklung dieses Projekts.

## 🚀 Schnellstart für Entwickler

### Entwicklungsumgebung einrichten

1. **Repository klonen:**

   ```bash
   git clone https://github.com/strausmann/hacs_emlog.git
   cd hacs_emlog
   ```

2. **Entwicklungsumgebung starten:**

   ```bash
   make dev-setup
   ```

3. **Integration testen:**
   - Öffnen Sie http://localhost:8123
   - Gehen Sie zu **Einstellungen > Geräte & Dienste**
   - **Integration hinzufügen > Emlog**
   - Konfigurieren Sie:
     - Host: `emlog-mock`
     - Strom Meterindex: `1`
     - Gas Meterindex: `2`

### Makefile-Befehle

Verwenden Sie die folgenden Make-Befehle für eine effiziente Entwicklung:

#### Grundlegende Befehle

```bash
make help          # Alle verfügbaren Befehle anzeigen
make dev-setup     # Komplette Entwicklungsumgebung starten
make dev-logs      # Logs beider Services anzeigen
make status        # Status aller Services anzeigen
```

#### Service-Management

```bash
# Mock Server
make mock-up       # Mock Server starten
make mock-down     # Mock Server stoppen
make mock-logs     # Mock Server Logs

# Home Assistant
make ha-up         # Home Assistant starten
make ha-down       # Home Assistant stoppen
make ha-logs       # Home Assistant Logs
```

#### Tests und Qualitätssicherung

```bash
make test          # Vollständige Tests (Mock Server + API)
make test-api      # Nur API-Endpunkte testen
make lint          # Code-Qualitätsprüfungen (Python, JSON, YAML)
```

#### Aufräumen

```bash
make clean         # Services stoppen und Container entfernen
make full-clean    # Vollständiges Cleanup (inkl. Images)
```

## 🏗️ Architektur verstehen

### Projektstruktur

```
hacs_emlog/
├── custom_components/emlog/     # HACS Integration
│   ├── __init__.py             # Integration Setup
│   ├── config_flow.py          # UI-Konfiguration
│   ├── coordinator.py          # Daten-Polling
│   ├── sensor.py               # Sensor-Entities
│   ├── const.py                # Konstanten
│   ├── manifest.json           # Integration-Metadaten
│   └── translations/           # UI-Übersetzungen
├── package/emlog.yaml          # Legacy YAML-Package
├── mock/                       # Test-Infrastruktur
├── test_config/                # HA-Testkonfiguration
├── tools/docker/compose.yml     # Test-Umgebung
└── Makefile                    # Entwicklungswerkzeuge
```

### Datenfluss

1. **Coordinator** fragt regelmäßig Emlog API ab
2. **Sensor Entities** verarbeiten die JSON-Daten
3. **Config Flow** ermöglicht UI-basierte Konfiguration
4. **Mock Server** simuliert Emlog API für Tests

## 🧪 Testen

### Mit Mock Server (empfohlen)

```bash
make dev-setup  # Startet Mock Server + Home Assistant
make test       # Führt alle Tests durch
```

### Mit echter Hardware

```bash
# Echte Emlog-IP in der Integration konfigurieren
# Beispiel: Host: 192.168.1.100
```

### API-Manuelle Tests

```bash
# Mock Server starten
make mock-up

# API-Endpunkte testen
curl "http://localhost:8080/pages/getinformation.php?export&meterindex=1"
curl "http://localhost:8080/pages/getinformation.php?export&meterindex=2"
```

## 🔧 Entwicklung

### Code-Qualität

- Verwenden Sie `make lint` vor jedem Commit
- Verwenden Sie `npm run prettier` um Code-Formatierung zu überprüfen
- Python-Code sollte PEP 8 konform sein
- Verwenden Sie aussagekräftige Commit-Nachrichten

### Commit-Richtlinien

Dieses Projekt verwendet **Conventional Commits** für automatisierte Versionierung:

#### Interaktive Commits

```bash
npm run commit
```

Führt Sie durch ein interaktives Menü mit deutschen Prompts zur Erstellung von Conventional Commits.

#### Manuelle Commits

Format: `type(scope): description`

**Typen:**

- `feat:` - Neues Feature (erhöht Minor-Version)
- `fix:` - Fehlerbehebung (erhöht Patch-Version)
- `docs:` - Dokumentation
- `style:` - Code-Formatierung (keine Funktionalität)
- `refactor:` - Code-Refaktorierung (keine Funktionalität)
- `perf:` - Performance-Verbesserung
- `test:` - Tests hinzufügen/korrigieren
- `chore:` - Wartungsarbeiten
- `build:` - Build-System/Dependencies
- `ci:` - CI/CD-Konfiguration

**Scopes (empfohlen):**

- `coordinator` - Daten-Polling Logik
- `sensor` - Sensor-Entities
- `config` - UI-Konfiguration
- `manifest` - Integration-Metadaten
- `const` - Konstanten und Konfiguration
- `translations` - UI-Übersetzungen
- `mock` - Test-Infrastruktur
- `test` - Tests
- `docs` - Dokumentation
- `ci` - CI/CD-Konfiguration
- `deps` - Dependencies
- `build` - Build-System

**Beispiele:**

```
feat(sensor): add new gas consumption sensor entity
fix(coordinator): resolve timeout in API polling
docs(readme): update installation instructions
chore(deps): update semantic-release to v25.0.2
ci(workflow): add automated testing to GitHub Actions
feat(config)!: change host validation logic

BREAKING CHANGE: host configuration now requires protocol prefix
```

Alle Commits werden automatisch validiert - bei Fehlern wird der Commit abgelehnt.

### Neue Features hinzufügen

1. **Planung:** Feature in einem Issue beschreiben
2. **Implementierung:** Code in entsprechendem Modul entwickeln
3. **Tests:** Mock-Daten und Tests hinzufügen
4. **Dokumentation:** README und Code-Kommentare aktualisieren

### Emlog API verstehen

Die Integration kommuniziert mit der Emlog API:

- **Endpoint:** `http://{host}/pages/getinformation.php?export&meterindex={index}`
- **Datenformat:** JSON mit verschachtelten Objekten
- **Meter-Indizes:** Typischerweise 1 (Strom) und 2 (Gas)

Beispiel API-Antwort:

```json
{
  "product": "Emlog - Electronic Meter Log",
  "version": 1.16,
  "Zaehlerstand_Bezug": { "Stand180": 3474, "Stand181": 0, "Stand182": 0 },
  "Wirkleistung_Bezug": {
    "Leistung170": 2.8,
    "Leistung171": 0,
    "Leistung172": 0,
    "Leistung173": 0
  },
  "Kwh_Bezug": { "Kwh180": 14, "Kwh181": 0, "Kwh182": 0 }
}
```

## 📝 Pull Requests

1. **Branch erstellen:** `git checkout -b feature/mein-feature`
2. **Änderungen committen:** `git commit -m "feat: Beschreibung des Features"`
3. **Pushen:** `git push origin feature/mein-feature`
4. **PR erstellen:** Über GitHub Interface

### PR-Checkliste

- [ ] `make lint` besteht
- [ ] `make test` besteht
- [ ] Neue Features sind in Mock-Daten abgebildet
- [ ] Dokumentation aktualisiert
- [ ] Changelog aktualisiert
- [ ] Tests für neue Funktionalität

## 🐛 Fehler melden

Bei Fehlern:

1. **Reproduktion:** Schritte zur Reproduktion beschreiben
2. **Logs:** Relevante Logs mit `make dev-logs` sammeln
3. **Umgebung:** HA-Version, Emlog-Version, Netzwerk-Setup
4. **Issue erstellen:** Mit detaillierter Beschreibung

## 📚 Weitere Ressourcen

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Integration Guidelines](https://hacs.xyz/docs/developer/)
- [Emlog API Dokumentation](https://shop.weidmann-elektronik.de/media/files_public/1235c869b3a5e00aad44fa0b521cddd6/Emlog%20Datenschnittstelle%20extern.pdf)

## 🙏 Danke

Vielen Dank für Ihre Beiträge zur Emlog Integration! Jeder Pull Request und jedes Issue hilft, das Projekt zu verbessern.
