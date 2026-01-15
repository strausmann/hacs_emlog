# Emlog Home Assistant Integration - AI Coding Guidelines

**Sprache / Language:** Mit Entwickler _strausmann_ stets auf Deutsch kommunizieren.

## Architecture Overview

This is a Home Assistant custom component for polling energy meter data from Emlog devices (Electronic Meter Log). The integration uses a **coordinator pattern** with local HTTP polling to fetch JSON data from meter endpoints.

**Migration Context:**

- Originally implemented as a YAML package (`package/emlog.yaml`)
- Now being migrated to a proper HACS custom component (`custom_components/emlog/`)
- The package version remains for backward compatibility and advanced features

**Key Components:**

- `coordinator.py`: Handles HTTP polling and data coordination
- `sensor.py`: Creates sensor entities from polled data
- `config_flow.py`: User configuration UI
- `package/emlog.yaml`: Legacy YAML package with cost calculations and utility meters (maintained for compatibility)

## Data Flow & API Integration

**Emlog API Structure (Complete):**

- Endpoint: `http://{host}/pages/getinformation.php?export&meterindex={index}`
- Returns comprehensive JSON with all meter data:

```json
{
  "product": "Emlog - Electronic Meter Log",
  "version": 1.16,
  "Zaehlerstand_Bezug": {"Stand180": value, "Stand181": value, "Stand182": value},
  "Zaehlerstand_Lieferung": {"Stand280": value, "Stand281": value, "Stand282": value},
  "Wirkleistung_Bezug": {"Leistung170": value, "Leistung171": value, "Leistung172": value, "Leistung173": value},
  "Wirkleistung_Lieferung": {"Leistung270": value, "Leistung271": value, "Leistung272": value, "Leistung273": value},
  "Kwh_Bezug": {"Kwh180": value, "Kwh181": value, "Kwh182": value},
  "Kwh_Lieferung": {"Kwh280": value, "Kwh281": value, "Kwh282": value},
  "Betrag_Bezug": {"Betrag180": value, "Betrag181": value, "Betrag182": value, "Waehrung": "EUR"},
  "Betrag_Lieferung": {"Betrag280": value, "Betrag281": value, "Betrag282": value, "Waehrung": "EUR"},
  "DiffBezugLieferung": {"Betrag": value}
}
```

**Data Mapping Pattern:**

```python
# From coordinator.py - extract values from nested JSON
return float(data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
```

**Unique ID Convention:**

```python
# From sensor.py - consistent entity identification
self._attr_unique_id = f"emlog_{host}_{channel}_{definition.key}".replace(".", "_")
```

## Code Style & Formatting

**⚠️ MANDATORY: Prettier Code Formatting**

Alle Dateien müssen mit Prettier formatiert sein BEVOR sie committed werden. Dies ist NICHT optional!

```bash
# Code-Stil überprüfen
npm run prettier

# Code-Stil automatisch korrigieren (VOR dem Commit!)
npm run prettier-fix
```

**WICHTIG für Copilot:**

- Immer `npm run prettier-fix` ausführen BEVOR Änderungen committed werden
- Keine Commits mit Formatierungsfehlern erstellen
- Prettier wird automatisch bei Git Hooks ausgeführt (nach husky install)

Formatierungsprobleme werden vom Prettier-Linter erkannt und müssen behoben werden.

## Commit Conventions & Semantic Release

**CRITICAL: Alle Commits MÜSSEN Conventional Commits Format folgen!**

Dieses Projekt verwendet **Semantic Release** für automatisierte Versionierung. Alle Commits müssen dem Conventional Commits Standard entsprechen:

### Commit Format mit Scopes

```
type(scope): description

[body]

[footer]
```

**⚠️ MANDATORY: Scope MUSS bei JEDEM Commit verwendet werden!**

Der Scope gibt an, welche Komponente betroffen ist. **Commits OHNE Scope sind nicht akzeptabel!**

### Erlaubte Scopes für dieses Projekt

- `coordinator:` - Änderungen an `coordinator.py` (Daten-Polling)
- `sensor:` - Änderungen an `sensor.py` (Sensor-Entities)
- `config:` - Änderungen an `config_flow.py` (UI-Konfiguration)
- `manifest:` - Änderungen an `manifest.json` (Integration-Metadaten)
- `const:` - Änderungen an `const.py` (Konstanten)
- `translations:` - Änderungen an Übersetzungsdateien
- `mock:` - Änderungen am Mock-Server (`mock/` Verzeichnis)
- `test:` - Test-bezogene Änderungen
- `docs:` - Dokumentationsänderungen
- `ci:` - CI/CD-Konfiguration (`.github/`, `.releaserc.json`)
- `deps:` - Dependency-Updates (`package.json`, `requirements.txt`)
- `build:` - Build-System und Entwicklungstools (`Makefile`, Docker)
- `chore:` - Allgemeine Wartung (Cleanup, Refactoring ohne Funktionsänderung)

### Erlaubte Commit-Typen (aus .releaserc.json)

- `feat:` - Neue Features (erhöht MINOR version)
- `fix:` - Bugfixes (erhöht PATCH version)
- `docs:` - Dokumentation
- `style:` - Code-Formatierung (keine Funktionalität)
- `refactor:` - Code-Refaktorierung (keine Funktionalität)
- `perf:` - Performance-Verbesserungen
- `test:` - Tests hinzufügen/korrigieren
- `chore:` - Wartungsarbeiten (Semantic Release verwendet diesen für Releases)
- `build:` - Build-System/Dependencies
- `ci:` - CI/CD-Konfiguration

### Breaking Changes

Für Breaking Changes:

```
feat!: breaking change description

BREAKING CHANGE: detailed explanation
```

### Beispiele

```
feat(sensor): add new gas consumption sensor entity
fix(coordinator): resolve timeout in API polling
docs(readme): update installation instructions
chore(deps): update semantic-release to v25.0.2
ci(workflow): add automated testing to GitHub Actions
feat(config)!: change host validation logic

BREAKING CHANGE: host configuration now requires protocol prefix
```

### Automatische Versionierung

- Semantic Release analysiert Commit-Typen automatisch
- Erstellt Releases, Tags und CHANGELOG.md
- Release-Commits verwenden: `chore(release): ${nextRelease.version}`

### WICHTIG für Copilot - Strenge Commit-Regeln

**⚠️ ABSOLUTE REGELN (KEINE AUSNAHMEN):**

1. **NIEMALS Sammel-Commits!** Jeder Commit = Genau EINE logische Änderung
   - ❌ FALSCH: Ein Commit mit Änderungen an config_flow.py + sensor.py + const.py
   - ✅ RICHTIG: Drei separate Commits - einer pro Datei/Feature

2. **Commits müssen granular sein:**
   - Jede neue Feature → eigener `feat(scope):` Commit
   - Jeder Bugfix → eigener `fix(scope):` Commit
   - Jede Übersetzung → eigener `translations:` Commit
   - Jede Test-Datei-Änderung → eigener `test(scope):` Commit

3. **Standard-Pattern für zusammenhängende Änderungen:**

   ```
   fix(__init__): remove broken async_setup_utility_meter import          [Commit 1]
   feat(const): add base price constants for electricity and gas          [Commit 2]
   feat(coordinator): store config_entry for property-based resolution    [Commit 3]
   feat(sensor): implement property-based value resolution                [Commit 4]
   feat(config): add base price fields and entity selectors               [Commit 5]
   feat(template): add cost sensor class with consumption calculation     [Commit 6]
   feat(manifest): bump version to 0.2.0 and require HA 2024.1.0         [Commit 7]
   feat(translations): add base price field descriptions (de + en)        [Commit 8]
   test: update test configuration and mock data                         [Commit 9]
   chore: fix gitignore to properly track custom_components/emlog        [Commit 10]
   ```

4. **Nutzen von git add --patch oder git reset:**
   - Wenn mehrere Änderungen in einer Datei: `git add -p` für selective staging
   - Wenn Änderungen gegenüber gemischt werden: `git reset` und neu-committen

5. **Commits OHNE Scope sind NICHT ERLAUBT:**
   - ❌ FALSCH: `feat: add new sensor` (kein Scope!)
   - ✅ RICHTIG: `feat(sensor): add new sensor`

6. **Bei Unsicherheit:**
   - `.releaserc.json` und `.commitlintrc.json` konsultieren
   - Commitlint validiert automatisch alle Commits
   - Fehlschlagende Commits werden abgelehnt

**Beispiel für FALSCHE Commits (unakzeptabel):**

```
feat: add new sensor                           ❌ Kein Scope!
feat(config): refactor all components          ❌ Sammel-Commit!
fix: fix several bugs in multiple files        ❌ Zu vage, mehrere Dinge!
docs: update docs                              ❌ Kein Scope!
```

**Beispiel für KORREKTE Commits (akzeptabel):**

```
feat(sensor): add new gas consumption sensor               ✅
fix(coordinator): resolve timeout in API polling          ✅
feat(config): add base price entity selector              ✅
feat(translations): add German descriptions for helpers    ✅
test(mock): update mock server response data              ✅
chore(manifest): bump version to 0.2.0                    ✅
```

**Commits sollten die Frage beantworten:**

- Was wurde genau geändert? (spezifisch)
- Welche Komponente? (Scope)
- Warum? (Commit-Message Body bei komplexen Änderungen)

## Configuration & Setup

**Integration Config:**

- `host`: IP address (without http://)
- `strom_index` & `gas_index`: Meter indices (default 1/2)
- `scan_interval`: Polling frequency in seconds (default 30)

**Package Enhancement (Legacy):**
The companion `package/emlog.yaml` provides advanced features but remains as the original YAML package implementation:

- Cost calculations with tariff switching
- Utility meters for daily/monthly/yearly consumption
- Gas conversion factors (Brennwert/Zustandszahl)
- Template sensors for effective pricing

**Migration Goal:** The HACS integration should eventually provide equivalent functionality to the YAML package, but currently focuses on core sensor data polling.

## Development Patterns

**Sensor Definition Pattern:**

```python
@dataclass
class EmlogSensorDef:
    key: str
    name: str
    unit: str | None
    device_class: SensorDeviceClass | None
    state_class: SensorStateClass | None

STROM_SENSORS = [
    EmlogSensorDef("zaehlerstand_kwh", "Strom Zählerstand", "kWh", SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    # ...
]
```

**Error Handling:**

```python
# From coordinator.py - consistent error patterns
try:
    async with session.get(url, timeout=10) as resp:
        if resp.status != 200:
            raise UpdateFailed(f"HTTP {resp.status} from {url}")
        return await resp.json(content_type=None)
except asyncio.TimeoutError as err:
    raise UpdateFailed(f"Timeout while fetching {url}") from err
```

**Translation Support:**

- German primary language with English fallback
- Keys match configuration constants from `const.py`

## Testing & Validation

**Integration Testing (HACS):**

- Integration requires running Emlog device on network
- Test with actual meter indices and host IP
- Validate JSON response structure matches expected nesting
- Focus on core sensor functionality

**Package Testing (Legacy):**

- YAML package uses `resource_template` for dynamic URLs
- Test tariff switching with `input_datetime` entities
- Validate cost calculations against utility meter cycles
- Maintains backward compatibility for existing users

**Development Testing:**

- Use `./test.sh` to start mock server and test API endpoints
- Mock server provides realistic JSON responses for both electricity and gas meters
- Docker Compose setup (`docker-compose.test.yml`) for isolated testing
- Test configuration in `test_config/configuration.yaml`
- Use `make` commands for quick development workflow management

## Key Files Reference

- `Makefile`: Development workflow commands and automation
- `CONTRIBUTING.md`: Comprehensive development guidelines and workflow
- `custom_components/emlog/manifest.json`: Integration metadata and requirements
- `custom_components/emlog/const.py`: All configuration constants and defaults
- `custom_components/emlog/coordinator.py`: Core data fetching logic
- `custom_components/emlog/sensor.py`: Entity creation and data mapping
- `package/emlog.yaml`: Legacy YAML package implementation (backward compatibility)
- `.devcontainer/devcontainer.json`: Development environment configuration
- `mock/`: Mock server for testing without physical Emlog device
- `test.sh`: Test script for running mock server and validation
- `docker-compose.test.yml`: Docker setup for isolated testing
- `.releaserc.json`: Semantic Release configuration (CRITICAL für Commit-Format!)
- `.commitlintrc.json`: Commitlint configuration (muss bei allen Commits befolgt werden!)
- `package.json`: Node.js dependencies for tooling (Prettier, Commitlint, Husky)</content>
  <parameter name="filePath">/workspaces/hacs_emlog/.github/copilot-instructions.md
