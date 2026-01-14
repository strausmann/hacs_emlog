from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import ConfigEntryNotReady

from .utility_meter import async_setup_utility_meters, async_remove_utility_meters

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up emlog from a config entry."""
    try:
        # Setup sensor platform
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        # Setup utility meters after sensors are ready
        # Warte bis die Sensor-Entities registriert sind
        await hass.async_add_executor_job(
            lambda: None  # Dummy wait to ensure sensors are registered
        )
        await async_setup_utility_meters(hass, entry)
        
    except ConfigEntryNotReady:
        raise
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove utility meters first
    await async_remove_utility_meters(hass, entry)
    
    # Then unload sensor platform
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
