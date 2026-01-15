DOMAIN = "emlog"

# Config
CONF_HOST = "host"
CONF_METER_INDEX = "meter_index"
CONF_PRICE_KWH = "price_kwh"
CONF_GAS_BRENNWERT = "gas_brennwert"
CONF_GAS_ZUSTANDSZAHL = "gas_zustandszahl"
CONF_PRICE_HELPER = "price_helper"
CONF_GAS_BRENNWERT_HELPER = "gas_brennwert_helper"
CONF_GAS_ZUSTANDSZAHL_HELPER = "gas_zustandszahl_helper"
CONF_BASE_PRICE_STROM = "base_price_strom"
CONF_BASE_PRICE_GAS = "base_price_gas"
CONF_BASE_PRICE_STROM_HELPER = "base_price_strom_helper"
CONF_BASE_PRICE_GAS_HELPER = "base_price_gas_helper"
CONF_MONTHLY_ADVANCE_STROM = "monthly_advance_strom"
CONF_MONTHLY_ADVANCE_GAS = "monthly_advance_gas"
CONF_MONTHLY_ADVANCE_STROM_HELPER = "monthly_advance_strom_helper"
CONF_MONTHLY_ADVANCE_GAS_HELPER = "monthly_advance_gas_helper"
CONF_SETTLEMENT_MONTH = "settlement_month"
CONF_METER_TYPE = "meter_type"  # "strom" oder "gas"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_INCLUDE_FEED_IN_SENSORS = "include_feed_in_sensors"

# Tarifwechsel (für Preisänderungen)
CONF_PRICE_CHANGE_DATE_STROM = "price_change_date_strom"
CONF_PRICE_CHANGE_DATE_GAS = "price_change_date_gas"
CONF_PRICE_KWH_NEW_STROM = "price_kwh_new_strom"
CONF_PRICE_KWH_NEW_GAS = "price_kwh_new_gas"
CONF_PRICE_KWH_NEW_STROM_HELPER = "price_kwh_new_strom_helper"
CONF_PRICE_KWH_NEW_GAS_HELPER = "price_kwh_new_gas_helper"
CONF_BASE_PRICE_STROM_NEW = "base_price_strom_new"
CONF_BASE_PRICE_GAS_NEW = "base_price_gas_new"
CONF_BASE_PRICE_STROM_NEW_HELPER = "base_price_strom_new_helper"
CONF_BASE_PRICE_GAS_NEW_HELPER = "base_price_gas_new_helper"

# Meter Types
METER_TYPE_STROM = "strom"
METER_TYPE_GAS = "gas"

# Meter Indices
METER_INDICES = [1, 2, 3, 4]

# Defaults
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PRICE_KWH = 0.0
DEFAULT_BASE_PRICE_STROM = 0.0
DEFAULT_BASE_PRICE_GAS = 0.0
DEFAULT_MONTHLY_ADVANCE_STROM = 0.0
DEFAULT_MONTHLY_ADVANCE_GAS = 0.0
DEFAULT_SETTLEMENT_MONTH = 12
DEFAULT_GAS_BRENNWERT = 10.88
DEFAULT_GAS_ZUSTANDSZAHL = 1.0

# API
EMLOG_EXPORT_PATH = "/pages/getinformation.php"
