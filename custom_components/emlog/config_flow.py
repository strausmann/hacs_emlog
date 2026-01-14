from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_STROM_INDEX,
    CONF_GAS_INDEX,
    CONF_SCAN_INTERVAL,
    DEFAULT_STROM_INDEX,
    DEFAULT_GAS_INDEX,
    DEFAULT_SCAN_INTERVAL,
)


class EmlogConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Unique ID: host + indices (damit nicht doppelt)
            await self.async_set_unique_id(
                f"{user_input[CONF_HOST]}_{user_input[CONF_STROM_INDEX]}_{user_input[CONF_GAS_INDEX]}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Emlog {user_input[CONF_HOST]}",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_STROM_INDEX, default=DEFAULT_STROM_INDEX): vol.Coerce(int),
                vol.Required(CONF_GAS_INDEX, default=DEFAULT_GAS_INDEX): vol.Coerce(int),
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @callback
    def async_get_options_flow(self, config_entry):
        return EmlogOptionsFlowHandler(config_entry)


class EmlogOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL,
                        self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    ),
                ): vol.Coerce(int),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
