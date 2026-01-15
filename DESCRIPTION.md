# Emlog (Electronic Meter Log) – Home Assistant Integration

A Home Assistant custom integration for Emlog devices by Weidmann Elektronik.

## Functionality

This integration reads electricity and gas meter data directly from the Emlog device and makes it available in Home Assistant. It offers:

### Sensors

- **Meter Readings** - Total consumption in kWh / m³
- **Power Sensors** - Current power in Watts (real-time)
- **Cost Sensors** - Daily costs calculated by the Emlog API
- **Price Sensors** - Configurable kWh prices for cost calculation

### Home Assistant Integration

- **Utility Meter Support** - Automatic daily, monthly, and yearly consumption aggregation
- **Config Flow** - User-friendly configuration via Home Assistant UI
- **Multi-Language** - German and English user interface
- **Multi-Meter** - Support for multiple Emlog devices simultaneously

### Advanced Features

- Dynamic helper entity integration for prices, calorific values, and gas density
- Flexible base prices (standing charges) for electricity and gas
- Installment payments and configurable billing date
- Automatic timezone usage instead of UTC
- Dynamic currency detection from API

## Installation

### Via HACS (coming soon)

1. HACS → Integrations → Search "Emlog"
2. Install
3. Restart Home Assistant

### Manual Installation (Custom Repository)

1. HACS → Integrations → Custom Repositories
2. URL: `https://github.com/strausmann/hacs_emlog`
3. Category: Integration
4. Install

## Configuration

After installation:

1. Settings → Devices & Services → Integrations
2. New Integration: "Emlog"
3. Enter Emlog device host IP or hostname
4. Configure meter indices (default: 1, 2)
5. Set scan interval (default: 30 seconds)

## Requirements

- Home Assistant 2024.1.0 or newer
- Emlog device accessible in local network
- HTTP access to Emlog API

## License

MIT - See LICENSE file

## Support

- 📖 [Documentation](https://github.com/strausmann/hacs_emlog)
- 🐛 [Issue Tracker](https://github.com/strausmann/hacs_emlog/issues)
- 💬 [Discussions](https://github.com/strausmann/hacs_emlog/discussions)

## Disclaimer

This is an unofficial integration and is not supported by Weidmann Elektronik (the manufacturer of Emlog). The integration was developed by the community.
