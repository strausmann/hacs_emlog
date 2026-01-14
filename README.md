# Emlog (Electronic Meter Log) – Home Assistant Integration (HACS)

Diese Integration liest Daten aus dem Emlog-Endpoint (z. B. `getinformation.php?export&meterindex=...`).

## Installation (HACS Custom Repository)

1. HACS → Integrationen → Menü (⋮) → **Custom Repositories**
2. Repo-URL eintragen (dieses Repository)
3. Kategorie: **Integration**
4. Installieren → Home Assistant neu starten
5. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → **Emlog**

## Konfiguration

Im UI-Setup:
- Host/IP (ohne http://)
- Strom Meterindex
- Gas Meterindex
- Scan-Intervall

## Entities (MVP)
- Strom: Zählerstand (kWh), Wirkleistung (W), Tagesverbrauch (kWh)
- Gas: Zählerstand (m³), Wirkleistung (W), Tagesverbrauch (kWh)

## Hinweise
- Diese Integration ist **local_polling**.
- Für Kosten/Tarife kannst du zusätzlich das beiliegende YAML-Package nutzen (Ordner `packages/`).

## Support
Issues/Feature Requests bitte über GitHub Issues.
