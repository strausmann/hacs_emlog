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

## Entwicklung & Testen

### Lokale Entwicklungsumgebung

Das Projekt enthält eine vollständige Entwicklungsumgebung für GitHub Codespaces:

- **Dev Container**: Vollständige Python/Home Assistant Umgebung
- **Mock Server**: Simuliert Emlog API ohne echte Hardware
- **Test Scripts**: Automatisierte Tests für API und Integration

### Testen ohne echte Hardware

```bash
# Starte Mock Server und führe Tests durch
./test.sh
```

Oder manuell:
```bash
# Mock Server starten
docker-compose -f docker-compose.test.yml up -d emlog-mock

# API testen
curl "http://localhost:8080/pages/getinformation.php?export&meterindex=1"

# Home Assistant mit Test-Konfiguration starten
docker-compose -f docker-compose.test.yml up homeassistant
```

### Mit echter Emlog Hardware

Für Tests mit echter Hardware:
1. Stelle sicher, dass der Emlog Server im gleichen Netzwerk erreichbar ist
2. Verwende die echte IP-Adresse in der Konfiguration
3. Bei Bedarf Tailscale oder VPN für Remote-Zugriff einrichten

## Support
Issues/Feature Requests bitte über GitHub Issues.
