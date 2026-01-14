"""Utility Meter Setup for Emlog Integration."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_HOST,
    CONF_METER_TYPE,
    METER_TYPE_STROM,
    METER_TYPE_GAS,
)

_LOGGER = logging.getLogger(__name__)

# Utility Meter Zyklen
UTILITY_METER_CYCLES = {
    "daily": "Tag",
    "monthly": "Monat", 
    "yearly": "Jahr",
}


async def async_setup_utility_meters(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Erstelle Utility Meter Config Entries für Emlog Zählerstände.
    
    Für jeden Emlog-Zähler werden drei Utility Meter erstellt:
    - daily (Tag)
    - monthly (Monat)
    - yearly (Jahr)
    """
    from .const import CONF_METER_INDEX
    
    host = entry.data[CONF_HOST]
    meter_type = entry.data[CONF_METER_TYPE]
    meter_index = entry.data[CONF_METER_INDEX]
    meter_type_name = "Strom" if meter_type == METER_TYPE_STROM else "Gas"
    
    # Finde die Zählerstands-Entity für diesen Meter
    registry = er.async_get(hass)
    source_entity_id = None
    
    # Suche nach der Zählerstands-Entity (z.B. sensor.emlog_strom_zaehlerstand_kwh)
    for entity in registry.entities.values():
        if (
            entity.platform == "emlog"
            and entity.config_entry_id == entry.entry_id
            and "zaehlerstand_kwh" in entity.entity_id
        ):
            source_entity_id = entity.entity_id
            break
    
    if not source_entity_id:
        _LOGGER.warning(
            f"Keine Zählerstands-Entity gefunden für {meter_type_name} ({host}). "
            "Utility Meter werden nicht erstellt."
        )
        return
    
    _LOGGER.info(
        f"Erstelle Utility Meter für {meter_type_name} Zähler {meter_index} Zählerstand: {source_entity_id}"
    )
    
    # Erstelle für jeden Zyklus einen Utility Meter
    for cycle, cycle_name in UTILITY_METER_CYCLES.items():
        await _async_create_utility_meter(
            hass, entry, source_entity_id, cycle, cycle_name, meter_type_name, meter_index
        )


async def _async_create_utility_meter(
    hass: HomeAssistant,
    parent_entry: ConfigEntry,
    source_entity_id: str,
    cycle: str,
    cycle_name: str,
    meter_type_name: str,
    meter_index: int,
) -> None:
    """Erstelle einen einzelnen Utility Meter Config Entry."""
    
    # Utility Meter unique_id und name mit Zählernummer
    unique_id = f"{parent_entry.unique_id}_{cycle}"
    name = f"Emlog {meter_type_name} {meter_index} Verbrauch {cycle_name}"
    
    # Prüfe ob dieser Utility Meter bereits existiert
    existing_entries = [
        entry
        for entry in hass.config_entries.async_entries("utility_meter")
        if entry.unique_id == unique_id
    ]
    
    if existing_entries:
        _LOGGER.debug(f"Utility Meter {name} existiert bereits")
        return
    
    # Erstelle Utility Meter Config Entry über den user flow
    try:
        result = await hass.config_entries.flow.async_init(
            "utility_meter",
            context={"source": "user"},
        )
        
        # Fülle das Formular aus
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                "source": source_entity_id,
                "cycle": cycle,
                CONF_NAME: name,
            },
        )
        
        # Setze die unique_id für den erstellten Entry
        if result["type"] == "create_entry":
            entry_id = result["result"].entry_id
            entry = hass.config_entries.async_get_entry(entry_id)
            if entry:
                hass.config_entries.async_update_entry(
                    entry,
                    unique_id=unique_id,
                )
            _LOGGER.info(f"✅ Utility Meter erstellt: {name}")
        
    except Exception as err:
        _LOGGER.error(f"Fehler beim Erstellen von Utility Meter {name}: {err}")


async def async_remove_utility_meters(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Entferne alle Utility Meter die zu diesem Emlog Entry gehören."""
    
    # Finde alle Utility Meter mit unserem unique_id Präfix
    unique_id_prefix = entry.unique_id
    
    utility_meters_to_remove = [
        um_entry
        for um_entry in hass.config_entries.async_entries("utility_meter")
        if um_entry.unique_id and um_entry.unique_id.startswith(unique_id_prefix)
    ]
    
    for um_entry in utility_meters_to_remove:
        _LOGGER.info(f"Entferne Utility Meter: {um_entry.title}")
        await hass.config_entries.async_remove(um_entry.entry_id)
