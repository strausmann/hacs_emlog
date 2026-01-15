# Development Guide - Emlog Home Assistant Integration

**Praktischer Guide für Feature-Entwicklung, Testing, Debugging und Releases.**

---

## Quick Start: Feature entwickeln

### 1. Feature-Planung

```bash
# 1a. Branch erstellen
git checkout -b feature/your-feature-name

# 1b. Verständnis überprüfen
# - Was wird hinzugefügt? (neuer Sensor, neue Config, etc.)
# - Betrifft es mehrere Komponenten?
# - Wird ein Migration/Breaking Change nötig?

# 1c. Abhängigkeiten klären
# - Braucht es neue const?
# - Neue Translations?
# - Neue Tests?
```

### 2. Implementierung mit Checkliste

```bash
# IMMER TESTEN, BEVOR DU BEGINNST!
make check-logs

# 2a. Schreibe Code
# Siehe: "Feature-Entwicklungs-Pattern" weiter unten

# 2b. Nach JEDER Änderung testen
make ha-reload

# 2c. Python Syntax validieren
python3 -m py_compile custom_components/emlog/*.py

# 2d. Formatiere Code
npm run prettier-fix -- <file>

# 2e. Git staging: GRANULAR (ein Commit = eine Änderung!)
git add custom_components/emlog/const.py
git commit -m "feat(const): add NEW_CONSTANT"

git add custom_components/emlog/sensor.py
git commit -m "feat(sensor): implement new sensor logic"

# Nicht:
# git add .
# git commit -m "added feature xyz"  <- BAD!
```

### 3. Nach Fertigstellung

```bash
# Final validation
make check-logs       # Integration lädt noch?
make ha-reload       # Final test in HA

# Push
git push origin feature/your-feature-name

# Erstelle PR mit guter Beschreibung
```

---

## Feature-Entwicklungs-Pattern

### Pattern 1: Neuen Sensor hinzufügen

**Beispiel: Gaseinspeisungs-Sensor (feed-in gas)**

#### Schritt 1: Konstanten in const.py

```python
# const.py
# (Am besten nah bei verwandten Konstanten)
CONF_INCLUDE_FEED_IN_GAS = "include_feed_in_gas"  # Neue Config
SENSOR_FEED_IN_GAS_VERBRAUCH = "feed_in_gas_verbrauch_m3"  # Sensor-Key
```

#### Schritt 2: Translation hinzufügen

```json
// translations/de.json
{
  "config": {
    "step": {
      "init": {
        "data": {
          "include_feed_in_gas": "Gas-Einspeisungs-Sensoren einschließen"
        },
        "description": {
          "include_feed_in_gas": "Nur wenn Biogasanlage verfügbar. Zeigt Einspeisungsmengen an."
        }
      }
    }
  }
}

// translations/en.json
{
  "config": {
    "step": {
      "init": {
        "data": {
          "include_feed_in_gas": "Include gas feed-in sensors"
        },
        "description": {
          "include_feed_in_gas": "Only if biogas facility available. Shows feed-in volumes."
        }
      }
    }
  }
}
```

#### Schritt 3: Config Flow anpassen

```python
# config_flow.py - EmlogOptionsFlowHandler.async_step_init()
# Am Ende des Schema-Aufbaus (vor vol.Schema creation):

if meter_type == METER_TYPE_GAS:
    current_include_feed_in_gas = options.get(
        CONF_INCLUDE_FEED_IN_GAS,
        data.get(CONF_INCLUDE_FEED_IN_GAS, False)
    )
    schema_dict[vol.Optional(CONF_INCLUDE_FEED_IN_GAS, default=current_include_feed_in_gas)] = bool
```

#### Schritt 4: Sensor-Definition in sensor.py

```python
# sensor.py - am Ende der Sensor-Listen

GAS_FEED_IN_SENSORS = [
    EmlogSensorDef(
        key="feed_in_verbrauch_m3",
        name="Gas Einspeisungs-Volumen",
        unit="m³",
        device_class=SensorDeviceClass.GAS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
]
```

#### Schritt 5: Sensor-Creation in async_setup_entry()

```python
# sensor.py - async_setup_entry()
# In der Schleife für Sensor-Erstellung:

# Bedingte Sensor-Listen
if meter_type == METER_TYPE_GAS and options.get(CONF_INCLUDE_FEED_IN_GAS):
    sensor_defs.extend(GAS_FEED_IN_SENSORS)
```

#### Schritt 6: Daten-Extraktion im Coordinator

```python
# coordinator.py - async_update_data()
# Neue Methode für Gas-Einspeisungs-Daten

async def _get_gas_feed_in_verbrauch(self) -> float:
    """Extrahiere Gas-Einspeisungs-Volumen."""
    data = await self._fetch_data()
    # Passe an echte API-Struktur an!
    return float(
        data.get("Zaehlerstand_Lieferung_Gas", {}).get("Stand_Feed_In", 0) or 0
    )
```

#### Schritt 7: Testen (vor Commit!)

```bash
# 1. Syntax validieren
python3 -m py_compile custom_components/emlog/*.py

# 2. Formatieren
npm run prettier-fix -- custom_components/emlog/sensor.py
npm run prettier-fix -- custom_components/emlog/config_flow.py
npm run prettier-fix -- custom_components/emlog/const.py
npm run prettier-fix -- custom_components/emlog/translations/de.json
npm run prettier-fix -- custom_components/emlog/translations/en.json

# 3. Integration neu laden
make ha-reload

# 4. Log Check
make check-logs

# 5. Manuell in HA prüfen: Erscheint neuer Sensor? Korrekte Werte?
```

---

## Common Pitfalls & Lösungen

### Pitfall 1: ImportError - Konstante nicht in const.py

**Problem:**

```
ImportError: cannot import name 'METER_TYPE_STROM' from 'custom_components.emlog.const'
```

**Ursache:** Neue Konstante wird in `__init__.py`, `sensor.py`, etc. verwendet, aber nicht in `const.py` definiert.

**Lösung:**

1. Alle verwendeten Konstanten in `const.py` definieren
2. `from .const import NEW_CONST` hinzufügen
3. `make check-logs` ausführen

**Workaround (schnell debuggen):**

```bash
grep -r "METER_TYPE_STROM" custom_components/emlog/*.py  # Alle Verwendungen finden
grep "METER_TYPE_STROM" custom_components/emlog/const.py # In const.py vorhanden?
```

### Pitfall 2: JSON-Syntaxfehler in translations

**Problem:**

```
json.decoder.JSONDecodeError: Expecting value: line 1, column 1
```

**Ursache:** Ungültiger JSON in `de.json` oder `en.json` (fehlende Kommas, falsche Klammern).

**Lösung:**

```bash
python3 -m json.tool custom_components/emlog/translations/de.json > /dev/null
python3 -m json.tool custom_components/emlog/translations/en.json > /dev/null

# Oder mit jq (falls installiert):
jq . custom_components/emlog/translations/de.json
```

**Prevention:** Nutze VS Code JSON-Validierung:

- Install "JSON Schema Store" Extension
- JSON wird live validiert während du schreibst

### Pitfall 3: Sensor-Daten extrahieren - Nested Dict falsch

**Problem:**

```
KeyError: 'Zaehlerstand_Bezug' oder None-Wert
```

**Ursache:** API-Struktur nicht korrekt verstanden, oder Fallback-Logik fehlerhaft.

**Lösung - korrekt extrahieren:**

```python
# ❌ FALSCH - crasht wenn Key nicht existiert
value = data["Zaehlerstand_Bezug"]["Stand180"]

# ✅ RICHTIG - mit Fallback
value = float(
    data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0
)

# Erklärung:
# - data.get("X", {})           # Wenn X fehlt, gib leeres Dict zurück
# - .get("Y", 0)                # Wenn Y fehlt, gib 0 zurück
# - or 0                         # Wenn Wert None/False, gib 0 zurück
# - float(...)                  # Konvertiere zu float
```

### Pitfall 4: Meter-Index Validierung schlägt fehl

**Problem:**

```
Setup failed: HTTP 400 from http://192.168.1.100/pages/getinformation.php?export&meterindex=99
```

**Ursache:** Meter-Index 99 existiert auf der Hardware nicht.

**Lösung:**

```python
# In config_flow.py - validate_emlog_connection()
# Diese Funktion ist bereits korrekt implementiert!
# Sie validiert die Verbindung beim Setup.

# Wenn User Index eintippt, der nicht existiert:
# 1. Setup-Step zeigt HTTP 400 Error
# 2. Config Flow lässt User neuen Index eingeben
# 3. Keine ungültige Konfiguration möglich
```

### Pitfall 5: Helper-Entity nicht gefunden

**Problem:**

```
Sensor zeigt no-data, statt Helper-Wert zu verwenden
```

**Ursache:** Helper-Entity-ID nicht exakt korrekt (z.B. `input_number.price` statt `input_number.electricity_price`).

**Lösung:**

```python
# In coordinator.py oder sensor.py - Helper extrahieren:

def get_helper_value(hass, entity_id: str, fallback_value: float) -> float:
    """Hole Wert aus Helper-Entity mit Fallback."""
    if not entity_id:
        return fallback_value

    try:
        state = hass.states.get(entity_id)
        if state and state.state not in ("unknown", "unavailable"):
            return float(state.state)
    except (ValueError, AttributeError):
        _LOGGER.warning(f"Cannot convert {entity_id} to float, using fallback")

    return fallback_value

# Verwendung:
price = get_helper_value(
    hass,
    options.get(CONF_PRICE_HELPER, ""),
    DEFAULT_PRICE_KWH
)
```

### Pitfall 6: Tarifwechsel-Datum Format falsch

**Problem:**

```
Neue Preise werden nie aktiv (werden als Date gezählt, nicht verglichen)
```

**Ursache:** Datum-Format ist nicht ISO 8601 (`YYYY-MM-DD`).

**Lösung:**

```python
# Immer ISO 8601 verwenden!
from datetime import datetime

def should_use_new_price(change_date_str: str) -> bool:
    """Prüfe ob neuer Preis wirksam sein sollte."""
    if not change_date_str:
        return False

    try:
        change_date = datetime.strptime(change_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        return today >= change_date
    except ValueError:
        _LOGGER.error(f"Invalid date format: {change_date_str}, use YYYY-MM-DD")
        return False
```

**In Translations dokumentieren:**

```json
{
  "config": {
    "step": {
      "init": {
        "description": {
          "price_change_date_strom": "Format: YYYY-MM-DD (z.B. 2026-01-01)"
        }
      }
    }
  }
}
```

### Pitfall 7: Sammel-Commits werden abgelehnt

**Problem:**

```
error: commit message does not follow conventional commits format
```

**Ursache:** Commit-Message folgt nicht dem Pattern `type(scope): description` oder kombiniert mehrere Änderungen.

**Lösung:**

```bash
# ❌ FALSCH
git commit -m "add feature"                    # Kein type/scope
git commit -m "fix(sensor): fix everything"   # Sammel-Commit

# ✅ RICHTIG
git commit -m "feat(sensor): add feed-in sensors"      # Eine Änderung
git commit -m "fix(const): add missing defaults"       # Eine Änderung
git commit -m "feat(translations): add german labels"  # Eine Änderung

# Wenn du bereits einen Sammel-Commit gemacht hast:
git reset --soft HEAD~1     # Undo letzten Commit
git add file1.py
git commit -m "feat(sensor): ..."
git add file2.py
git commit -m "feat(config): ..."
```

---

## Testing-Checkliste

Bevor du einen Commit machst:

```bash
# 1. IMMER: Log-Validierung
make check-logs
# ✅ Sollte "✅ Alles OK" zeigen
# ❌ Falls Fehler: Integration lädt nicht -> Beheben!

# 2. IMMER: Integration neu laden
make ha-reload
# ✅ Sollte "✅ Home Assistant neugestartet" zeigen
# ✅ Coordinator-Logs sollten erfolgreiche Datenabrufe zeigen

# 3. Python Syntax
python3 -m py_compile custom_components/emlog/*.py
# ✅ Sollte keine Fehler zeigen

# 4. JSON Validierung (falls Translations geändert)
python3 -m json.tool custom_components/emlog/translations/de.json > /dev/null
python3 -m json.tool custom_components/emlog/translations/en.json > /dev/null
# ✅ Sollte keine Fehler zeigen

# 5. Code-Formatierung
npm run prettier-fix -- <geänderte Dateien>
# ✅ Prettier sollte Files (un)changed anzeigen

# 6. Manueller Spot-Check (wenn UI-Änderungen)
# - Öffne HA Web UI (http://localhost:8123)
# - Gehe zu Settings → Devices & Services → Emlog
# - Prüfe: Neue Felder? Neue Sensoren? Korrekte Werte?
```

---

## Release-Prozess

### 1. Vorbereitung

```bash
# Stelle sicher, dass main-Branch up-to-date ist
git checkout main
git pull origin main

# Stelle sicher, dass alle Tests grün sind
make check-logs
make ha-reload

# Lese CHANGELOG.md und verstehe letzte Änderungen
cat CHANGELOG.md | head -50
```

### 2. Release-Nummern (Semantic Versioning)

Release-Nummern werden AUTOMATISCH von Semantic Release berechnet:

- `feat:` Commit → **Minor** Version (0.2.0 → 0.3.0)
- `fix:` Commit → **Patch** Version (0.2.0 → 0.2.1)
- `feat!:` (Breaking Change) → **Major** Version (0.2.0 → 1.0.0)

### 3. Release durchführen

```bash
# GitHub Release wird AUTOMATISCH erstellt durch:
# 1. GitHub Actions (nach Push zu main)
# 2. Semantic Release (in .releaserc.json konfiguriert)

# Deine Aufgabe:
1. Stelle sicher, dass Commits dem Pattern folgen ✅
2. Pushe zu main ✅
3. GitHub Actions macht den Rest 🎉

# Manual Release (falls nötig):
npm run release

# Das erzeugt:
# - Neue Version in package.json
# - CHANGELOG.md aktualisiert
# - Git Tag erstellt
# - GitHub Release erstellt
# - alles committed und gepusht
```

### 4. Troubleshooting: Release schlägt fehl

```bash
# Häufigste Ursache: Commits folgen nicht dem Pattern

# Debug:
git log --oneline -10  # Letzten 10 Commits anschauen
# Sollte Pattern sein: "type(scope): description"

# Falls falsch: Fix und neuer Commit
git rebase -i HEAD~3   # Letzte 3 Commits editieren
# (Aber normalerweise besser: neuer Commit mit Fix!)

# Oder: GitHub Actions Logs prüfen
# - Gehe zu Actions Tab
# - Sieh dir "Release" Workflow an
# - Error Message lesen und beheben
```

---

## Bekannte Limitationen & Gotchas

### 1. Meter-Indizes sind Hardware-spezifisch

**Limitation:** Die Integration unterstützt Indizes 1-4, aber nicht alle Emlog-Geräte haben alle 4 Meter.

**Workaround:** Config Flow validiert Index beim Setup. Wenn falsch → Setup schlägt fehl, User gibt neuen Index ein.

**Zukünftige Verbesserung:** Auto-Discovery der verfügbaren Meter?

### 2. Feed-In Sensoren nur für Strom

**Limitation:** Gas kann nicht rückgespeist werden (physikalisch unmöglich). Feed-in Feature nur für `METER_TYPE_STROM`.

**Warum so:** Andere HACS Integrations haben auch type-spezifische Features.

### 3. Tarifwechsel nur mit manuellem Datum

**Limitation:** Kann nicht automatisch Tarifwechsel-Daten von Versorger abrufen.

**Workaround:** User muss Datum und neue Preise manuell eingeben.

**Zukünftige Idee:** Automation mit Home Assistant Automations erstellen?

### 4. Helper-Entities müssen vorher existieren

**Limitation:** Wenn User `input_number.electricity_price` referenziert, muss diese Entity in HA bereits existieren.

**Error:** Nichts passiert (Helper-Entity wird einfach ignoriert).

**Workaround:** Dokumentieren, dass User Helper-Entities im `configuration.yaml` definieren muss (oder via UI erstellen).

### 5. Polling-Interval ist global

**Limitation:** `CONF_SCAN_INTERVAL` gilt für ALLE Sensoren des Meters. Kann nicht einzelne Sensoren schneller aktualisieren.

**Warum:** Home Assistant Coordinator-Pattern - alle Entities eines Coordinators teilen sich den Update-Interval.

### 6. Unique IDs können nicht geändert werden (ohne Data-Loss)

**Gotcha:** Wenn wir unique-ID Pattern ändern, verlieren User ihre HA History!

```python
# Beispiel: Alte ID
f"emlog_{host}_{meter_type}_{index}_zaehlerstand_kwh"

# Neue Idee: Andere Reihenfolge
f"emlog_{meter_type}_{host}_{index}_zaehlerstand_kwh"

# ❌ Problem: HA denkt es sind neue Entities
# 💥 Alte History ist weg!
```

**Lösung:** Unique-ID Schema ist now LOCKED - nur mit Breaking Change änderbar.

### 7. Config Entry Data vs. Options

**Gotcha:** Data (initial config) wird nur EINMAL beim Setup gespeichert. Options (überschreibungen) können jederzeit geändert werden.

```python
# Priorität in Options Flow:
data = config_entry.data           # Nur beim Setup gelesen, danach NICHT aktualisiert
options = config_entry.options     # User kann ändern

# In Sensoren/Coordinator:
value = options.get(KEY) or data.get(KEY) or DEFAULT

# Problem: Wenn User Host/Meter-Index ändern will, muss neue Config Entry erstellt werden
# (kann nicht in Options geändert werden - weil API-Ziel ändern würde)
```

**Workaround:** Nur änderbare Werte in Options - Host/Index sind read-only nach Setup.

---

## Debug-Tricks

### Trick 1: Live HA Logs watching

```bash
# Terminal 1: Folge HA Logs live
docker logs -f docker-homeassistant-1 | grep emlog

# Terminal 2: Mache Änderungen/Tests
# Logs erscheinen live in Terminal 1
```

### Trick 2: Python REPL für Schnelltests

```bash
python3
>>> from decimal import Decimal, ROUND_HALF_UP
>>> price = Decimal("0.456789")
>>> rounded = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
>>> float(rounded)
0.46
```

### Trick 3: Mock-Server Log anschauen

```bash
docker logs docker-emlog-mock-1 | grep "GET\|POST"
# Sieh welche API-Requests HA sendet
```

### Trick 4: Integration in HA neu laden (ohne Restart)

```bash
# Schneller als make ha-reload
make ha-reload

# Oder manuell im HA Web UI:
# Settings → Developer Tools → Services
# Suche: "reload"
# Wähle: Integration: Reload
# Wähle: emlog
```

### Trick 5: Config Entry Daten inspizieren

```bash
# In HA Web UI → Developer Tools → States
# Suche nach `config_entries`
# JSON zeigt alle Konfigurationen
```

---

## Ressourcen

- **Docs:** `.github/ARCHITECTURE_DECISIONS.md` - Design-Entscheidungen
- **Code:** `custom_components/emlog/` - Hauptcode
- **Tests:** `tests/mock/` - Mock-Server
- **CI/CD:** `.github/workflows/release.yml` - Automatische Releases
- **Git:** `.commitlintrc.json` - Commit-Validierung

---

**Zuletzt aktualisiert:** 2026-01-15
**Für Fragen:** Siehe `.github/copilot-instructions.md`
