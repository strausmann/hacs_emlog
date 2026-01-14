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

# Meter Types
METER_TYPE_STROM = "strom"
METER_TYPE_GAS = "gas"

# Meter Indices (1-4 möglich)
METER_INDICES = [1, 2, 3, 4]

# Defaults
DEFAULT_SCAN_INTERVAL = 30  # Sekunden
DEFAULT_PRICE_KWH = 0.0
DEFAULT_GAS_BRENNWERT = 11.58
DEFAULT_GAS_ZUSTANDSZAHL = 0.95
DEFAULT_BASE_PRICE_STROM = 0.0  # EUR/Monat
DEFAULT_BASE_PRICE_GAS = 0.0    # EUR/Monat
DEFAULT_MONTHLY_ADVANCE_STROM = 0.0  # EUR/Monat
DEFAULT_MONTHLY_ADVANCE_GAS = 0.0    # EUR/Monat
DEFAULT_SETTLEMENT_MONTH = 12  # Dezember (Monat 12)

EMLOG_EXPORT_PATH = "/pages/getinformation.php"
