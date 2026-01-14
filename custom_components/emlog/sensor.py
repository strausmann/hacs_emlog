from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_HOST, CONF_STROM_INDEX, CONF_GAS_INDEX, CONF_SCAN_INTERVAL
from .coordinator import EmlogCoordinator


@dataclass
class EmlogSensorDef:
    key: str
    name: str
    unit: str | None
    device_class: SensorDeviceClass | None
    state_class: SensorStateClass | None


STROM_SENSORS: list[EmlogSensorDef] = [
    EmlogSensorDef(
        "zaehlerstand_kwh",
        "Strom Zählerstand",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL_INCREASING,
    ),
    EmlogSensorDef(
        "wirkleistung_w",
        "Strom Wirkleistung",
        "W",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
    ),
    EmlogSensorDef(
        "verbrauch_tag_kwh",
        "Strom Verbrauch (Tag)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL,
    ),
]

GAS_SENSORS: list[EmlogSensorDef] = [
    EmlogSensorDef(
        "zaehlerstand_m3",
        "Gas Zählerstand",
        "m³",
        SensorDeviceClass.GAS,
        SensorStateClass.TOTAL_INCREASING,
    ),
    EmlogSensorDef(
        "wirkleistung_w",
        "Gas Wirkleistung",
        "W",
        SensorDeviceClass.POWER,
        SensorStateClass.MEASUREMENT,
    ),
    EmlogSensorDef(
        "verbrauch_tag_kwh",
        "Gas Verbrauch (Tag)",
        "kWh",
        SensorDeviceClass.ENERGY,
        SensorStateClass.TOTAL,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    host = entry.data[CONF_HOST]
    strom_index = int(entry.data[CONF_STROM_INDEX])
    gas_index = int(entry.data[CONF_GAS_INDEX])
    scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, 30)))

    coordinator = EmlogCoordinator(hass, host, strom_index, gas_index, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    entities: list[SensorEntity] = []
    for s in STROM_SENSORS:
        entities.append(EmlogSensorEntity(coordinator, host, "strom", s))
    for s in GAS_SENSORS:
        entities.append(EmlogSensorEntity(coordinator, host, "gas", s))

    async_add_entities(entities)


class EmlogSensorEntity(SensorEntity):
    def __init__(self, coordinator: EmlogCoordinator, host: str, channel: str, definition: EmlogSensorDef):
        self.coordinator = coordinator
        self._host = host
        self._channel = channel
        self._def = definition

        self._attr_name = f"Emlog {definition.name}"
        self._attr_unique_id = f"emlog_{host}_{channel}_{definition.key}".replace(".", "_")

        self._attr_native_unit_of_measurement = definition.unit
        self._attr_device_class = definition.device_class
        self._attr_state_class = definition.state_class

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        data = self.coordinator.data.strom if self._channel == "strom" else self.coordinator.data.gas

        # Mapping entsprechend der export JSON Struktur
        if self._channel == "strom":
            if self._def.key == "zaehlerstand_kwh":
                return float(data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
            if self._def.key == "wirkleistung_w":
                return float(data.get("Wirkleistung_Bezug", {}).get("Leistung170", 0) or 0)
            if self._def.key == "verbrauch_tag_kwh":
                return float(data.get("Kwh_Bezug", {}).get("Kwh180", 0) or 0)

        if self._channel == "gas":
            if self._def.key == "zaehlerstand_m3":
                return float(data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0) or 0)
            if self._def.key == "wirkleistung_w":
                return float(data.get("Wirkleistung_Bezug", {}).get("Leistung170", 0) or 0)
            if self._def.key == "verbrauch_tag_kwh":
                return float(data.get("Kwh_Bezug", {}).get("Kwh180", 0) or 0)

        return None

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
