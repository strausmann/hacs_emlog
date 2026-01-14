from __future__ import annotations

import asyncio
import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_METER_TYPE,
    CONF_METER_INDEX,
    CONF_SCAN_INTERVAL,
    DEFAULT_METER_INDEX,
    DEFAULT_SCAN_INTERVAL,
    METER_TYPE_STROM,
    METER_TYPE_GAS,
    CONF_PRICE_KWH,
    CONF_GAS_BRENNWERT,
    CONF_GAS_ZUSTANDSZAHL,
    CONF_PRICE_HELPER,
    CONF_GAS_BRENNWERT_HELPER,
    CONF_GAS_ZUSTANDSZAHL_HELPER,
    CONF_BASE_PRICE_STROM,
    CONF_BASE_PRICE_GAS,
    CONF_BASE_PRICE_STROM_HELPER,
    CONF_BASE_PRICE_GAS_HELPER,
    DEFAULT_PRICE_KWH,
    DEFAULT_GAS_BRENNWERT,
    DEFAULT_GAS_ZUSTANDSZAHL,
    DEFAULT_BASE_PRICE_STROM,
    DEFAULT_BASE_PRICE_GAS,
    EMLOG_EXPORT_PATH,
)

_LOGGER = logging.getLogger(__name__)


async def validate_emlog_connection(hass, host: str, meter_index: int) -> dict[str, str]:
    """Validiere die Verbindung zur Emlog API.
    
    Returns:
        Dict mit error key wenn Fehler, sonst leeres dict
    """
    session = async_get_clientsession(hass)
    url = f"http://{host}{EMLOG_EXPORT_PATH}?export&meterindex={meter_index}"
    
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                return {
                    "base": "cannot_connect",
                    "error_detail": f"HTTP {resp.status} für Meter-Index {meter_index}"
                }
            
            # Versuche JSON zu parsen
            try:
                data = await resp.json(content_type=None)
            except Exception as err:
                return {
                    "base": "invalid_response",
                    "error_detail": f"Ungültige JSON-Antwort: {err}"
                }
            
            # Prüfe ob die erwarteten Emlog-Felder vorhanden sind
            if not isinstance(data, dict):
                return {
                    "base": "invalid_response",
                    "error_detail": "JSON ist kein Dictionary"
                }
            
            # Prüfe auf typische Emlog-Felder
            expected_fields = ["product", "version", "Zaehlerstand_Bezug", "Wirkleistung_Bezug"]
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                return {
                    "base": "invalid_response",
                    "error_detail": f"Fehlende Felder: {', '.join(missing_fields)}"
                }
            
            # Prüfe ob es wirklich Emlog ist
            product = data.get("product", "")
            if "emlog" not in product.lower():
                return {
                    "base": "invalid_response",
                    "error_detail": f"Kein Emlog-Gerät (product: {product})"
                }
            
            _LOGGER.debug(f"Successfully validated meter (index {meter_index})")
            return {}
            
    except asyncio.TimeoutError:
        return {
            "base": "timeout_connect",
            "error_detail": f"Timeout beim Verbinden zu {host}"
        }
    except aiohttp.ClientConnectorError as err:
        return {
            "base": "cannot_connect",
            "error_detail": f"Verbindung zu {host} fehlgeschlagen: {err}"
        }
    except Exception as err:
        return {
            "base": "unknown",
            "error_detail": f"Unerwarteter Fehler: {type(err).__name__} - {err}"
        }


class EmlogConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Emlog."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler."""
        return EmlogOptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validiere die Verbindung zur Emlog API
            validation_result = await validate_emlog_connection(
                self.hass,
                user_input[CONF_HOST],
                user_input[CONF_METER_INDEX]
            )
            
            if validation_result:
                # Fehler bei der Validierung
                errors["base"] = validation_result["base"]
                error_detail = validation_result.get("error_detail", "")
                _LOGGER.error(f"Emlog validation failed: {error_detail}")
                
                # Zeige das Formular erneut mit Fehler
                schema = vol.Schema(
                    {
                        vol.Required(CONF_HOST, default=user_input[CONF_HOST]): str,
                        vol.Required(CONF_METER_TYPE, default=user_input[CONF_METER_TYPE]): vol.In({
                            METER_TYPE_STROM: "Strom",
                            METER_TYPE_GAS: "Gas"
                        }),
                        vol.Required(CONF_METER_INDEX, default=user_input[CONF_METER_INDEX]): vol.Coerce(int),
                        vol.Required(CONF_SCAN_INTERVAL, default=user_input[CONF_SCAN_INTERVAL]): vol.Coerce(int),
                    }
                )
                return self.async_show_form(
                    step_id="user",
                    data_schema=schema,
                    errors=errors,
                    description_placeholders={"error_detail": error_detail}
                )
            
            # Validierung erfolgreich - Unique ID setzen
            meter_type_name = "Strom" if user_input[CONF_METER_TYPE] == METER_TYPE_STROM else "Gas"
            await self.async_set_unique_id(
                f"{user_input[CONF_HOST]}_{user_input[CONF_METER_TYPE]}_{user_input[CONF_METER_INDEX]}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Emlog {meter_type_name} ({user_input[CONF_HOST]})",
                data=user_input,
            )

        # Zeige das Formular
        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_METER_TYPE, default=METER_TYPE_STROM): vol.In({
                    METER_TYPE_STROM: "Strom",
                    METER_TYPE_GAS: "Gas"
                }),
                vol.Required(CONF_METER_INDEX, default=DEFAULT_METER_INDEX): vol.Coerce(int),
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class EmlogOptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow to adjust price and gas factors without deleting the entry."""

    async def async_step_init(self, user_input=None):
        errors = {}

        data = self.config_entry.data
        options = self.config_entry.options
        meter_type = data.get(CONF_METER_TYPE)

        current_price = options.get(CONF_PRICE_KWH, data.get(CONF_PRICE_KWH, DEFAULT_PRICE_KWH))
        current_brennwert = options.get(CONF_GAS_BRENNWERT, data.get(CONF_GAS_BRENNWERT, DEFAULT_GAS_BRENNWERT))
        current_zustandszahl = options.get(CONF_GAS_ZUSTANDSZAHL, data.get(CONF_GAS_ZUSTANDSZAHL, DEFAULT_GAS_ZUSTANDSZAHL))
        current_price_helper = options.get(CONF_PRICE_HELPER, data.get(CONF_PRICE_HELPER, ""))
        current_brennwert_helper = options.get(CONF_GAS_BRENNWERT_HELPER, data.get(CONF_GAS_BRENNWERT_HELPER, ""))
        current_zustandszahl_helper = options.get(CONF_GAS_ZUSTANDSZAHL_HELPER, data.get(CONF_GAS_ZUSTANDSZAHL_HELPER, ""))
        
        # Base prices (monthly)
        if meter_type == METER_TYPE_STROM:
            current_base_price = options.get(CONF_BASE_PRICE_STROM, data.get(CONF_BASE_PRICE_STROM, DEFAULT_BASE_PRICE_STROM))
            current_base_price_helper = options.get(CONF_BASE_PRICE_STROM_HELPER, data.get(CONF_BASE_PRICE_STROM_HELPER, ""))
        else:
            current_base_price = options.get(CONF_BASE_PRICE_GAS, data.get(CONF_BASE_PRICE_GAS, DEFAULT_BASE_PRICE_GAS))
            current_base_price_helper = options.get(CONF_BASE_PRICE_GAS_HELPER, data.get(CONF_BASE_PRICE_GAS_HELPER, ""))

        if user_input is not None:
            # Entferne leere Helper-Entity-IDs aus der Eingabe
            cleaned_input = {k: v for k, v in user_input.items() if not (k.endswith("_helper") and not v)}
            return self.async_create_entry(title="", data=cleaned_input)

        # Build schema dynamically: only include helper fields if they have values
        schema_dict = {
            vol.Optional(CONF_PRICE_KWH, default=current_price): vol.Coerce(float),
        }
        
        # Only add entity selector if there's already a value configured
        if current_price_helper:
            schema_dict[vol.Optional(CONF_PRICE_HELPER, default=current_price_helper)] = selector.EntitySelector(
                selector.EntitySelectorConfig(domain=["input_number", "sensor"])
            )
        else:
            schema_dict[vol.Optional(CONF_PRICE_HELPER, default="")] = str
        
        # Base price (Grundpreis pro Monat)
        schema_dict[vol.Optional(CONF_BASE_PRICE_STROM if meter_type == METER_TYPE_STROM else CONF_BASE_PRICE_GAS, default=current_base_price)] = vol.Coerce(float)
        if current_base_price_helper:
            base_price_helper_key = CONF_BASE_PRICE_STROM_HELPER if meter_type == METER_TYPE_STROM else CONF_BASE_PRICE_GAS_HELPER
            schema_dict[vol.Optional(base_price_helper_key, default=current_base_price_helper)] = selector.EntitySelector(
                selector.EntitySelectorConfig(domain=["input_number", "sensor"])
            )
        else:
            base_price_helper_key = CONF_BASE_PRICE_STROM_HELPER if meter_type == METER_TYPE_STROM else CONF_BASE_PRICE_GAS_HELPER
            schema_dict[vol.Optional(base_price_helper_key, default="")] = str
        
        # Gas-specific fields: only show for gas meters
        if meter_type == METER_TYPE_GAS:
            schema_dict[vol.Optional(CONF_GAS_BRENNWERT, default=current_brennwert)] = vol.Coerce(float)
            
            if current_brennwert_helper:
                schema_dict[vol.Optional(CONF_GAS_BRENNWERT_HELPER, default=current_brennwert_helper)] = selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["input_number", "sensor"])
                )
            else:
                schema_dict[vol.Optional(CONF_GAS_BRENNWERT_HELPER, default="")] = str
                
            schema_dict[vol.Optional(CONF_GAS_ZUSTANDSZAHL, default=current_zustandszahl)] = vol.Coerce(float)
            
            if current_zustandszahl_helper:
                schema_dict[vol.Optional(CONF_GAS_ZUSTANDSZAHL_HELPER, default=current_zustandszahl_helper)] = selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=["input_number", "sensor"])
                )
            else:
                schema_dict[vol.Optional(CONF_GAS_ZUSTANDSZAHL_HELPER, default="")] = str

        schema = vol.Schema(schema_dict)

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
