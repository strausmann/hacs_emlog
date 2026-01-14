# Emlog (Electronic Meter Log) – Home Assistant Integration

Diese Integration liest Energie- und Gaszählerdaten direkt vom Emlog-Gerät und macht sie in Home Assistant verfügbar.

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
| **Strom Meterindex** | Meterindex für Stromdaten | `1` |
| **Gas Meterindex** | Meterindex für Gasdaten | `2` |
| **Scan-Intervall** | Wie oft Daten abgefragt werden (Sekunden) | `30` |

### Schritt 3: Optionen konfigurieren (Optional)

Nach der Einrichtung kannst du **erweiterte Optionen** im Zahnrad-Icon (⚙️) der Integration setzen:

| Option | Beschreibung | Standard |
|--------|-------------|---------|
| **Strompreis (€/kWh)** | Strompreis für Kostenberechnung | `0,00` |
| **Gasbrennwert** | Gasumrechnung Brennwert | `10,88` |
| **Gaszustandszahl** | Gasumrechnung Zustandszahl | `1,0` |
| **Grundpreis Strom (€/Monat)** | Monatlicher Grundpreis Strom | `0,00` |
| **Grundpreis Gas (€/Monat)** | Monatlicher Grundpreis Gas | `0,00` |
| **Hilfsenzitäten** | Verlinke `input_number` Entities für dynamische Werte | - |

**💡 Tipp:** Du kannst auch `input_number` Entities erstellen und diese in den Optionen verlinken. So kannst du Preise und Faktoren jederzeit von der UI aus ändern, ohne die Integration neu zu starten!

## 📊 Verfügbare Sensoren

Nach der Konfiguration werden automatisch folgende Sensoren erstellt:

### Strom (Electricity)
- 📊 **Zählerstand (kWh)** - Gesamte Stromverbrauch seit Inbetriebnahme
- 📈 **Tarif 1 Zählerstand (kWh)** - Gesamter Verbrauch Tarif 1
- 📈 **Tarif 2 Zählerstand (kWh)** - Gesamter Verbrauch Tarif 2
- ⚡ **Aktuelle Leistung (W)** - Aktueller Stromverbrauch
- 📉 **Tagesverbrauch (kWh)** - Heutiger Verbrauch
- 💶 **Tageskosten (€)** - Heute ausgegebenes Geld
- 💶 **Monatskosten (€)** - Diesen Monat ausgegebenes Geld
- 💶 **Jahreskosten (€)** - Dieses Jahr ausgegebenes Geld

### Gas (Gas)
- 📊 **Zählerstand (m³)** - Gesamter Gasverbrauch seit Inbetriebnahme
- ⚡ **Aktuelle Leistung (W)** - Aktuelle Gasleistung
- 📉 **Tagesverbrauch (kWh)** - Heutiger Gasverbrauch
- 💶 **Tageskosten (€)** - Heute ausgegebenes Geld für Gas
- 💶 **Monatskosten (€)** - Diesen Monat ausgegebenes Geld für Gas
- 💶 **Jahreskosten (€)** - Dieses Jahr ausgegebenes Geld für Gas

**Kostenberechnung:** Die Kosten-Sensoren berechnen sich aus:
- `Verbrauch × Preis/kWh + (Grundpreis ÷ Anzahl Tage/Monate)`

## 🎯 Praktische Verwendung

### Automatisierungen erstellen
Du kannst die Sensoren in Automatisierungen nutzen:

```yaml
automation:
  - alias: "Hoher Stromverbrauch"
    trigger:
      platform: numeric_state
      entity_id: sensor.emlog_strom_leistung
      above: 2000  # über 2000W
    action:
      service: notify.push_notification
      data:
        message: "Stromverbrauch über 2000W!"
```

### Dashboard mit Verbrauch
Erstelle ein schönes Dashboard mit den Verbrauch-Sensoren:

```yaml
type: glance
title: Stromverbrauch
entities:
  - entity: sensor.emlog_strom_zaehlerstand
    name: Gesamtverbrauch
  - entity: sensor.emlog_strom_verbrauch_tag
    name: Heute
  - entity: sensor.emlog_strom_kosten_monat
    name: Kosten diesen Monat
```

### Mit anderen Integrationen kombinieren
- **Energie Integration:** Verbrauchsdaten für die HA-Energie-Statistik nutzen
- **Utility Meter:** Tägliche/monatliche/jährliche Verbrauchsmessung
- **Lovelace Cards:** Custom Cards für Visualisierung der Daten

## 🔧 Fehlerbehebung

### Integration wird nicht angezeigt
- Home Assistant **neu starten** (Einstellungen → Neu starten oben rechts)
- HACS Cache leeren: Seite mit `Strg+Shift+R` neu laden

### Verbindungsfehler
- **"Connection refused"** - Prüfe ob Emlog-IP korrekt ist (probiere `ping 192.168.x.x`)
- **"404 Not Found"** - Meterindex prüfen (meist `1` für Strom, `2` für Gas)
- **Timeout** - Scan-Intervall erhöhen (z.B. auf `60` Sekunden)

### Keine Sensoren sichtbar
- Gehe in die **Optionen** der Integration (Zahnrad-Icon)
- Überprüfe dass Hilfsenzitäten korrekt verlinkt sind
- Integration **neu laden**: Einstellungen → Geräte & Dienste → Emlog → **Einstellungen neu laden**

## 📚 Weitere Dokumentation

- **[Technische Details](docs/architecture/)** - Für fortgeschrittene Benutzer
- **[API Referenz](docs/api/)** - Emlog Datenformat
- **[Vollständige Sensor-Liste](docs/guides/)** - Alle verfügbaren Sensoren

## 🤝 Fragen & Support

- **GitHub Issues:** [Bug Reports & Feature Requests](https://github.com/strausmann/hacs_emlog/issues)
- **Diskussionen:** [GitHub Discussions](https://github.com/strausmann/hacs_emlog/discussions)
- **Home Assistant Forum:** Stelle deine Frage im [Home Assistant Forum](https://community.home-assistant.io/)

## 🙌 Beitragen

Möchtest du zur Integration beitragen? Wir freuen uns über:
- 🐛 **Bug Reports** - Finde und melde Fehler
- 💡 **Feature Requests** - Deine Ideen für neue Funktionen
- 📝 **Dokumentation** - Verbessere die Dokumentation
- 💻 **Code Contributions** - Wenn du selbst programmierst

Schaue dir [CONTRIBUTING.md](CONTRIBUTING.md) für die detaillierten Entwicklungs-Richtlinien an.

## 📄 Lizenz

Diese Integration ist unter der [Apache 2.0 Lizenz](LICENSE) lizenziert.
