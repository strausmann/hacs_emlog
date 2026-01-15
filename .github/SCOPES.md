# Commit Scopes Reference

**Dokumentation aller erlaubten Commit Scopes für die Emlog Integration.**

---

## Scope-Strategie

Scopes sollten:

- **Semantisch** sein (was wird geändert?)
- **Reusable** sein (immer gleiche Scopes verwenden)
- **Granular** sein (nicht zu viel kombiniert)
- **Self-documenting** sein (Name erklärt die Änderung)

**Guideline:** Scopes orientieren sich an **Dateien/Komponenten**, nicht an Änderungen. Ein Scope = Eine Komponente/Datei-Familie.

---

## ✅ Erlaubte Scopes

### 🔧 Core Components (Hauptkomponenten)

| Scope           | Anwendungsfall                      | Betrifft           | Beispiel                                                             |
| --------------- | ----------------------------------- | ------------------ | -------------------------------------------------------------------- |
| `coordinator`   | Daten-Polling, API-Logik            | `coordinator.py`   | `fix(coordinator): resolve timeout in API polling`                   |
| `sensor`        | Sensor-Entitäten, Daten-Mapping     | `sensor.py`        | `feat(sensor): add new gas consumption sensor entity`                |
| `config`        | Config Flow, Optionen, Benutzer-UI  | `config_flow.py`   | `feat(config): add base price fields and entity selectors`           |
| `template`      | Template-Sensoren, Kostenberechnung | `template.py`      | `feat(template): add cost sensor class with consumption calculation` |
| `utility-meter` | Utility-Meter Konfiguration         | `utility_meter.py` | `fix(utility-meter): correct meter reset logic`                      |

### 📋 Metadata & Configuration

| Scope          | Anwendungsfall                   | Betrifft                                       | Beispiel                                                          |
| -------------- | -------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| `const`        | Konstanten-Definitionen          | `const.py`                                     | `feat(const): add base price constants for electricity and gas`   |
| `manifest`     | Integration-Metadaten, Versionen | `manifest.json`                                | `feat(manifest): bump version to 0.2.0 and require HA 2024.1.0`   |
| `translations` | Mehrsprachige Texte              | `translations/de.json`, `translations/en.json` | `feat(translations): add base price field descriptions (de + en)` |

### 🧪 Testing & Mocking

| Scope  | Anwendungsfall                   | Betrifft      | Beispiel                                                    |
| ------ | -------------------------------- | ------------- | ----------------------------------------------------------- |
| `mock` | Mock-Server für Tests            | `tests/mock/` | `feat(mock): add realistic meter response data for testing` |
| `test` | Test-Dateien, Test-Konfiguration | `tests/`      | `test: update test configuration and mock data`             |

### 📚 Documentation

| Scope          | Anwendungsfall            | Betrifft                                                            | Beispiel                                                      |
| -------------- | ------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------- |
| `docs`         | Dokumentation, READMEs    | `README.md`, `docs/`                                                | `docs(readme): update installation instructions`              |
| `architecture` | Architektur-Dokumentation | `.github/ARCHITECTURE_DECISIONS.md`, `.github/DEVELOPMENT_GUIDE.md` | `docs(architecture): document helper entity fallback pattern` |

### 🔐 CI/CD & Git

| Scope   | Anwendungsfall                       | Betrifft                                       | Beispiel                                                           |
| ------- | ------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------ |
| `ci`    | GitHub Actions, CI-Pipelines         | `.github/workflows/`                           | `ci(workflow): add automated testing to GitHub Actions`            |
| `build` | Build-System, Makefile, Dependencies | `Makefile`, `package.json`, `requirements.txt` | `build(makefile): add check-logs target for pre-commit validation` |

### 🔄 Maintenance & Refactoring

| Scope   | Anwendungsfall              | Betrifft                           | Beispiel                                                         |
| ------- | --------------------------- | ---------------------------------- | ---------------------------------------------------------------- |
| `chore` | Allgemeine Wartung, Cleanup | Misc                               | `chore: fix gitignore to properly track custom_components/emlog` |
| `deps`  | Dependency-Updates          | `package.json`, `requirements.txt` | `deps: update semantic-release to v25.0.2`                       |

---

## ❌ NICHT erlaubte Patterns

### Sammel-Commits (VERBOTEN!)

```bash
❌ FALSCH:
feat(config): refactor all components and add new features

❌ FALSCH:
fix: fix everything in coordinator, config, and sensor

❌ FALSCH:
docs: update docs and add architecture decisions
```

**Grund:** Ein Commit = Ein logisches Change. Mehrere Scopes in einem Commit sind unklar und schwer zu reviewen.

**Richtig:**

```bash
✅ RICHTIG - Drei separate Commits:
feat(coordinator): add timeout retry logic
feat(config): add base price fields
feat(sensor): implement property-based value resolution
```

### Kombinierte Scopes (VERBOTEN!)

```bash
❌ FALSCH: feat(coordinator/sensor): add new sensor

Grund: Nur ein Scope pro Commit!
```

### Zu spezifische Scopes (VERMEIDEN!)

```bash
❌ ZU SPEZIFISCH:
feat(__init__): add async setup
feat(strings.json): add translations
feat(device_registry): register device

✅ BESSER:
fix(__init__): remove broken async_setup_utility_meter import
feat(translations): add base price descriptions
(device registry -> hat keinen eigenen Scope, gehört zu config)
```

---

## 📋 Decision Tree: Welcher Scope?

```
Bin ich unklar, welcher Scope richtig ist?

1. WAS WIRD GEÄNDERT?
   ├─ Hauptlogik → coordinator, sensor, template, utility-meter
   ├─ Benutzer-UI → config
   ├─ Konstanten → const
   ├─ Metadaten → manifest
   ├─ Tests → mock, test
   ├─ Dokumentation → docs, architecture
   ├─ CI/CD → ci, build
   └─ Sonstiges → chore, deps

2. WELCHE DATEI(EN)?
   ├─ coordinator.py → coordinator
   ├─ sensor.py → sensor
   ├─ template.py → template
   ├─ utility_meter.py → utility-meter
   ├─ config_flow.py → config
   ├─ const.py → const
   ├─ manifest.json → manifest
   ├─ translations/ → translations
   ├─ tests/mock/ → mock
   ├─ tests/ → test
   ├─ .github/workflows/ → ci
   ├─ Makefile, package.json → build
   ├─ README.md, docs/ → docs
   ├─ .github/ARCHITECTURE_DECISIONS.md → docs (oder architecture)
   └─ sonstige → chore

3. IST ES MEHRERE DATEIEN?
   ├─ JA → Mehrere separate Commits (je eine Datei/Komponente pro Commit!)
   └─ NEIN → Ein Commit mit entsprechendem Scope
```

---

## 📊 Scope-Häufigkeit (erwartete Verteilung)

Wie oft sollten welche Scopes verwendet werden?

| Scope                | Häufigkeit | Grund                          |
| -------------------- | ---------- | ------------------------------ |
| `fix(sensor)`        | ⭐⭐⭐⭐⭐ | Sensoren sind das Kernfeature  |
| `feat(sensor)`       | ⭐⭐⭐⭐   | Regelmäßige neue Sensoren      |
| `feat(template)`     | ⭐⭐⭐     | Neue Kostenberechnung-Features |
| `fix(coordinator)`   | ⭐⭐⭐     | API-Fehler treten auf          |
| `feat(config)`       | ⭐⭐⭐     | Neue Config-Optionen           |
| `fix(config)`        | ⭐⭐       | UI-Fehler selten               |
| `feat(const)`        | ⭐⭐       | Neue Konstanten für Features   |
| `fix(const)`         | ⭐         | Konstanten-Fehler selten       |
| `feat(manifest)`     | ⭐         | Version Bumps beim Release     |
| `feat(translations)` | ⭐⭐       | Neue UI-Texte                  |
| `fix(translations)`  | ⭐         | Typos in Übersetzungen         |
| `docs(...)`          | ⭐⭐       | Dokumentation erweitern        |
| `test(...)`          | ⭐         | Tests hinzufügen               |
| `ci(...)`            | ⭐         | CI-Konfiguration               |
| `build(...)`         | ⭐⭐       | Build-Tools                    |
| `chore(...)`         | ⭐         | Cleanup                        |
| `deps(...)`          | ⭐         | Dependency Updates             |

---

## 🎯 Best Practices

### ✅ DO: Gute Scope-Nutzung

```bash
# Sensor Features
git commit -m "feat(sensor): add new gas feed-in sensor entity"
git commit -m "fix(sensor): resolve null pointer in data extraction"

# Config UI Improvements
git commit -m "feat(config): add entity selector for price helper"
git commit -m "fix(config): validate meter index range 1-4"

# Dokumentation
git commit -m "docs(readme): update installation instructions"
git commit -m "docs(architecture): explain helper entity fallback pattern"

# Tests
git commit -m "test: update mock data for new sensor"
git commit -m "feat(mock): add gas feed-in response"

# Maintenance
git commit -m "chore: fix gitignore patterns"
git commit -m "deps: update semantic-release to v25.0.2"
```

### ❌ DON'T: Schlechte Scope-Nutzung

```bash
# Sammel-Commits
❌ git commit -m "feat(sensor, config, const): add everything"

# Unklar
❌ git commit -m "feat(fix): something something"

# Falsch kombiniert
❌ git commit -m "feat(coordinator/sensor): do both"

# Zu spezifisch
❌ git commit -m "feat(coordinator.py): add one line"

# Generisch
❌ git commit -m "feat(internal): stuff"
```

---

## 🔍 Häufige Fragen

### F: Was wenn Änderung mehrere Dateien betrifft?

A: **Ein Commit pro Datei/Komponente!** Nicht alles in einen Commit quetschen.

```bash
# ❌ FALSCH
git add coordinator.py sensor.py const.py
git commit -m "feat(core): implement everything"

# ✅ RICHTIG
git add const.py
git commit -m "feat(const): add new constants for feature X"

git add coordinator.py
git commit -m "feat(coordinator): implement API integration for feature X"

git add sensor.py
git commit -m "feat(sensor): create new sensor using coordinator"
```

### F: Was wenn ich Typo in const.py und sensor.py habe?

A: **Zwei separate Commits!**

```bash
git add const.py
git commit -m "fix(const): correct typo in constant name"

git add sensor.py
git commit -m "fix(sensor): update constant reference after rename"
```

### F: Was wenn eine Änderung mehrere Komponenten braucht, aber ein logisches Feature ist?

A: **Mehrere Commits, aber zusammenhängend im PR.**

Beispiel: "Add new sensor for solar feed-in"

```bash
# Commit 1: Konstanten
git commit -m "feat(const): add FEED_IN constants"

# Commit 2: Config-UI
git commit -m "feat(config): add toggle for feed-in sensors"

# Commit 3: Sensor-Logik
git commit -m "feat(sensor): implement feed-in sensor entities"

# Commit 4: Koordinator-Daten
git commit -m "feat(coordinator): extract feed-in data from API"

# Commit 5: Übersetzungen
git commit -m "feat(translations): add feed-in sensor labels"

# All in ONE PR, aber FÜNF separate, granular Commits!
```

### F: Was ist mit "fix(#123)" oder "ref(optimization)"?

A: **Nicht verwenden! Nur die erlaubten Scopes verwenden.**

Die erlaubten Scopes sind fix definiert in `.commitlintrc.json` und `.releaserc.json`.

---

## 🚀 Tools & Validierung

### Automatische Validierung

```bash
# Commitlint prüft JEDEN Commit automatisch
# Ungültige Commits werden blockiert:
git commit -m "add feature"
# ❌ ERROR: "add feature" does not match pattern "type(scope): description"

git commit -m "feat(invalid_scope): add feature"
# ❌ ERROR: "invalid_scope" is not allowed

git commit -m "feat(sensor): add feature"
# ✅ OK - Commit akzeptiert!
```

### Interaktives Commit-Tool

```bash
npm run cz
# Interaktives CLI-Tool mit Auswahl der Scopes
# Hilft bei Auswahl des richtigen Scopes
```

---

## 📚 Referenzen

- `.commitlintrc.json` - Technische Validierung
- `.releaserc.json` - Semantic Release Konfiguration
- `CONTRIBUTING.md` - Development Guidelines
- `.github/copilot-instructions.md` - Überblick

---

**Zuletzt aktualisiert:** 2026-01-15
**Status:** Aktiv - diese Scopes sind final und sollten nicht erweitert werden!
