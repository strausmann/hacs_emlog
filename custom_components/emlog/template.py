"""Template sensors for cost calculation in Emlog integration."""
from __future__ import annotations

from datetime import datetime

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
    CONF_BASE_PRICE_STROM_NEW,
    CONF_BASE_PRICE_GAS_NEW,
    CONF_BASE_PRICE_STROM_NEW_HELPER,
    CONF_BASE_PRICE_GAS_NEW_HELPER,
    CONF_PRICE_KWH,
    CONF_PRICE_HELPER,
    CONF_PRICE_KWH_NEW_STROM,
    CONF_PRICE_KWH_NEW_GAS,
    CONF_PRICE_KWH_NEW_STROM_HELPER,
    CONF_PRICE_KWH_NEW_GAS_HELPER,
    CONF_PRICE_CHANGE_DATE_STROM,
    CONF_PRICE_CHANGE_DATE_GAS,
    CONF_MONTHLY_ADVANCE_STROM,
    CONF_MONTHLY_ADVANCE_GAS,
    CONF_MONTHLY_ADVANCE_STROM_HELPER,
    CONF_MONTHLY_ADVANCE_GAS_HELPER,
    DEFAULT_BASE_PRICE_STROM,
    DEFAULT_BASE_PRICE_GAS,
    DEFAULT_MONTHLY_ADVANCE_STROM,
    DEFAULT_MONTHLY_ADVANCE_GAS,
    METER_TYPE_STROM,
    METER_TYPE_GAS,
)


class EmlogCostSensor(SensorEntity):
    """Sensor for cost calculation with tariff change support."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(
        self,
        hass: HomeAssistant,
        meter_type: str,
        meter_index: int,
        period: str,  # "tag", "monat", "jahr"
        entry: ConfigEntry,
    ):
        """Initialize cost sensor."""
        self.hass = hass
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._period = period
        self._entry = entry
        self._currency = "EUR"
        self._attr_should_poll = True

        # Map period to German name
        period_name = {
            "tag": "Tag",
            "monat": "Monat",
            "jahr": "Jahr",
        }.get(period, period)

        meter_name = "Strom" if meter_type == METER_TYPE_STROM else "Gas"
        self._attr_name = f"Emlog {meter_name} {meter_index} Kosten {period_name}"
        self._attr_unique_id = f"emlog_{meter_type}_{meter_index}_kosten_{period}"

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement (currency)."""
        return self._currency

    def _get_value_from_helper_or_config(
        self, helper_key: str, config_key: str, default_value: float
    ) -> float:
        """Get value from helper entity or config with fallback."""
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

    def _get_config_for_meter_type(self, config_type: str) -> tuple:
        """Get configuration keys for current meter type."""
        if config_type == "price":
            if self._meter_type == METER_TYPE_STROM:
                return (
                    CONF_PRICE_CHANGE_DATE_STROM,
                    CONF_PRICE_KWH_NEW_STROM_HELPER,
                    CONF_PRICE_KWH_NEW_STROM,
                    CONF_PRICE_HELPER,
                    CONF_PRICE_KWH,
                )
            else:
                return (
                    CONF_PRICE_CHANGE_DATE_GAS,
                    CONF_PRICE_KWH_NEW_GAS_HELPER,
                    CONF_PRICE_KWH_NEW_GAS,
                    CONF_PRICE_HELPER,
                    CONF_PRICE_KWH,
                )
        elif config_type == "base_price":
            if self._meter_type == METER_TYPE_STROM:
                return (
                    CONF_PRICE_CHANGE_DATE_STROM,
                    CONF_BASE_PRICE_STROM_NEW_HELPER,
                    CONF_BASE_PRICE_STROM_NEW,
                    CONF_BASE_PRICE_STROM_HELPER,
                    CONF_BASE_PRICE_STROM,
                    DEFAULT_BASE_PRICE_STROM,
                )
            else:
                return (
                    CONF_PRICE_CHANGE_DATE_GAS,
                    CONF_BASE_PRICE_GAS_NEW_HELPER,
                    CONF_BASE_PRICE_GAS_NEW,
                    CONF_BASE_PRICE_GAS_HELPER,
                    CONF_BASE_PRICE_GAS,
                    DEFAULT_BASE_PRICE_GAS,
                )
        return ()

    def _get_effective_value_with_tariff_change(
        self, config_type: str, default_value: float = 0.0
    ) -> float:
        """Get effective value considering tariff change date."""
        config = self._get_config_for_meter_type(config_type)
        change_date_key = config[0]
        new_helper_key = config[1]
        new_key = config[2]
        current_helper_key = config[3]
        current_key = config[4]
        default = config[5] if len(config) > 5 else default_value

        # Check if tariff change date has passed
        change_date_str = self._entry.options.get(
            change_date_key, self._entry.data.get(change_date_key, "")
        )

        if change_date_str:
            try:
                change_date = datetime.strptime(change_date_str, "%Y-%m-%d").date()
                if datetime.now().date() >= change_date:
                    # Use new value
                    return self._get_value_from_helper_or_config(
                        new_helper_key, new_key, 0.0
                    )
            except ValueError:
                pass

        # Use current value
        return self._get_value_from_helper_or_config(
            current_helper_key, current_key, default
        )

    def _get_effective_price(self) -> float:
        """Get effective price considering tariff change date."""
        return self._get_effective_value_with_tariff_change("price", 0.0)

    def _get_effective_base_price(self) -> float:
        """Get effective base price considering tariff change date."""
        return self._get_effective_value_with_tariff_change("base_price")

    @property
    def native_value(self) -> float | None:
        """Calculate cost: consumption × price + base_rate / days_in_period."""
        try:
            # Get consumption sensor with meter_index
            consumption_sensor = f"sensor.emlog_{self._meter_type}_{self._meter_index}_verbrauch_{self._period}_kwh"
            consumption_state = self.hass.states.get(consumption_sensor)
            if not consumption_state or consumption_state.state in (
                "unknown",
                "unavailable",
            ):
                return None

            consumption = float(consumption_state.state)

            # Get effective prices with tariff change consideration
            price_kwh = self._get_effective_price()
            base_price = self._get_effective_base_price()

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


class EmlogAdvanceTotalSensor(SensorEntity):
    """Calculate total yearly advance payment (monthly_advance × 12)."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_should_poll = True

    def __init__(
        self,
        hass: HomeAssistant,
        meter_type: str,
        meter_index: int,
        entry: ConfigEntry,
    ):
        """Initialize advance total sensor."""
        self.hass = hass
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._entry = entry
        self._currency = "EUR"

        meter_name = "Strom" if meter_type == METER_TYPE_STROM else "Gas"
        self._attr_name = f"Emlog {meter_name} {meter_index} Abschlag Jahresgesamt"
        self._attr_unique_id = f"emlog_{meter_type}_{meter_index}_advance_total"

    @property
    def unit_of_measurement(self) -> str:
        """Return currency."""
        return self._currency

    def _get_monthly_advance_config_keys(self) -> tuple:
        """Get config keys for monthly advance based on meter type."""
        if self._meter_type == METER_TYPE_STROM:
            return (
                CONF_MONTHLY_ADVANCE_STROM_HELPER,
                CONF_MONTHLY_ADVANCE_STROM,
                DEFAULT_MONTHLY_ADVANCE_STROM,
            )
        else:
            return (
                CONF_MONTHLY_ADVANCE_GAS_HELPER,
                CONF_MONTHLY_ADVANCE_GAS,
                DEFAULT_MONTHLY_ADVANCE_GAS,
            )

    def _get_advance_value(self) -> float:
        """Get monthly advance value from helper or config."""
        helper_key, config_key, default = self._get_monthly_advance_config_keys()

        helper_id = self._entry.options.get(helper_key, self._entry.data.get(helper_key, ""))
        if helper_id:
            state = self.hass.states.get(helper_id)
            if state and state.state not in ("unknown", "unavailable"):
                try:
                    return float(state.state)
                except (ValueError, TypeError):
                    pass

        return float(self._entry.options.get(config_key, self._entry.data.get(config_key, default)))

    @property
    def native_value(self) -> float | None:
        """Calculate yearly advance: monthly_advance × 12."""
        try:
            monthly_advance = self._get_advance_value()
            return round(monthly_advance * 12, 2)
        except Exception:
            return None


class EmlogAdvanceDifferenceSensor(SensorEntity):
    """Calculate difference between yearly costs and advance payments."""

    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_should_poll = True

    def __init__(
        self,
        hass: HomeAssistant,
        meter_type: str,
        meter_index: int,
        entry: ConfigEntry,
    ):
        """Initialize advance difference sensor."""
        self.hass = hass
        self._meter_type = meter_type
        self._meter_index = meter_index
        self._entry = entry
        self._currency = "EUR"

        meter_name = "Strom" if meter_type == METER_TYPE_STROM else "Gas"
        self._attr_name = f"Emlog {meter_name} {meter_index} Abschlag Differenz"
        self._attr_unique_id = f"emlog_{meter_type}_{meter_index}_advance_difference"

    @property
    def unit_of_measurement(self) -> str:
        """Return currency."""
        return self._currency

    def _get_monthly_advance(self) -> float:
        """Get monthly advance value from helper or config."""
        if self._meter_type == METER_TYPE_STROM:
            helper_key = CONF_MONTHLY_ADVANCE_STROM_HELPER
            config_key = CONF_MONTHLY_ADVANCE_STROM
            default = DEFAULT_MONTHLY_ADVANCE_STROM
        else:
            helper_key = CONF_MONTHLY_ADVANCE_GAS_HELPER
            config_key = CONF_MONTHLY_ADVANCE_GAS
            default = DEFAULT_MONTHLY_ADVANCE_GAS

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
                config_key, self._entry.data.get(config_key, default)
            )
        )

    @property
    def native_value(self) -> float | None:
        """Calculate difference: yearly_cost - (monthly_advance × 12).

        Positive value: Customer paid too much (should get refund)
        Negative value: Customer paid too little (should pay more)
        """
        try:
            # Get yearly cost sensor with meter_index
            yearly_cost_sensor = f"sensor.emlog_{self._meter_type}_{self._meter_index}_kosten_jahr"
            yearly_cost_state = self.hass.states.get(yearly_cost_sensor)
            if not yearly_cost_state or yearly_cost_state.state in (
                "unknown",
                "unavailable",
            ):
                return None
            yearly_cost = float(yearly_cost_state.state)

            monthly_advance = self._get_monthly_advance()
            yearly_advance = monthly_advance * 12
            difference = yearly_cost - yearly_advance

            return round(difference, 2)

        except Exception:
            return None


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Emlog cost and advance sensors from a config entry."""
    meter_type = entry.data.get("meter_type")
    meter_index = entry.data.get("meter_index")

    entities = []

    # Create cost sensors for day/month/year
    for period in ["tag", "monat", "jahr"]:
        entities.append(EmlogCostSensor(hass, meter_type, meter_index, period, entry))

    # Create advance payment sensors
    entities.append(EmlogAdvanceTotalSensor(hass, meter_type, meter_index, entry))
    entities.append(EmlogAdvanceDifferenceSensor(hass, meter_type, meter_index, entry))

    async_add_entities(entities)
