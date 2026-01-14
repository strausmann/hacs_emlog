# Emlog Home Assistant Integration - AI Coding Guidelines

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

**Emlog API Structure:**
- Endpoint: `http://{host}/pages/getinformation.php?export&meterindex={index}`
- Returns JSON with nested structure: `{"Zaehlerstand_Bezug": {"Stand180": value}, "Wirkleistung_Bezug": {"Leistung170": value}, ...}`

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

## Key Files Reference

- `custom_components/emlog/manifest.json`: Integration metadata and requirements
- `custom_components/emlog/const.py`: All configuration constants and defaults
- `custom_components/emlog/coordinator.py`: Core data fetching logic
- `custom_components/emlog/sensor.py`: Entity creation and data mapping
- `package/emlog.yaml`: Legacy YAML package implementation (backward compatibility)
- `.devcontainer/devcontainer.json`: Development environment configuration
- `mock/`: Mock server for testing without physical Emlog device
- `test.sh`: Test script for running mock server and validation
- `docker-compose.test.yml`: Docker setup for isolated testing</content>
<parameter name="filePath">/workspaces/hacs_emlog/.github/copilot-instructions.md