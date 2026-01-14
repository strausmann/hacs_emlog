from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import ConfigEntryNotReady

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up emlog from a config entry."""
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except ConfigEntryNotReady:
        raise
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    for meter_id, config in utility_meters.items():
        try:
            await hass.helpers.discovery.async_load_platform(
                "utility_meter",
                "platform",
                {"unique_id": meter_id, "source": source, "cycle": config["cycle"]},
                hass.data,
            )
        except Exception as err:
            _LOGGER.warning(f"Could not create utility meter {meter_id}: {err}")


async def async_create_cost_sensors(hass: HomeAssistant, entry: ConfigEntry, meter_type: str) -> None:
    """Create template sensors for cost calculation (consumption × price + base rate)."""
    # This is handled by template.yaml or can be added as template entities
    # For now, we'll create placeholder - real implementation in a follow-up
    pass
