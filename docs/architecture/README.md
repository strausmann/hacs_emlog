# 🏗️ Architektur der Emlog Integration

Technische Übersicht des HACS-Integration-Designs.

## 📊 System-Überblick

```
┌─────────────────────────────────────────────────────┐
│         Home Assistant Instance                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  Emlog Integration (custom_components)       │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │  config_flow.py                      │   │  │
│  │  │  • Benutzer-Konfiguration UI        │   │  │
│  │  │  • Host, Meter-Indizes              │   │  │
│  │  │  • Scan-Interval                    │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                    ↓                         │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │  coordinator.py                      │   │  │
│  │  │  • HTTP Polling (30s default)       │   │  │
│  │  │  • JSON API Parsing                 │   │  │
│  │  │  • Error Handling & Retry           │   │  │
│  │  │  • Daten-Caching                    │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                    ↓                         │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │  sensor.py                           │   │  │
│  │  │  • Entity Factories                 │   │  │
│  │  │  • Sensor-Definitionen              │   │  │
│  │  │  • Datentyp-Mapping                 │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  │                    ↓                         │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │  Sensoren                           │   │  │
│  │  │  • Electricity (6 Sensoren)        │   │  │
│  │  │  • Gas (6 Sensoren)                │   │  │
│  │  │  • Costs (8 Sensoren)              │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────┘  │
└────────────────┬─────────────────────────────────┘
                 │ HTTP GET
                 ↓
         ┌──────────────┐
         │ Emlog Device │
         │ (Meter API)  │
         └──────────────┘
```

## 🔄 Datenfluss

### 1. Initialization
```
Home Assistant Start
    ↓
ConfigEntry laden (config_flow)
    ↓
Coordinator instanziieren
    ↓
Sensor Entities erstellen
    ↓
Polling starten (coordinator.async_config_entry_first_refresh)
```

### 2. Polling Loop
```
30 Sekunden Interval (konfigurierbar)
    ↓
HTTP GET zu Emlog: /pages/getinformation.php?export&meterindex={index}
    ↓
JSON Response parsen
    ↓
Daten in Coordinator speichern
    ↓
Alle Sensoren updaten (automatisch via listener)
    ↓
Home Assistant State aktualisieren
```

### 3. Error Handling
```
API Request fehlgeschlagen?
    ↓ (Timeout/HTTP Error/JSON Error)
    ↓
UpdateFailed Exception werfen
    ↓
Home Assistant markiert Integration als unavailable
    ↓
Nächster Poll-Versuch nach 30s
```

## 📦 Komponenten-Details

### config_flow.py
**Aufgabe:** Konfigurationsfluss (Setup & Optionen)

**Funktionen:**
- User Input Formular (Host, Indizes)
- Validierung (Connectivity Check)
- Config Storage
- Options Flow (Scan Interval ändern)

**Data Flow:**
```
User Input → Validation → ConfigEntry → coordinator → sensor
```

### coordinator.py
**Aufgabe:** Zentrale Daten-Verwaltung

**Funktionen:**
- HTTP Requests zu Emlog API
- JSON Parsing
- Fehlerbehandlung
- Daten-Caching
- Automatische Updates (async_refresh)

**Key Classes:**
```python
class EmlogCoordinator(DataUpdateCoordinator):
    async def _async_update_data(self):
        # Pole alle Meter (STROM_SENSORS, GAS_SENSORS)
        # Aggregiere Daten
        # Caching
```

### sensor.py
**Aufgabe:** Entity Factories und Sensor-Definitionen

**Funktionen:**
- Sensor-Klasse-Subklassen
- Datentyp-Mapping
- Attribute Management (unit, device_class, state_class)

**Key Classes:**
```python
@dataclass
class EmlogSensorDef:
    key: str
    name: str
    unit: str | None
    device_class: SensorDeviceClass | None
    state_class: SensorStateClass | None

async def async_setup_entry(hass, entry, async_add_entities):
    # Erstelle Sensoren aus Definitionen
```

## 🔌 Emlog API Integration

### Endpoint
```
GET http://{host}:80/pages/getinformation.php?export&meterindex={index}
```

### Response Structure
```json
{
  "product": "Emlog - Electronic Meter Log",
  "version": 1.16,
  "Zaehlerstand_Bezug": {
    "Stand180": 12345.67,  // Zählerstand
    "Stand181": 12346.78,
    "Stand182": 12347.89
  },
  "Wirkleistung_Bezug": {
    "Leistung170": 1500,   // Aktuelle Leistung (W)
    "Leistung171": 1600,
    "Leistung172": 1700,
    "Leistung173": 1500
  },
  // ... weitere Felder
}
```

### Data Mapping
```python
# Extrahiere aus JSON:
def get_value(data, category, key, default=0):
    return float(data.get(category, {}).get(key, default) or default)

# Beispiel:
zaehlerstand = get_value(data, "Zaehlerstand_Bezug", "Stand180")
leistung = get_value(data, "Wirkleistung_Bezug", "Leistung173")
```

## 🧪 Testing-Architektur

### Mock Server
```
Flask App (tests/mock/mock_server.py)
    ↓
Simuliert Emlog API
    ↓
Realistic Consumption (200W avg electricity, 150W avg gas)
    ↓
JSON Response (identisch zu echtem Emlog)
```

### Docker Integration
```
docker-compose.test.yml
    ├── homeassistant (port 8123)
    ├── emlog-mock (port 8080)
    └── hacs_emlog_test (network)
```

## 🔐 Daten & State Management

### Unique ID Convention
```python
unique_id = f"emlog_{host}_{channel}_{sensor_key}".replace(".", "_")

# Beispiel:
"emlog_192.168.1.100_1_zaehlerstand_kwh"
```

### State Classes
```python
# SensorStateClass.TOTAL_INCREASING
# Für Zählerstände (nie fallend, nur steigende Werte)

# SensorStateClass.MEASUREMENT  
# Für Momentanwerte (Leistung, Temperatur)
```

### Device Classes
```python
SensorDeviceClass.ENERGY        # kWh
SensorDeviceClass.POWER         # W
SensorDeviceClass.MONETARY      # EUR, etc
```

## 🌐 Multi-Language Support

### Translation System
```
custom_components/emlog/translations/
    ├── de.json      # German
    └── en.json      # English
```

### Flüsse:
- config_flow Strings
- Options Flow Labels
- Sensor Names & Descriptions
- Error Messages

## 📈 Monitoring & Diagnostics

### Health Checks
- Connection Status (available/unavailable)
- Last Update Timestamp
- Poll Frequency
- Error Logging

### Logging
```python
_LOGGER = logging.getLogger(__name__)

# Verschiedene Level:
_LOGGER.debug("Polling started")
_LOGGER.info("Update successful")
_LOGGER.warning("Timeout detected")
_LOGGER.error("API error")
```

## 🚀 Deployment

### HACS Installation
```
1. User installiert HACS
2. Sucht "Emlog"
3. Lädt custom_components/emlog/ herunter
4. Home Assistant Neustart
5. Integration aus UI konfigurieren
```

### Package (Legacy)
```
1. package/emlog.yaml in packages/ kopieren
2. In configuration.yaml includen:
   packages:
     emlog: !include_dir_named packages/
3. Home Assistant Neustart
```

## 📚 Weitere Dokumentation

- [Sensor Reference](./sensors.md) (ToDo)
- [API Reference](../api/) 
- [Contributing Guide](../guides/CONTRIBUTING.md)
- [Codespaces Setup](../guides/README-Codespaces.md)

---

**Zuletzt aktualisiert:** 2025-01-15  
**Integration Version:** 0.1.0
