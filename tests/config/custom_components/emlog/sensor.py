from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_HOST,
    CONF_METER_TYPE,
    CONF_METER_INDEX,
    CONF_SCAN_INTERVAL,
    CONF_PRICE_KWH,
    CONF_GAS_BRENNWERT,
    CONF_GAS_ZUSTANDSZAHL,
    CONF_PRICE_HELPER,
    CONF_GAS_BRENNWERT_HELPER,
    CONF_GAS_ZUSTANDSZAHL_HELPER,
    DEFAULT_PRICE_KWH,
    DEFAULT_GAS_BRENNWERT,
    DEFAULT_GAS_ZUSTANDSZAHL,
    METER_TYPE_STROM,
    METER_TYPE_GAS,
)
from .coordinator import EmlogCoordinator


@dataclass
class EmlogSensorDef:
    key: str
    name: str
    unit: str | None
    device_class: SensorDeviceClass | None
    state_class: SensorStateClass | None
    icon: str | None = None
    suggested_display_precision: int | None = None


# Gemeinsame Info-Sensoren (für beide Meter-Typen)
COMMON_SENSORS: list[EmlogSensorDef] = [
    EmlogSensorDef(
        "product",
        "Produkt",
        None,
        None,
        None,
        "mdi:chip",
    ),
    EmlogSensorDef(
        "version",
        "Software Version",
        None,
        None,
        None,
        "mdi:information-outline",
    ),
]

# Sensor-Definitionen für Strom
STROM_SENSORS: list[EmlogSensorDef] = [
    EmlogSensorDef(
        "zaehlerstand_kwh",
        "Zählerstand (kWh)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        "mdi:flash",
    ),
    EmlogSensorDef(
        "wirkleistung_w",
        "Wirkleistung (W)",
        "W",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
        "mdi:flash-outline",
    ),
    EmlogSensorDef(
        "verbrauch_tag_kwh",
        "Verbrauch Heute (kWh)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL,
        "mdi:counter",
    ),
    EmlogSensorDef(
        "betrag_tag_eur",
        "Betrag Heute",
        None,  # Wird dynamisch vom Coordinator gesetzt
        SensorDeviceClass.MONETARY,
        SensorStateClass.TOTAL,
        "mdi:currency-eur",
    ),
    EmlogSensorDef(
        "preis_eur_kwh",
        "Preis (kWh)",
        None,  # Wird dynamisch vom Coordinator gesetzt (z.B. EUR/kWh)
        SensorDeviceClass.MONETARY,
        None,
        "mdi:tag",
    ),
]

# Sensor-Definitionen für Gas
GAS_SENSORS: list[EmlogSensorDef] = [
    EmlogSensorDef(
        "zaehlerstand_m3",
        "Zählerstand (m³)",
        "m³",
        SensorDeviceClass.GAS,
        SensorStateClass.TOTAL_INCREASING,
        "mdi:gas-cylinder",
    ),
    EmlogSensorDef(
        "zaehlerstand_kwh",
        "Zählerstand (kWh)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
        "mdi:gas-burner",
    ),
    EmlogSensorDef(
        "wirkleistung_w",
        "Wirkleistung (W)",
        "W",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
        "mdi:fire",
    ),
    EmlogSensorDef(
        "verbrauch_tag_kwh",
        "Verbrauch Heute (kWh)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL,
        "mdi:counter",
    ),
    EmlogSensorDef(
        "betrag_tag_eur",
        "Betrag Heute",
        None,  # Wird dynamisch vom Coordinator gesetzt
        SensorDeviceClass.MONETARY,
        SensorStateClass.TOTAL,
        "mdi:currency-eur",
    ),
    EmlogSensorDef(
        "preis_eur_kwh",
        "Preis (kWh)",
        None,  # Wird dynamisch vom Coordinator gesetzt (z.B. EUR/kWh)
        SensorDeviceClass.MONETARY,
        None,
        "mdi:tag",
    ),
    EmlogSensorDef(
        "gas_brennwert",
        "Brennwert",
        None,
        None,
        None,
        "mdi:fire-circle",
    ),
    EmlogSensorDef(
        "gas_zustandszahl",
        "Zustandszahl",
        None,
        None,
        None,
        "mdi:gauge",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Emlog sensors from a config entry."""
    host = entry.data[CONF_HOST]
    meter_type = entry.data[CONF_METER_TYPE]
    meter_index = int(entry.data[CONF_METER_INDEX])
    scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, 30)))

    # Helper function to get value from entity or fallback to config
    def get_value_from_helper_or_config(helper_key: str, config_key: str, default_value: float) -> float:
        """Get value from helper entity state or fallback to config/options/default."""
        helper_entity_id = entry.options.get(helper_key, entry.data.get(helper_key, ""))
        
        if helper_entity_id:
            # Try to get state from helper entity
            state = hass.states.get(helper_entity_id)
            if state and state.state not in ("unknown", "unavailable"):
                try:
                    return float(state.state)
                except (ValueError, TypeError):
                    hass.logger.warning(
                        f"Could not convert helper entity {helper_entity_id} state '{state.state}' to float, using config value"
                    )
        
        # Fallback to options/data/default
        return float(entry.options.get(config_key, entry.data.get(config_key, default_value)))

    # Get values with priority: Helper state > Options > Data > Default
    price_kwh = get_value_from_helper_or_config(CONF_PRICE_HELPER, CONF_PRICE_KWH, DEFAULT_PRICE_KWH)
    gas_brennwert = get_value_from_helper_or_config(CONF_GAS_BRENNWERT_HELPER, CONF_GAS_BRENNWERT, DEFAULT_GAS_BRENNWERT)
    gas_zustandszahl = get_value_from_helper_or_config(CONF_GAS_ZUSTANDSZAHL_HELPER, CONF_GAS_ZUSTANDSZAHL, DEFAULT_GAS_ZUSTANDSZAHL)

    # Erstelle den Coordinator für diesen einen Zähler
    coordinator = EmlogCoordinator(hass, host, meter_type, meter_index, scan_interval, entry)
    
    # Versuche den Coordinator zu initialisieren, aber ignoriere Fehler beim Start
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        # Fehler beim initialen Refresh sind OK - der Coordinator wird weiterhin versuchen, Daten zu fetchen
        hass.logger.warning(f"Initial Emlog coordinator refresh failed (will retry): {err}")

    entities: list[SensorEntity] = []
    
    # Bestimme Meter-Namen einmal
    meter_name = "Strom" if meter_type == METER_TYPE_STROM else "Gas"

    # Preise und Faktoren aus Config (removed duplicates)
    
    # Gemeinsame Info-Sensoren (Produkt, Version)
    for sensor_def in COMMON_SENSORS:
        entities.append(
            EmlogSensorEntity(
                coordinator,
                host,
                meter_type,
                meter_index,
                meter_name,
                sensor_def,
                price_kwh,
                gas_brennwert,
                gas_zustandszahl,
            )
        )
    
    # Wähle die richtigen Sensoren basierend auf meter_type
    sensor_defs = STROM_SENSORS if meter_type == METER_TYPE_STROM else GAS_SENSORS
    
    for sensor_def in sensor_defs:
        entities.append(
            EmlogSensorEntity(
                coordinator,
                host,
                meter_type,
                meter_index,
                meter_name,
                sensor_def,
                price_kwh,
                gas_brennwert,
                gas_zustandszahl,
            )
        )

    # Status-Entitäten (für alle Meter-Typen)
    entities.append(EmlogStatusEntity(coordinator, host, meter_type, meter_index, meter_name))
    entities.append(EmlogLastErrorEntity(coordinator, host, meter_type, meter_index, meter_name))
    entities.append(EmlogLastUpdateEntity(coordinator, host, meter_type, meter_index, meter_name))

    async_add_entities(entities)


class EmlogSensorEntity(SensorEntity):
    """Representation of an Emlog Sensor."""

    def __init__(
        self,
        coordinator: EmlogCoordinator,
        host: str,
        meter_type: str,
        meter_index: int,
        meter_name: str,
        definition: EmlogSensorDef,
        price_kwh: float,
        gas_brennwert: float,
        gas_zustandszahl: float,
    ):
        self.coordinator = coordinator
        self._host = host
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._meter_name = meter_name
        self._definition = definition
        # Store initial values but will read from coordinator for dynamic updates
        self._initial_price_kwh = price_kwh
        self._initial_gas_brennwert = gas_brennwert
        self._initial_gas_zustandszahl = gas_zustandszahl

        # Entity ID mit Zählernummer für Konsistenz mit Utility Metern
        self.entity_id = f"sensor.emlog_{meter_type}_{meter_index}_{definition.key}"

        self._attr_name = f"Emlog {meter_name} {meter_index} {definition.name}"
        self._attr_unique_id = f"emlog_{host}_{meter_type}_{meter_index}_{definition.key}".replace(".", "_")
        # Native unit wird jetzt dynamisch in property gesetzt (wegen Währung)
        # self._attr_native_unit_of_measurement wird durch property überschrieben
        self._attr_device_class = definition.device_class
        self._attr_state_class = definition.state_class
        if definition.icon:
            self._attr_icon = definition.icon

    @property
    def _price_kwh(self) -> float:
        """Get current price from coordinator's config entry."""
        try:
            if hasattr(self.coordinator, 'config_entry'):
                entry = self.coordinator.config_entry
                helper_id = entry.options.get(CONF_PRICE_HELPER, entry.data.get(CONF_PRICE_HELPER, ""))
                if helper_id:
                    state = self.coordinator.hass.states.get(helper_id)
                    if state and state.state not in ("unknown", "unavailable"):
                        return float(state.state)
                return float(entry.options.get(CONF_PRICE_KWH, entry.data.get(CONF_PRICE_KWH, self._initial_price_kwh)))
        except Exception:
            pass
        return self._initial_price_kwh

    @property
    def _currency(self) -> str:
        """Get currency from coordinator."""
        if self.coordinator.data and hasattr(self.coordinator.data, 'currency'):
            return self.coordinator.data.currency or "EUR"
        return "EUR"

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement, dynamically set for monetary sensors."""
        # Wenn definition.unit None ist, verwende Währung vom Coordinator
        if self._definition.unit is None:
            if self._definition.key == "betrag_tag_eur":
                return self._currency
            elif self._definition.key == "preis_eur_kwh":
                return f"{self._currency}/kWh"
        return self._definition.unit

    @property
    def _gas_brennwert(self) -> float:
        """Get current brennwert from coordinator's config entry."""
        try:
            if hasattr(self.coordinator, 'config_entry'):
                entry = self.coordinator.config_entry
                helper_id = entry.options.get(CONF_GAS_BRENNWERT_HELPER, entry.data.get(CONF_GAS_BRENNWERT_HELPER, ""))
                if helper_id:
                    state = self.coordinator.hass.states.get(helper_id)
                    if state and state.state not in ("unknown", "unavailable"):
                        return float(state.state)
                return float(entry.options.get(CONF_GAS_BRENNWERT, entry.data.get(CONF_GAS_BRENNWERT, self._initial_gas_brennwert)))
        except Exception:
            pass
        return self._initial_gas_brennwert

    @property
    def _gas_zustandszahl(self) -> float:
        """Get current zustandszahl from coordinator's config entry."""
        try:
            if hasattr(self.coordinator, 'config_entry'):
                entry = self.coordinator.config_entry
                helper_id = entry.options.get(CONF_GAS_ZUSTANDSZAHL_HELPER, entry.data.get(CONF_GAS_ZUSTANDSZAHL_HELPER, ""))
                if helper_id:
                    state = self.coordinator.hass.states.get(helper_id)
                    if state and state.state not in ("unknown", "unavailable"):
                        return float(state.state)
                return float(entry.options.get(CONF_GAS_ZUSTANDSZAHL, entry.data.get(CONF_GAS_ZUSTANDSZAHL, self._initial_gas_zustandszahl)))
        except Exception:
            pass
        return self._initial_gas_zustandszahl

    @staticmethod
    def _get_decimal_places(value: float) -> int:
        """Ermittle die Anzahl der Nachkommastellen aus einem Float-Wert."""
        try:
            # Konvertiere zu String und zähle Dezimalstellen
            value_str = str(value)
            if '.' in value_str:
                # Entferne trailing zeros und zähle
                decimal_part = value_str.split('.')[1].rstrip('0')
                return len(decimal_part) if decimal_part else 0
            return 0
        except Exception:
            return 2  # Fallback: 2 Dezimalstellen

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        try:
            # Verfügbar, wenn Coordinator Daten hat (auch wenn Status "failed")
            return self.coordinator.data is not None
        except Exception:
            return False

    @property
    def suggested_display_precision(self) -> int | None:
        """Dynamische Nachkommastellen basierend auf Emlog-Daten."""
        try:
            value = self.native_value
            if value is None or not isinstance(value, (int, float)):
                return None
            
            # Berechne Nachkommastellen aus dem aktuellen Wert
            decimal_places = self._get_decimal_places(value)
            
            # Mindestens 2, maximal 6 Nachkommastellen
            return max(2, min(decimal_places, 6))
        except Exception:
            return 2

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            if self.coordinator.data is None:
                return None
            
            meter_data = self.coordinator.data.meter_data
            if not meter_data:
                return None
            
            # Extrahiere Wert basierend auf Sensor-Typ
            key = self._definition.key
            
            # Gemeinsame Info-Sensoren
            if key == "product":
                return str(meter_data.get("product", "Unknown"))
            elif key == "version":
                return float(meter_data.get("version", 0) or 0)
            
            # Meter-spezifische Sensoren
            elif key == "zaehlerstand_kwh":
                # Strom: Stand180 bereits kWh
                if self._meter_type == METER_TYPE_STROM:
                    return float(meter_data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
                # Gas: konvertiere m3 -> kWh mit Brennwert/Zustandszahl
                m3 = float(meter_data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
                return m3 * self._gas_brennwert * self._gas_zustandszahl
            elif key == "zaehlerstand_m3":
                return float(meter_data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
            elif key == "wirkleistung_w":
                return float(meter_data.get("Wirkleistung_Bezug", {}).get("Leistung170", 0) or 0)
            elif key == "verbrauch_tag_kwh":
                return float(meter_data.get("Kwh_Bezug", {}).get("Kwh180", 0) or 0)
            elif key == "betrag_tag_eur":
                return float(meter_data.get("Betrag_Bezug", {}).get("Betrag180", 0) or 0)
            elif key == "preis_eur_kwh":
                return float(self._price_kwh)
            elif key == "gas_brennwert":
                return float(self._gas_brennwert)
            elif key == "gas_zustandszahl":
                return float(self._gas_zustandszahl)
            
            return None
        except Exception:
            return None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        try:
            self.async_on_remove(
                self.coordinator.async_add_listener(self.async_write_ha_state)
            )
        except Exception:
            pass


class EmlogStatusEntity(SensorEntity):
    """Zeigt den API-Status an: 'connected', 'failed' oder 'initializing'."""

    def __init__(self, coordinator: EmlogCoordinator, host: str, meter_type: str, meter_index: int, meter_name: str):
        self.coordinator = coordinator
        self._host = host
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._meter_name = meter_name

        self._attr_name = f"Emlog {meter_name} {meter_index} API Status"
        self._attr_unique_id = f"emlog_{host}_{meter_type}_{meter_index}_api_status"
        self._attr_icon = "mdi:api"

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        # Immer verfügbar, auch wenn noch keine Daten da sind
        return True

    @property
    def native_value(self) -> str:
        try:
            if self.coordinator.data is None:
                return "Initializing..."
            return self.coordinator.data.api_status.capitalize()
        except Exception:
            return "Unknown"

    async def async_added_to_hass(self) -> None:
        try:
            self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
        except Exception:
            pass


class EmlogLastErrorEntity(SensorEntity):
    """Zeigt die letzte Fehlermeldung an."""

    def __init__(self, coordinator: EmlogCoordinator, host: str, meter_type: str, meter_index: int, meter_name: str):
        self.coordinator = coordinator
        self._host = host
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._meter_name = meter_name

        self._attr_name = f"Emlog {meter_name} {meter_index} Letzte Fehlermeldung"
        self._attr_unique_id = f"emlog_{host}_{meter_type}_{meter_index}_last_error"
        self._attr_icon = "mdi:alert-circle"

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        # Immer verfügbar
        return True

    @property
    def native_value(self) -> str:
        try:
            if self.coordinator.data is None:
                return "Initializing..."
            # Wenn kein Fehler, dann "-" oder None anzeigen
            return self.coordinator.data.last_error or "No errors"
        except Exception:
            return "Error"

    async def async_added_to_hass(self) -> None:
        try:
            self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
        except Exception:
            pass


class EmlogLastUpdateEntity(SensorEntity):
    """Zeigt den Zeitpunkt des letzten erfolgreichen Daten-Updates an."""

    def __init__(self, coordinator: EmlogCoordinator, host: str, meter_type: str, meter_index: int, meter_name: str):
        self.coordinator = coordinator
        self._host = host
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._meter_name = meter_name

        self._attr_name = f"Emlog {meter_name} {meter_index} Letztes Update"
        self._attr_unique_id = f"emlog_{host}_{meter_type}_{meter_index}_last_update"
        self._attr_icon = "mdi:clock"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        # Immer verfügbar, auch wenn noch keine Daten da sind
        return True

    @property
    def native_value(self) -> datetime | None:
        try:
            if self.coordinator.data is None:
                return None
            return self.coordinator.data.last_successful_update
        except Exception:
            return None

    async def async_added_to_hass(self) -> None:
        try:
            self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
        except Exception:
            pass
