# Contributing to Emlog Home Assistant Integration

Willkommen bei der Emlog Home Assistant Integration! Vielen Dank für Ihr Interesse an der Weiterentwicklung dieses Projekts.

**Nutzer-Dokumentation:** Siehe [README.md](README.md) für Installations- und Verwendungshinweise.

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
   - Gehen Sie in die **Optionen** (Zahnrad-Icon) um Preise und Faktoren zu testen

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

#### Release Management

```bash
make release-dry-run    # Teste Semantic Release (Dry-Run, ohne zu pushen)
make release-notes      # Zeige generierte Release Notes für nächste Release
```

#### Aufräumen

```bash
make clean         # Services stoppen und Container entfernen
make full-clean    # Vollständiges Cleanup (inkl. Images)
```

## ✨ Code Quality & Formatting

### Prettier Code Formatting

Alle Code-Änderungen **MÜSSEN** mit Prettier formatiert sein, bevor sie committed werden!

```bash
# Überprüfe Formatierung
npm run prettier

# Repariere Formatierungsprobleme automatisch
npm run prettier-fix
```

**Wichtige Regeln:**

- ✅ Führe `npm run prettier-fix` VOR jedem Commit aus
- ✅ Keine Commits mit Formatierungsfehlern pushen
- ✅ Prettier wird durch Git Hooks automatisch überprüft (nach `husky install`)

### Code Style

- **Python**: PEP 8 via Black und Pylint
- **JSON/YAML**: Prettier
- **Markdown**: Prettier mit max 80 Zeichen pro Zeile

## 🏗️ Architektur verstehen

### Projektstruktur

```
hacs_emlog/
├── custom_components/emlog/     # HACS Integration
│   ├── __init__.py             # Integration Setup
│   ├── config_flow.py          # UI-Konfiguration
│   ├── coordinator.py          # Daten-Polling
│   ├── sensor.py               # Sensor-Entities
│   ├── template.py             # Kosten-Sensoren
│   ├── const.py                # Konstanten
│   ├── manifest.json           # Integration-Metadaten
│   └── translations/           # UI-Übersetzungen (de.json, en.json)
├── docs/                       # Dokumentation
│   ├── guides/                 # Getting Started
│   ├── architecture/           # Technisches Design
│   └── api/                    # API Referenz
├── package/emlog.yaml          # Legacy YAML-Package
├── tests/
│   ├── mock/                   # Mock Server (Flask)
│   └── config/                 # HA Test-Konfiguration
├── tools/                      # Scripts & Docker
│   ├── docker/                 # Docker Configs
│   └── scripts/                # Test-Scripts
└── Makefile                    # Task Runner
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

### Test-Helper Entities verwenden

Die Test-Konfiguration (`tests/config/configuration.yaml`) enthält vordefinierte `input_number` Entities für das Testen von Preisen und Faktoren:

#### Verfügbare Helper Entities

**Strom (Electricity):**

- `input_number.strom_preis_kwh` - Strompreis: **0.3850 EUR/kWh**
- `input_number.strom_grundpreis_monat` - Grundpreis: **50.00 EUR/Monat**
- `input_number.strom_abschlag_monat` - Abschlag: **120.00 EUR/Monat**

**Gas:**

- `input_number.gas_preis_kwh` - Gaspreis: **0.1200 EUR/kWh**
- `input_number.gas_grundpreis_monat` - Grundpreis: **15.00 EUR/Monat**
- `input_number.gas_abschlag_monat` - Abschlag: **80.00 EUR/Monat**
- `input_number.gas_brennwert` - Brennwert: **11.58 kWh/m³** (aus package/emlog.yaml)
- `input_number.gas_zustandszahl` - Zustandszahl: **0.95** (aus package/emlog.yaml)

#### So verwendest du diese zum Testen

1. Starten Sie die Entwicklungsumgebung: `make dev-setup`
2. Öffne Home Assistant: http://localhost:8123
3. Gehe zu **Einstellungen > Geräte & Dienste > Emlog** (Zahnrad-Icon)
4. Gehe zu **Optionen**
5. Bei jedem Feld kannst du die entsprechende `input_number` Entity verlinken:
   - Preis pro kWh → `input_number.strom_preis_kwh` oder `input_number.gas_preis_kwh`
   - Basis-Preis (€/Monat) → `input_number.strom_grundpreis_monat` oder `input_number.gas_grundpreis_monat`
   - Gasbrennwert → `input_number.gas_brennwert`
   - etc.

6. Speichern → Die Sensoren verwenden jetzt die dynamischen Werte!
7. Ändere die `input_number` Werte in der UI und beobachte, wie sich die Sensor-Berechnungen ändern

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

## � Commit Konventionen

**CRITICAL:** Alle Commits MÜSSEN [Conventional Commits](https://www.conventionalcommits.org/) Format folgen!

Dieses Projekt verwendet **Semantic Release** für automatisierte Versionierung.

### Commit Format mit Scopes

```
type(scope): description

[body]

[footer]
```

### Erlaubte Scopes

- `coordinator:` - Änderungen an `coordinator.py` (Daten-Polling)
- `sensor:` - Änderungen an `sensor.py` (Sensor-Entities)
- `config:` - Änderungen an `config_flow.py` (UI-Konfiguration)
- `template:` - Änderungen an `template.py` (Kosten-Sensoren)
- `manifest:` - Änderungen an `manifest.json` (Integration-Metadaten)
- `const:` - Änderungen an `const.py` (Konstanten)
- `translations:` - Änderungen an Übersetzungsdateien
- `mock:` - Änderungen am Mock-Server
- `test:` - Test-bezogene Änderungen
- `docs:` - Dokumentationsänderungen
- `ci:` - CI/CD-Konfiguration
- `chore:` - Allgemeine Wartung

### ⚠️ WICHTIG: Granulare Commits (KEINE Sammel-Commits!)

**Regel:** Jeder Commit = Genau EINE logische Änderung

```
✅ RICHTIG - Granular:
feat(const): add base price constants
feat(config): add base price fields to options flow
feat(sensor): implement property-based value resolution
feat(translations): add base price descriptions

❌ FALSCH - Sammel-Commit:
feat: add base price support everywhere
```

Wenn mehrere Dateien betroffen sind: Separate Commits erstellen!

Nutze `git add -p` für selective staging wenn Änderungen gemischt sind.

### Erlaubte Commit-Typen

- `feat:` - Neue Features (erhöht MINOR version)
- `fix:` - Bugfixes (erhöht PATCH version)
- `docs:` - Dokumentation
- `style:` - Code-Formatierung (keine Funktionalität)
- `refactor:` - Code-Refaktorierung (keine Funktionalität)
- `perf:` - Performance-Verbesserungen
- `test:` - Tests hinzufügen/korrigieren
- `chore:` - Wartungsarbeiten
- `build:` - Build-System/Dependencies
- `ci:` - CI/CD-Konfiguration

### Commit-Beispiele

```bash
# Feature
git commit -m "feat(sensor): add new gas consumption sensor entity"

# Bug Fix
git commit -m "fix(coordinator): resolve timeout in API polling"

# Dokumentation
git commit -m "docs(readme): update installation instructions"

# Dependency
git commit -m "chore(deps): update semantic-release to v25.0.2"

# CI/CD
git commit -m "ci(workflow): add automated testing to GitHub Actions"

# Breaking Change
git commit -m "feat(config)!: change host validation logic

BREAKING CHANGE: host configuration now requires protocol prefix"
```

### Interaktive Commits

Verwende `npm run commit` für eine interaktive Commit-Erstellung mit deutschen Prompts:

```bash
npm run commit
```

Dies führt dich durch:

- Auswahl des Commit-Typs (feat, fix, docs, etc.)
- Scope der Änderung
- Betreff und Beschreibung
- Breaking Changes
- Issue-Referenzen

**Alle Commits werden automatisch validiert** - bei Fehlern wird der Commit abgelehnt.

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

## � Automatisierte Releases mit Semantic Release

Dieses Projekt verwendet **Semantic Release** für automatisierte Versionierung und Release-Verwaltung.

### Wie es funktioniert

1. **Commits analysieren:** Bei jedem Push werden Commits analysiert
2. **Version berechnen:** Basierend auf Conventional Commits (feat, fix, etc.)
3. **Release erstellen:** Automatische GitHub-Release mit aktualisierten Daten
4. **CHANGELOG aktualisieren:** Release Notes werden in CHANGELOG.md eingetragen

### Release-Typen

```
feat(scope):     → MINOR Release (0.4.0 → 0.5.0)
fix(scope):      → PATCH Release (0.4.0 → 0.4.1)
docs/test/etc:   → Kein Release
```

### Testing vor dem Release

Vor dem Pushen können Sie die nächste Release testen:

```bash
# Test ohne zu pushen
make release-dry-run

# Zeige generierte Release Notes
make release-notes
```

### Beispiel: Test-Release

```bash
$ make release-dry-run
🚀 Teste Semantic Release (Dry-Run)...

The next release version is 0.5.0
✔ Completed step "analyzeCommits"
✔ Completed step "generateNotes"
```

```bash
$ make release-notes
📝 Generierte Release Notes:

## 0.5.0 (2026-01-14)

### Features
* my new feature ([abc1234](https://github.com/...))

### Bug Fixes
* fixed bug ([def5678](https://github.com/...))
```

### Automatische GitHub Actions

Bei jedem Push zu `main` werden folgende Schritte automatisch ausgeführt:

1. ✅ Commits analysieren
2. ✅ Neue Version berechnen
3. ✅ CHANGELOG.md generieren
4. ✅ Git-Tag erstellen (z.B. v0.5.0)
5. ✅ GitHub Release veröffentlichen

**Keine manuellen Schritte notwendig!**

### Manuelle Releases

Es gibt drei Wege, einen Release manuell auszulösen:

#### 1. Lokal im Codespace/Terminal

```bash
make release
```

Dies führt aus:

1. Commits seit letztem Release analysieren
2. Version berechnen und aktualisieren
3. CHANGELOG.md generieren
4. Git Tag erstellen
5. GitHub Release veröffentlichen
6. Alle Änderungen zu Git pushen

**Mit Bestätigungsdialog für Sicherheit!**

#### 2. Via GitHub CLI (Remote Trigger)

```bash
make release-github
```

Triggert die GitHub Actions Workflow remote. **Benötigt einen Personal Access Token (PAT) mit `workflow` Scope!**

**PAT Setup (einmalig pro Codespace):**

1. **Token erstellen:**
   - Gehe zu https://github.com/settings/tokens/new
   - **Note:** `Codespaces Release Workflow`
   - **Expiration:** 90 days (oder Custom nach Bedarf)
   - **Scopes:** Nur `workflow` auswählen
   - Klicke **Generate token**
   - **Token kopieren** (wird nur einmal angezeigt!)

2. **In Codespace verwenden:**

   ```bash
   gh auth login
   # Wähle: GitHub.com → Paste an authentication token → Token einfügen
   ```

3. **Release triggern:**
   ```bash
   make release-github
   # Zeigt URL zum Workflow: https://github.com/strausmann/hacs_emlog/actions/workflows/release.yml
   ```

**🔐 Token dauerhaft speichern (Codespaces Secret):**

Um das Token nicht bei jeder neuen Codespace-Instanz eingeben zu müssen:

1. Gehe zu https://github.com/settings/codespaces
2. Klicke **New secret**
3. **Name:** `GH_WORKFLOW_TOKEN`
4. **Value:** Dein PAT einfügen
5. **Repository access:** `strausmann/hacs_emlog` auswählen
6. Klicke **Add secret**

**In Codespace verfügbar machen:**

```bash
# In .bashrc oder .zshrc hinzufügen (nur einmal):
echo 'export GITHUB_TOKEN=$GH_WORKFLOW_TOKEN' >> ~/.bashrc
source ~/.bashrc

# Dann gh CLI neu authentifizieren:
gh auth login --with-token <<< $GH_WORKFLOW_TOKEN
```

**Alternative: In devcontainer.json**

```json
{
  "remoteEnv": {
    "GITHUB_TOKEN": "${localEnv:GH_WORKFLOW_TOKEN}"
  }
}
```

> **Hinweis:** Mit Codespaces Secret ist das Token automatisch in jeder neuen Instanz verfügbar!

#### 3. GitHub Actions UI (Einfachste Methode)

Kein Token Setup notwendig:

1. Gehe zu https://github.com/strausmann/hacs_emlog/actions/workflows/release.yml
2. Klicke **Run workflow** (Dropdown)
3. Branch auswählen: `main`
4. Klicke **Run workflow** (Button)

### Zeitgesteuerte Releases

Die Release-Automation läuft automatisch:

- **Täglich um 02:00 UTC** (über `schedule` in GitHub Actions)
- **Oder manuell** via eine der drei oben genannten Methoden

**Vorteil:** Releases werden nicht bei jedem Commit erstellt, sondern nur wenn wirklich neue Features/Fixes vorhanden sind.

## �🐛 Fehler melden

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
