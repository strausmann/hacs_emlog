# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-14

### Added
- **HACS Integration**: Initial Home Assistant Custom Component for Emlog devices
  - Coordinator pattern for HTTP polling of Emlog API endpoints
  - Config flow for user-friendly setup (host, meter indices, scan interval)
  - Sensor entities for electricity and gas meter data
  - German and English translations
  - Local polling integration with proper error handling

- **Development Environment**: Complete setup for GitHub Codespaces
  - Dev container with Python 3.11, Docker-in-Docker, and Home Assistant
  - VS Code extensions for Python development (Black, isort, Pylint)
  - Port forwarding for Home Assistant (port 8123)

- **Testing Infrastructure**: Mock server and automated testing
  - Flask-based mock server simulating Emlog API responses
  - Realistic JSON data for electricity (meter index 1) and gas (meter index 2)
  - Docker Compose setup for isolated testing
  - Automated test script (`test.sh`) for API validation
  - Test configuration for Home Assistant

- **Documentation**: Comprehensive guides for development and usage
  - AI coding guidelines in `.github/copilot-instructions.md`
  - Updated README with development and testing instructions
  - Migration context from YAML package to HACS integration

### Changed
- **Package Configuration**: Updated `package/emlog.yaml` for consistency
- **Project Structure**: Organized development and testing files

### Fixed
- **Dev Container**: Replaced incorrect `.devcontainer` file with proper `devcontainer.json`

### Migration Notes
- **From YAML Package to HACS**: The integration provides core sensor functionality
- **Legacy Support**: Original `package/emlog.yaml` remains for advanced features (cost calculations, tariff switching, utility meters)
- **Future Development**: HACS integration will eventually include all package features

### Technical Details
- **API Endpoint**: `http://{host}/pages/getinformation.php?export&meterindex={index}`
- **Data Structure**: Nested JSON with fields like `Zaehlerstand_Bezug.Stand180`, `Wirkleistung_Bezug.Leistung170`
- **Unique IDs**: Format `emlog_{host}_{channel}_{key}` with dots replaced by underscores
- **Error Handling**: Timeout handling and proper UpdateFailed exceptions

---

## Migration Guide

### From YAML Package to HACS Integration

1. **Install via HACS**: Add this repository as a custom integration
2. **Configure**: Use the UI setup to configure host and meter indices
3. **Advanced Features**: Continue using `package/emlog.yaml` for cost calculations and utility meters
4. **Testing**: Use the new mock server for development without physical hardware

### Development Setup

1. **GitHub Codespaces**: Automatic setup with dev container
2. **Local Testing**: Run `./test.sh` for automated testing
3. **Mock Server**: Simulates Emlog API for development

---

[Unreleased]: https://github.com/strausmann/hacs_emlog/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/strausmann/hacs_emlog/releases/tag/v0.1.0