"""Template sensors for cost calculation in Emlog integration."""
from __future__ import annotations

from homeassistant.components.template import DOMAIN as TEMPLATE_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.template import Template
from homeassistant.helpers.template_entity import TemplateEntity
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass

from .const import (
    CONF_BASE_PRICE_STROM,
    CONF_BASE_PRICE_GAS,
    CONF_BASE_PRICE_STROM_HELPER,
    CONF_BASE_PRICE_GAS_HELPER,
    CONF_PRICE_KWH,
    CONF_PRICE_HELPER,
    DEFAULT_BASE_PRICE_STROM,
    DEFAULT_BASE_PRICE_GAS,
)


class EmlogCostSensor(TemplateEntity, SensorEntity):
    """Template sensor for cost calculation."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    # Unit wird dynamisch gesetzt via _currency

    def __init__(
        self,
        hass: HomeAssistant,
        meter_type: str,
        period: str,  # "tag", "monat", "jahr"
        entry: ConfigEntry,
    ):
        """Initialize cost sensor."""
        self.hass = hass
        self._meter_type = meter_type
        self._period = period
        self._entry = entry
        self._currency = "EUR"  # Default, wird später aktualisiert

        # Map period to German name
        period_name = {
            "tag": "Tag",
            "monat": "Monat",
            "jahr": "Jahr",
        }.get(period, period)

        meter_name = "Strom" if meter_type == "strom" else "Gas"
        self._attr_name = f"Emlog {meter_name} Kosten {period_name}"
        self._attr_unique_id = f"emlog_{meter_type}_kosten_{period}"

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement (currency from coordinator)."""
        return self._currency

    def _get_value_from_helper_or_config(
        self, helper_key: str, config_key: str, default_value: float
    ) -> float:
        """Get value from helper entity or config."""
        helper_id = self._entry.options.get(
            helper_key, self._entry.data.get(helper_key, "")
        )

        if helper_id:
            state = self.hass.states.get(helper_id)
            if state and state.state not in ("unknown", "unavailable"):
                try:
                    return float(state.state)
                except (ValueError, TypeError):
                    pass

        return float(
            self._entry.options.get(
                config_key, self._entry.data.get(config_key, default_value)
            )
        )

    @property
    def native_value(self) -> str | None:
        """Calculate cost: consumption × price + base_rate / days_in_period."""
        try:
            # Get consumption sensor
            consumption_sensor = f"sensor.emlog_{self._meter_type}_verbrauch_{self._period}_kwh"
            consumption_state = self.hass.states.get(consumption_sensor)
            if not consumption_state or consumption_state.state in (
                "unknown",
                "unavailable",
            ):
                return None

            consumption = float(consumption_state.state)

            # Get price per kWh
            price_kwh = self._get_value_from_helper_or_config(
                CONF_PRICE_HELPER, CONF_PRICE_KWH, 0.0
            )

            # Get base price (monthly rate)
            if self._meter_type == "strom":
                base_price = self._get_value_from_helper_or_config(
                    CONF_BASE_PRICE_STROM_HELPER,
                    CONF_BASE_PRICE_STROM,
                    DEFAULT_BASE_PRICE_STROM,
                )
            else:
                base_price = self._get_value_from_helper_or_config(
                    CONF_BASE_PRICE_GAS_HELPER,
                    CONF_BASE_PRICE_GAS,
                    DEFAULT_BASE_PRICE_GAS,
                )

            # Calculate cost
            if self._period == "tag":
                # Daily: consumption × price + (base_price / 30 days)
                cost = (consumption * price_kwh) + (base_price / 30)
            elif self._period == "monat":
                # Monthly: consumption × price + base_price
                cost = (consumption * price_kwh) + base_price
            elif self._period == "jahr":
                # Yearly: consumption × price + (base_price × 12 months)
                cost = (consumption * price_kwh) + (base_price * 12)
            else:
                return None

            return round(cost, 2)

        except Exception:
            return None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Emlog cost sensors from a config entry."""
    meter_type = entry.data.get("meter_type")

    entities = []

    # Create cost sensors for day/month/year
    for period in ["tag", "monat", "jahr"]:
        entities.append(EmlogCostSensor(hass, meter_type, period, entry))

    async_add_entities(entities)
