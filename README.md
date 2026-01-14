# Emlog (Electronic Meter Log) – Home Assistant Integration

Diese Integration liest Energie- und Gaszählerdaten direkt vom Emlog-Gerät und macht sie in Home Assistant verfügbar. Sie bietet vollständige Automatisierung zur Datenerfassung mit erweiterten Konfigurationsoptionen für Tarifberechnungen.

## ✨ Features

### Kerneigenschaften
- 📡 **Automatisches Daten-Polling** - Regelmäßiges Auslesen der Emlog-API
- 🌐 **Dynamische Währungserkennung** - Währung wird automatisch von der API ausgelesen
- 🕐 **Automatische Timezone-Nutzung** - Verwendet die konfigurierte HA-Timezone statt UTC
- 🔄 **Utility Meter Integration** - Erstellt automatisch tägliche/monatliche/jährliche Verbrauchsmesser
- 🎯 **Flexible Helfer-Integration** - Nutze `input_number` Entities für dynamische Werte (Preise, Faktoren)
- ⚡ **Multi-Meter Support** - Unterstütze mehrere Emlog-Geräte gleichzeitig

### Sensoren
- **Zählerstände** (in kWh / m³) - Gesamtverbrauch mit verschiedenen Tarifen
- **Leistungssensoren** (in W) - Aktuelle Leistung in Echtzeit
- **Betrag-Sensoren** - Tagesaktuelle Kosten von der Emlog API
- **Preis-Sensoren** - Konfigurierbare kWh-Preise
- **Utility Meter** - Automatische tägliche/monatliche/jährliche Aggregationen
- **Status-Sensoren** - API-Verbindungsstatus und letzte Fehlermeldung

### Erweiterte Features
- 🏷️ **Basis-Preise** (Grundpreis) - Monatliche Grundgebühren für Strom & Gas
- 💳 **Monatliche Abschläge (Voraus)** - Vorkonfigurierte Abschlagszahlungen
- 📆 **Abrechnung Monat** - Flexibles Abrechnungsdatum für Kostenberechnungen
- 🔗 **Dynamische Helfer** - Verlinke Entities für:
  - Strom-/Gaspreise (kWh)
  - Gasbrennwert (Brennwert)
  - Gaszustandszahl
  - Basis-Preise (Grundgebühren)
  - Abschlagszahlungen

## 🚀 Installation

### Schritt 1: HACS Integration hinzufügen

1. Öffne **Einstellungen → Geräte & Dienste → Integrationen**
2. Klicke auf **Neue Integration erstellen** (Knopf rechts unten)
3. Suche nach **"Emlog"**
4. Klicke auf die Integration und folge dem Setup-Dialog

Falls die Integration nicht angezeigt wird:
- HACS → **Integrationen**
- Klicke auf das Menü (⋮) → **Custom Repositories**
- Trage die URL ein: `https://github.com/strausmann/hacs_emlog`
- Kategorie: **Integration**
- Speichern → **Installieren**
- Home Assistant **neu starten**

### Schritt 2: Integration konfigurieren

Nach dem Neustart öffne wieder **Einstellungen → Geräte & Dienste → Integration hinzufügen → Emlog**

Du musst folgende Angaben machen:

| Feld | Beschreibung | Beispiel |
|------|-------------|---------|
| **Host** | IP-Adresse deines Emlog-Geräts (ohne `http://`) | `192.168.1.50` |
| **Zähler-Index** | Meterindex für diesen Zähler (1-4) | `1` (für Strom), `2` (für Gas) |
| **Zähler-Typ** | Messertyp (Strom oder Gas) | `Strom` |
| **Scan-Intervall** | Wie oft Daten abgefragt werden (Sekunden) | `30` |

### Schritt 3: Optionen konfigurieren (Optional)

Nach der Einrichtung kannst du **erweiterte Optionen** im Zahnrad-Icon (⚙️) der Integration setzen:

#### Preise & Gebühren

| Option | Beschreibung | Standard | Format |
|--------|-------------|---------|--------|
| **Preis pro kWh** | Strompreis für Kostenberechnung | `0,00` | EUR/kWh mit bis zu 4 Dezimalstellen (z.B. `0,3854`) |
| **Basis-Preis (€/Monat)** | Monatliche Grundgebühr | `0,00` | EUR |
| **Monatlicher Abschlag** | Vorkonfigurierte monatliche Zahlung | `0,00` | EUR |

#### Gas-spezifische Einstellungen

| Option | Beschreibung | Standard |
|--------|-------------|---------|
| **Gasbrennwert** | Umrechnung m³ → kWh | `10,88` |
| **Gaszustandszahl** | Zusatzfaktor für Gasberechnung | `1,0` |

#### Abrechnung & Helfer

| Option | Beschreibung |
|--------|-------------|
| **Abrechnung Monat** | Monat (1-12) für jährliche Kostenberechnung |
| **Dynamische Helfer** | Verlinke `input_number` oder andere Entities für dynamische Werte |

**💡 Tipp:** Statt feste Werte einzustellen, kannst du **dynamische Helfer** verwenden:
1. Erstelle `input_number` Entities in der UI
2. Wähle diese in den Integrations-Optionen aus
3. Ändere Werte jederzeit ohne Integration neu zu laden!

Beispiel:
```yaml
# Erstelle diese Eingabe-Entities (Input > Number)
input_number:
  strompreis:
    min: 0
    max: 1
    step: 0.0001
    unit_of_measurement: "EUR/kWh"
    
  gasbrennwert:
    min: 5
    max: 15
    step: 0.01
```

## 📊 Verfügbare Sensoren

Nach der Konfiguration werden automatisch Sensoren für deinen Zähler erstellt. Die Entity-Namen folgen dem Pattern:
`sensor.emlog_{meter_type}_{sensor_key}`

Beispiele: `sensor.emlog_strom_zaehlerstand_kwh`, `sensor.emlog_gas_wirkleistung_w`

### Gemeinsame Informations-Sensoren

| Entity-Name | Name | Unit | Beschreibung |
|-------------|------|------|------------|
| `emlog_product` | Produkt | — | Produktbezeichnung vom Emlog-Gerät (z.B. "Emlog - Electronic Meter Log") |
| `emlog_version` | Software Version | — | Firmware-Version des Emlog-Geräts (z.B. 1.16) |

### Strom (Electricity) - Meter-Sensoren

| Entity-Name | Name | Unit | Device Class | Beschreibung |
|-------------|------|------|--------------|------------|
| `emlog_strom_zaehlerstand_kwh` | Zählerstand (kWh) | kWh | `energy` | **Gesamter Stromverbrauch** seit Inbetriebnahme (kumulativ, nur steigend) |
| `emlog_strom_wirkleistung_w` | Wirkleistung (W) | W | `power` | **Aktuelle Stromleistung** in Echtzeit (Messwert alle 30 Sekunden) |
| `emlog_strom_verbrauch_tag_kwh` | Verbrauch Heute (kWh) | kWh | `energy` | **Heutiger Stromverbrauch** (setzt sich täglich zurück) |
| `emlog_strom_betrag_tag_eur` | Betrag Heute | [Währung] | `monetary` | **Heutige Stromkosten** aus Emlog-API (berechneter Tagesbetrag) |
| `emlog_strom_preis_eur_kwh` | Preis (kWh) | [Währung]/kWh | `monetary` | **Konfigurierter Strompreis** (nutzt Helfer wenn verlinkt) |

### Gas (Gas) - Meter-Sensoren

| Entity-Name | Name | Unit | Device Class | Beschreibung |
|-------------|------|------|--------------|------------|
| `emlog_gas_zaehlerstand_m3` | Zählerstand (m³) | m³ | `gas` | **Gesamter Gasverbrauch** in Kubikmetern seit Inbetriebnahme |
| `emlog_gas_zaehlerstand_kwh` | Zählerstand (kWh) | kWh | `energy` | **Gesamter Gasverbrauch in kWh** (konvertiert mit Brennwert/Zustandszahl) |
| `emlog_gas_wirkleistung_w` | Wirkleistung (W) | W | `power` | **Aktuelle Gasleistung** |
| `emlog_gas_verbrauch_tag_kwh` | Verbrauch Heute (kWh) | kWh | `energy` | **Heutiger Gasverbrauch in kWh** |
| `emlog_gas_betrag_tag_eur` | Betrag Heute | [Währung] | `monetary` | **Heutige Gaskosten** |
| `emlog_gas_preis_eur_kwh` | Preis (kWh) | [Währung]/kWh | `monetary` | **Konfigurierter Gaspreis** |
| `emlog_gas_brennwert` | Brennwert | — | — | **Brennwert für Gas-Umrechnung** (m³ → kWh) |
| `emlog_gas_zustandszahl` | Zustandszahl | — | — | **Zustandszahl für Gas-Umrechnung** |

### Status & Fehler-Sensoren

| Entity-Name | Name | Unit | Beschreibung |
|-------------|------|------|------------|
| `emlog_strom_status` / `emlog_gas_status` | API Status | — | **API-Verbindungsstatus** ("connected", "failed", "initializing") |
| `emlog_strom_last_error` / `emlog_gas_last_error` | Letzte Fehlermeldung | — | **Letzter Fehler** bei API-Abfrage (leer wenn OK) |
| `emlog_strom_last_update` / `emlog_gas_last_update` | Letztes Update | — | **Zeitstempel** des letzten erfolgreichen Updates |

### Automatische Utility Meter (Aggregationen)

Die Integration erstellt automatisch für **jeden Meter-Typ** (Strom/Gas) **drei Utility Meter**:

| Entity-Name | Name | Period | Beschreibung |
|-------------|------|--------|------------|
| `sensor.emlog_strom_1_verbrauch_tag` | Emlog Strom 1 Verbrauch Tag | Täglich | Täglicher Stromverbrauch (Referenz-Entity: `sensor.emlog_strom_zaehlerstand_kwh`) |
| `sensor.emlog_strom_1_verbrauch_monat` | Emlog Strom 1 Verbrauch Monat | Monatlich | Monatlicher Stromverbrauch (setzt sich am 1. des Monats zurück) |
| `sensor.emlog_strom_1_verbrauch_jahr` | Emlog Strom 1 Verbrauch Jahr | Jährlich | Jährlicher Stromverbrauch (setzt sich am 1. Januar zurück) |
| `sensor.emlog_gas_2_verbrauch_tag` | Emlog Gas 2 Verbrauch Tag | Täglich | Täglicher Gasverbrauch |
| `sensor.emlog_gas_2_verbrauch_monat` | Emlog Gas 2 Verbrauch Monat | Monatlich | Monatlicher Gasverbrauch |
| `sensor.emlog_gas_2_verbrauch_jahr` | Emlog Gas 2 Verbrauch Jahr | Jährlich | Jährlicher Gasverbrauch |

**Hinweis:** Die Nummer in der Entity (z.B. "1" bei "emlog_strom_1") ist der Meter-Index aus der Konfiguration.

## 💡 Verwendungsbeispiele

### Dashboard mit Verbrauch
```yaml
type: glance
title: Stromverbrauch aktuell
entities:
  - entity: sensor.emlog_strom_zaehlerstand_kwh
    name: Gesamtverbrauch
  - entity: sensor.emlog_strom_wirkleistung_w
    name: Aktuelle Leistung
  - entity: sensor.emlog_strom_1_verbrauch_tag
    name: Heute
  - entity: sensor.emlog_strom_1_verbrauch_monat
    name: Dieser Monat
```

### Automatisierung - Hoher Stromverbrauch
```yaml
automation:
  - alias: "Stromverbrauch zu hoch"
    trigger:
      platform: numeric_state
      entity_id: sensor.emlog_strom_wirkleistung_w
      above: 3000
    action:
      - service: persistent_notification.create
        data:
          title: "⚠️ Hoher Stromverbrauch"
          message: "Leistung über 3000W: {{ states('sensor.emlog_strom_wirkleistung_w') }}W"
```

### Script - Tägliche Verbrauchsmitteilung
```yaml
script:
  tagesverbrauch_bericht:
    sequence:
      - service: notify.notify
        data:
          title: "📊 Stromverbrauch heute"
          message: |
            Verbrauch: {{ states('sensor.emlog_strom_1_verbrauch_tag') }} kWh
            Kosten: {{ (states('sensor.emlog_strom_1_verbrauch_tag') | float(0) * 0.35) | round(2) }} EUR
```

## 🔧 Fehlerbehebung

### Integration wird nicht angezeigt
- Home Assistant **neu starten** (Einstellungen → System → Neu starten oben rechts)
- HACS Cache leeren: HACS-Seite mit `Strg+Shift+R` neu laden

### Verbindungsfehler
- **"HTTP 404 Not Found"** → Meterindex prüfen (meist `1` für Strom, `2` für Gas)
- **"Timeout"** → Scan-Intervall erhöhen (z.B. auf `60` Sekunden), oder Emlog-IP-Adresse prüfen
- **"Connection refused"** → Prüfe ob Emlog online ist: `ping 192.168.x.x`

### Sensoren zeigen "unavailable"
- Gehe in die **Optionen** der Integration (Zahnrad-Icon)
- Prüfe dass Helfer-Entities korrekt verlinkt sind
- Führe einen **Integration Reload** durch: Einstellungen → Geräte & Dienste → Emlog → ⋮ (Menü) → **Neu laden**

### Dynamische Helfer funktionieren nicht
- Stelle sicher dass die `input_number` Entity existiert
- Prüfe die Entity-ID in den Integrations-Optionen
- Entity-ID muss exakt passen (z.B. `input_number.strompreis_kwh`)
- Nach Helfer-Änderung: **Integration Reload** durchführen

## 📚 Weitere Dokumentation

- **[Architektur-Details](docs/architecture/README.md)** - Technischer Aufbau
- **[API-Referenz](docs/api/README.md)** - Emlog JSON-Format
- **[Entwicklungs-Guide](CONTRIBUTING.md)** - Für Contributor

## 🤝 Fragen & Support

- **[GitHub Issues](https://github.com/strausmann/hacs_emlog/issues)** - Bug Reports & Feature Requests
- **[GitHub Discussions](https://github.com/strausmann/hacs_emlog/discussions)** - Fragen & Austausch
- **[Home Assistant Forum](https://community.home-assistant.io/)** - Community Support

## 🙌 Beitragen

Möchtest du zur Integration beitragen?
- 🐛 **Bug melden** - Im [Issue-Tracker](https://github.com/strausmann/hacs_emlog/issues)
- 💡 **Feature vorschlagen** - Mit detaillierter Beschreibung
- 📝 **Dokumentation verbessern** - Pull Request mit Verbesserungen
- 💻 **Code beitragen** - Schaue [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 Lizenz

Diese Integration ist unter der [Apache 2.0 Lizenz](LICENSE) lizenziert.
