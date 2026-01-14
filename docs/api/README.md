# 🔌 Emlog API Referenz

Vollständige Dokumentation der Emlog HTTP-API und Datenstruktur.

## 📍 Endpoints

### Meter Information
```
GET http://{host}:80/pages/getinformation.php?export&meterindex={index}
```

**Parameter:**
- `host`: IP-Adresse des Emlog Geräts (z.B. 192.168.1.100)
- `meterindex`: Meter-Index (Integer, typisch 1 für Strom, 2 für Gas)
- `export`: Aktiviert JSON Export Format

**Response:** JSON mit vollständigen Meter-Daten

## 📋 Response Struktur

### Grundgerüst
```json
{
  "product": "Emlog - Electronic Meter Log",
  "version": 1.16,
  
  "Zaehlerstand_Bezug": {},      // Zählerstände (Bezug)
  "Zaehlerstand_Lieferung": {},  // Zählerstände (Lieferung)
  
  "Wirkleistung_Bezug": {},      // Leistung (Bezug)
  "Wirkleistung_Lieferung": {},  // Leistung (Lieferung)
  
  "Kwh_Bezug": {},               // kWh Verbrauch
  "Kwh_Lieferung": {},           // kWh Erzeugung
  
  "Betrag_Bezug": {},            // Kosten (Bezug)
  "Betrag_Lieferung": {},        // Kosten (Lieferung)
  
  "DiffBezugLieferung": {}       // Differenz Bezug/Lieferung
}
```

## 🔋 Elektrischer Strom (Meterindex 1)

### Zählerstände (Zaehlerstand_Bezug)
```json
{
  "Stand180": 12345.67,      // Gesamtzähler (kWh)
  "Stand181": 1000.00,       // Tarif 1 (kWh) - Niedertarif
  "Stand182": 2345.67,       // Tarif 2 (kWh) - Hochtarif
  "Stand183": 9000.00        // (optional) Tarif 3 (kWh)
}
```

### Zählerstände (Zaehlerstand_Lieferung)
```json
{
  "Stand280": 5000.00,       // Gesamtzähler PV Erzeugung (kWh)
  "Stand281": 3000.00,       // Tarif 1 PV (kWh)
  "Stand282": 2000.00        // Tarif 2 PV (kWh)
}
```

### Aktuelle Leistung (Wirkleistung_Bezug) in W
```json
{
  "Leistung170": 1500,       // Phase L1 (W)
  "Leistung171": 1600,       // Phase L2 (W)
  "Leistung172": 1700,       // Phase L3 (W)
  "Leistung173": 1500        // Summe aller Phasen (W)
}
```

### Aktuelle Leistung (Wirkleistung_Lieferung) in W
```json
{
  "Leistung270": 500,        // Phase L1 PV (W)
  "Leistung271": 400,        // Phase L2 PV (W)
  "Leistung272": 300,        // Phase L3 PV (W)
  "Leistung273": 500         // Summe PV (W)
}
```

### Verbrauch & Kosten
```json
// Kwh_Bezug: Kumulierte Kilowattstunden
{
  "Kwh180": 12345.67,        // Gesamtverbrauch (kWh)
  "Kwh181": 1000.00,         // Tarif 1 Verbrauch (kWh)
  "Kwh182": 2345.67          // Tarif 2 Verbrauch (kWh)
}

// Betrag_Bezug: Kosten
{
  "Betrag180": 3500.00,      // Gesamtkosten (EUR)
  "Betrag181": 1000.00,      // Tarif 1 Kosten (EUR)
  "Betrag182": 2500.00,      // Tarif 2 Kosten (EUR)
  "Waehrung": "EUR"          // Währung
}
```

## 🔥 Gas (Meterindex 2)

### Zählerstände (Zaehlerstand_Bezug)
```json
{
  "Stand180": 100000.5,      // Gesamtzähler (m³)
  "Stand181": 50000.0,       // Tarif 1 (m³)
  "Stand182": 50000.5        // Tarif 2 (m³)
}
```

### Aktuelle Leistung (Wirkleistung_Bezug) in W
```json
{
  "Leistung170": 15000,      // Momentane Leistung (W)
  "Leistung171": 0,
  "Leistung172": 0,
  "Leistung173": 15000       // Summe (W)
}
```

### Verbrauch (Kwh_Bezug) in kWh
```json
{
  "Kwh180": 1000000.0,       // Gesamtverbrauch (kWh)
  "Kwh181": 500000.0,        // Tarif 1 (kWh)
  "Kwh182": 500000.0         // Tarif 2 (kWh)
}
```

## 💹 Sensor-Mapping in Integration

### Von JSON zu Home Assistant Sensoren

```python
# Electricity Sensors (Meterindex 1)
STROM_SENSORS = [
    # Zählerstände
    EmlogSensorDef("zaehlerstand_kwh", ..., "Stand180"),
    EmlogSensorDef("tarif1_kwh", ..., "Stand181"),
    EmlogSensorDef("tarif2_kwh", ..., "Stand182"),
    
    # Aktuelle Leistung
    EmlogSensorDef("leistung_w", ..., "Leistung173"),
    EmlogSensorDef("leistung_l1_w", ..., "Leistung170"),
    
    # Verbrauch
    EmlogSensorDef("verbrauch_kwh", ..., "Kwh180"),
]

# Gas Sensors (Meterindex 2)
GAS_SENSORS = [
    EmlogSensorDef("gas_zaehlerstand_m3", ..., "Stand180"),
    EmlogSensorDef("gas_leistung_w", ..., "Leistung173"),
]
```

## 📊 Datentypen & Einheiten

### Zählerstände
- **Datentyp:** Float (Dezimal)
- **Einheit:** kWh (Strom), m³ (Gas)
- **State Class:** `TOTAL_INCREASING` (steigt immer/bleibt gleich)
- **Device Class:** `ENERGY`, `VOLUME`

### Leistung
- **Datentyp:** Integer
- **Einheit:** W (Watt)
- **State Class:** `MEASUREMENT` (kann variieren)
- **Device Class:** `POWER`

### Kosten
- **Datentyp:** Float (Dezimal)
- **Einheit:** EUR, andere Währungen möglich
- **State Class:** `TOTAL` oder `TOTAL_INCREASING`
- **Device Class:** `MONETARY`

## 🔄 Beispiel-Requests

### cURL
```bash
# Strom abrufen
curl "http://192.168.1.100/pages/getinformation.php?export&meterindex=1"

# Gas abrufen
curl "http://192.168.1.100/pages/getinformation.php?export&meterindex=2"
```

### Python
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    url = "http://192.168.1.100/pages/getinformation.php"
    params = {"export": "", "meterindex": 1}
    
    async with session.get(url, params=params, timeout=10) as resp:
        data = await resp.json(content_type=None)
        
        # Extrahiere Zählerstand
        zaehler = data.get("Zaehlerstand_Bezug", {}).get("Stand180", 0)
        print(f"Zählerstand: {zaehler} kWh")
```

## ⚠️ Fehlerbehandlung

### Mögliche Fehler

| Status | Ursache | Lösung |
|--------|---------|--------|
| 404 | Endpoint nicht erreichbar | Prüfe IP & Port |
| 500 | Server Error | Emlog Device Neustart |
| Timeout | Netzwerkprobleme | Netzwerk prüfen, Timeout erhöhen |
| JSON Error | Ungültiges Response Format | Emlog Version prüfen |

### Integration Error Handling
```python
try:
    async with session.get(url, timeout=10) as resp:
        if resp.status != 200:
            raise UpdateFailed(f"HTTP {resp.status}")
        return await resp.json(content_type=None)
        
except asyncio.TimeoutError as err:
    raise UpdateFailed(f"Timeout: {url}") from err
    
except aiohttp.ClientError as err:
    raise UpdateFailed(f"Connection error: {err}") from err
    
except json.JSONDecodeError as err:
    raise UpdateFailed(f"Invalid JSON response: {err}") from err
```

## 🧪 Mock Server

Für Tests ohne physisches Emlog Gerät:

```bash
# Mock Server starten
make mock-up

# API testen
curl "http://localhost:8080/pages/getinformation.php?export&meterindex=1"
```

Der Mock Server simuliert realistische Daten mit:
- Zufälliger Variation (Leistung)
- Täglichen Zyklen (Gasverbrauch)
- Persistenten Zählern (state.json)

## 📚 Weitere Ressourcen

- [Emlog Handbuch](https://www.emlog.de/) (Hersteller)
- [Integration Architektur](./architecture.md)
- [Testing Guide](./testing.md)
- [GitHub Issues](https://github.com/strausmann/hacs_emlog/issues)

---

**API Version:** 1.16 (aktuell in Emlog)  
**Zuletzt aktualisiert:** 2025-01-15
