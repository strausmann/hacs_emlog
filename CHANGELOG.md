# Emlog Home Assistant Integration Change Log 📜📝

All notable changes to the **Emlog Home Assistant Integration** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0](https://github.com/strausmann/hacs_emlog/compare/v0.5.0...v0.6.0) (2026-01-14)

### Features

* **config:** add base price fields and entity selectors to options flow ([5e4a2c6](https://github.com/strausmann/hacs_emlog/commit/5e4a2c6a0f178704b48506082b64efbd3049382c))
* **const:** add base price constants for electricity and gas ([0d236fc](https://github.com/strausmann/hacs_emlog/commit/0d236fc7fb4743c50462ea1dbba08ec062a0ff2a))
* **coordinator:** store config_entry for property-based value resolution ([230b277](https://github.com/strausmann/hacs_emlog/commit/230b27788b54eddf5c7fcca594ddb2ba56ffff7b))
* **makefile:** add workflow URL display after release-github trigger ([1e4c4d9](https://github.com/strausmann/hacs_emlog/commit/1e4c4d95bb3409d8449c8c72dc82caa4aa4b3b1f))
* **manifest:** bump version to 0.2.0 and require HA 2024.1.0 ([42f58c5](https://github.com/strausmann/hacs_emlog/commit/42f58c59734bfd1444c0786f19d6cb39929b81f3))
* **sensor:** implement property-based value resolution and update entity names ([1f6c52f](https://github.com/strausmann/hacs_emlog/commit/1f6c52f093edb590700b98fef7b032331bbe8f8b))
* **template:** add cost sensor class with day/month/year consumption calculation ([17fa341](https://github.com/strausmann/hacs_emlog/commit/17fa34122f72717ac53aa78ea2273006a9c9dff6))
* **translations:** add base price field descriptions (de + en) ([73460b2](https://github.com/strausmann/hacs_emlog/commit/73460b229fbfc65ca7073dce29b56384983da337))

### Bug Fixes

* **__init__:** remove broken async_setup_utility_meter import ([32163f4](https://github.com/strausmann/hacs_emlog/commit/32163f43952773b1b7d972dcdcd2be678c03eca7))

## [0.5.0](https://github.com/strausmann/hacs_emlog/compare/v0.4.0...v0.5.0) (2026-01-14)

### Features

* **makefile:** add release-github command to trigger remote GitHub Actions release ([d646072](https://github.com/strausmann/hacs_emlog/commit/d6460724f05071457296b8de7b551488efe11a74))
* **test:** add test file for release testing ([afded2e](https://github.com/strausmann/hacs_emlog/commit/afded2e835a840345ae10a356618d061225f51b6))

### Bug Fixes

* **makefile:** add CI=true to release command for proper semantic-release execution ([2ee4677](https://github.com/strausmann/hacs_emlog/commit/2ee4677372972a72525d8749489bada9c3aa6962))

## [Unreleased]

## [0.4.0](https://github.com/strausmann/hacs_emlog/compare/v0.3.0...v0.4.0) (2026-01-14)

### Features

* update semantic release configuration with emoji-based changelog ([b94226f](https://github.com/strausmann/hacs_emlog/commit/b94226f7441a9b13837213e5f8441d5f803fbbf2))

### Bug Fixes

* **changelog:** remove duplicate 0.1.0 section and fix debug config ([be8b8b1](https://github.com/strausmann/hacs_emlog/commit/be8b8b15c534f525a7cd8b52d694d581179a1a9c))
* **docker:** adjust compose.yml paths for tools/docker directory ([dd86b99](https://github.com/strausmann/hacs_emlog/commit/dd86b99d9c57ab8c2e60b0c581ca942cbc0e8945))
* **mock:** implement realistic power consumption simulation ([aeb0dc5](https://github.com/strausmann/hacs_emlog/commit/aeb0dc54d589e64b09246e2f0ab08cde6152b902))
* **mock:** resolve API timeout by moving update_loop outside main block ([fb22816](https://github.com/strausmann/hacs_emlog/commit/fb22816d25c4a3bd39317b2bc4b55e71ee3c14ee))

## [0.3.0](https://github.com/strausmann/hacs_emlog/compare/v0.2.0...v0.3.0) (2026-01-14)

### ✨ Features

* update semantic release configuration with emoji-based changelog ([43effe3](https://github.com/strausmann/hacs_emlog/commit/43effe3b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b))

## [0.2.0](https://github.com/strausmann/hacs_emlog/compare/v0.1.0...v0.2.0) (2026-01-14)

### ✨ Features

* integrate Commitlint with German prompts for conventional commits ([be34601](https://github.com/strausmann/hacs_emlog/commit/be3460164649f4a234cd4fbb0ee6fb5533ec9943))
* integrate Prettier code formatting and update changelog format ([914eea7](https://github.com/strausmann/hacs_emlog/commit/914eea7b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b))

### 📚 Documentation

* document commit conventions and interactive commit workflow ([def71c8](https://github.com/strausmann/hacs_emlog/commit/def71c8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b))
* document Prettier code formatting in contribution guidelines ([be52092](https://github.com/strausmann/hacs_emlog/commit/be52092b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b))

## [0.1.0](https://github.com/strausmann/hacs_emlog/compare/v0.0.0...v0.1.0) (2026-01-14)

### ✨ Features

* **HACS Integration**: Initial Home Assistant Custom Component for Emlog devices
  * Coordinator pattern for HTTP polling of Emlog API endpoints
  * Config flow for user-friendly setup (host, meter indices, scan interval)
  * Sensor entities for electricity and gas meter data
  * German and English translations
  * Local polling integration with proper error handling

* **Development Environment**: Complete setup for GitHub Codespaces
  * Dev container with Python 3.11, Docker-in-Docker, and Home Assistant
  * VS Code extensions for Python development (Black, isort, Pylint)
  * Port forwarding for Home Assistant (port 8123)

* **Testing Infrastructure**: Mock server and automated testing
  * Flask-based mock server simulating Emlog API responses
  * Realistic JSON data for electricity (meter index 1) and gas (meter index 2)
  * Docker Compose setup for isolated testing
  * Automated test script (`test.sh`) for API validation
  * Test configuration for Home Assistant

* **Documentation**: Comprehensive guides for development and usage
  * AI coding guidelines in `.github/copilot-instructions.md`
  * Updated README with development and testing instructions
  * Migration context from YAML package to HACS integration

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

[Unreleased]: https://github.com/strausmann/hacs_emlog/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/strausmann/hacs_emlog/releases/tag/v0.4.0
[0.3.0]: https://github.com/strausmann/hacs_emlog/releases/tag/v0.3.0
[0.2.0]: https://github.com/strausmann/hacs_emlog/releases/tag/v0.2.0
[0.1.0]: https://github.com/strausmann/hacs_emlog/releases/tag/v0.1.0
