# Architecture Decisions - Emlog Home Assistant Integration

**Dokumentation aller bewussten Architektur- und Design-Entscheidungen für zukünftige Entwicklung.**

## 1. Constants-Zentrale (const.py)

**Entscheidung:** Alle Konfigurationskonstanten zentral in `const.py` definieren.

**Begründung:**

- Single Source of Truth für Konfigurationsschlüssel
- Einfache Wartung und Änderungen
- Verhindert Typos und Duplikate
- Leichte Übersicht über alle Optionen

**Implementierung:**

- `CONF_*`: Konfigurationsschlüssel (UI und persistente Werte)
- `DEFAULT_*`: Standardwerte mit aussagekräftigen Defaults
- `METER_TYPE_*`: Enumerationen für Zählertypen
- `METER_INDICES`: Liste der unterstützten Meter-Indizes

---

## 2. Helper-Entity-Fallback-Kette

**Entscheidung:** Hierarchisches Fallback-System für dynamische Werte (Preise, Gas-Faktoren).

**Begründung:**

- Maximale Flexibilität für den User
- Mehrere Konfigurationsebenen möglich
- Verhindert Fehler durch Prioritätsklarheit

**Prioritätsordnung (höher gewinnt):**

1. **Helper Entity** (wenn konfiguriert)
2. **Options Flow** (benutzer Überschreibung)
3. **Config Entry Data** (ursprüngliche Konfiguration)
4. **DEFAULT\_\* Konstante** (Fallback)

**Beispiel:**

```python
# In template.py oder sensor.py
price = (
    get_helper_value(CONF_PRICE_HELPER) or
    options.get(CONF_PRICE_KWH) or
    data.get(CONF_PRICE_KWH) or
    DEFAULT_PRICE_KWH
)
```

**Vorteil:** User kann jederzeit zwischen fest eingegebenem Wert und automatischem Helper wechseln, ohne die Konfiguration zu löschen.

---

## 3. Konditionaler EntitySelector in Options Flow

**Entscheidung:** EntitySelector nur anzeigen, wenn bereits ein Helper-Wert konfiguriert ist.

**Begründung:**

- **Bessere UX:** User sieht nur die Felder, die er braucht
- **Flexibilität:** Kann jederzeit Switch zwischen Fallback-Wert und Helper
- **Klarheit:** Unterschiedliche Eingabemethoden sind klar erkennbar
- **Performance:** Keine unnötigen Listenabfragen für Entity-Auswahl

**Implementierung:**

```python
# Pseudo-Code
if current_price_helper:
    # User hat bereits einen Helper - zeige EntitySelector
    schema[CONF_PRICE_HELPER] = EntitySelector(...)
else:
    # Kein Helper konfiguriert - zeige Text-Feld für Fallback-Wert
    schema[CONF_PRICE_HELPER] = str
```

**Ablauf:**

1. User gibt Fallback-Wert (z.B. 0,45 €/kWh) ein → speichern
2. Später: User kann Options neu öffnen, EntitySelector erscheint
3. User wählt Helper-Entity → automatische Werte übernehmen Priorität

---

## 4. Meter-Indizes: Hardware-abhängig (1-4)

**Entscheidung:** Meter-Indizes nicht auf 1,2 festlegen, sondern flexibel 1-4 erlauben.

**Begründung:**

- Verschiedene Emlog-Hardware hat unterschiedliche Zähler
- User weiß selbst, welche Indizes verfügbar sind
- Config-Flow validiert Verbindung mit gewähltem Index
- Fehler beim Index werden sofort beim Setup erkannt

**Implementierung:**

- `METER_INDICES = [1, 2, 3, 4]`
- SelectSelector in User-Step für intuitive Auswahl
- Validierung durch `validate_emlog_connection()` beim Setup

---

## 5. Feed-In Sensoren als optionales Feature

**Entscheidung:** Liefer-Sensoren (Solar/Einspeisungs-Werte) nur für Strom-Meter, nur wenn aktiviert.

**Begründung:**

- **Nur für Strom relevant:** Gas hat keine Rückspeisung
- **User-Choice:** Nicht jeder hat Photovoltaik
- **Cleaner UI:** Nur verfügbare Sensoren erzeugen
- **API-Datenekonomi:** Weniger Sensoren = weniger Speicher

**Implementierung:**

- `CONF_INCLUDE_FEED_IN_SENSORS = False` (default disabled)
- Nur aktivierbar bei `METER_TYPE_STROM`
- In `sensor.py`: Feeds nur erstellen wenn `include_feed_in_sensors = True`
- Sensor-Keys: `bezug_*` (Bezug), `lieferung_*` (Lieferung)

**Beispiel Sensor-Daten:**

```json
{
  "Zaehlerstand_Bezug": {"Stand180": 1234.56, ...},      // Nur wenn disabled
  "Zaehlerstand_Lieferung": {"Stand280": 42.10, ...}     // Nur wenn enabled
}
```

---

## 6. Tarifwechsel mit Date-basierter Preisänderung

**Entscheidung:** Tarifwechsel-Logik mit Datum und vordefinierten neuen Preisen.

**Begründung:**

- **Realistische Preispolitik:** Tarifwechsel an Stichtagen (meist 01.01.)
- **Automatisierung:** Neue Preise ab Datum automatisch aktiv
- **Nachverfolgung:** System berücksichtigt alte Preise für abgelaufene Periode
- **Vorausplanung:** User kann neue Preise vorausplanen

**Implementierung:**

```python
CONF_PRICE_CHANGE_DATE_STROM = "price_change_date_strom"  # Format: "YYYY-MM-DD"
CONF_PRICE_KWH_NEW_STROM = "price_kwh_new_strom"          # Neuer Preis ab Datum
CONF_PRICE_KWH_NEW_STROM_HELPER = "price_kwh_new_strom_helper"  # Optional Helper
```

**Logik in template.py:**

- Vor Change-Datum: alter Preis verwenden
- Ab Change-Datum: neuer Preis verwenden
- Kosten-Sensor verwendet korrekte Preise historisch korrekt

---

## 7. Template-Sensoren mit Kosten-Berechnung

**Entscheidung:** Eigene `template.py` für berechnete Sensoren (Kosten, Abschlag).

**Begründung:**

- **Separation of Concerns:** Rohdaten vs. berechnete Werte
- **Modularität:** Einfach erweiterbar mit neuen Berechnungen
- **Performance:** Nur wenn nötig aktualisieren
- **Wartbarkeit:** Komplexe Logik isoliert

**Sensoren in template.py:**

- **Cost Sensor:** `costs_today_strom`, `costs_month_strom`, etc.
  - Berechnung: Verbrauch × Preis + Grundgebühr
  - Mit Tarifwechsel-Unterstützung
- **Advance Tracking Sensor:** `advance_payment_balance_strom`
  - Vergleich: Gezahlter Abschlag vs. Verbrauchskosten
  - Hilft User, Nachzahlung/Rückzahlung zu tracken

---

## 8. Settlement Month (Abrechnungsmonat)

**Entscheidung:** Abrechnungsmonat konfigurierbar (default: Dezember).

**Begründung:**

- **Individualität:** Nicht alle User haben Jahresabrechnung im Dezember
- **Accurate Accounting:** Utility-Meter müssen auf Abrechnungsmonat basieren
- **Tariff-Switching:** Neue Tarife oft am Abrechnungsmonat wirksam
- **Kumulierte Metriken:** Yearly-Meter setzen bei Abrechnungsmonat zurück

**Implementierung:**

- Dropdown mit Monaten 1-12 (Januar-Dezember)
- DEFAULT: 12 (Dezember)
- Wird an Utility-Meter in `utility_meter.py` weitergegeben

---

## 9. Pre-Commit Validation mit `make check-logs`

**Entscheidung:** Make-Target zur Validierung von HA-Logs vor Commits.

**Begründung:**

- **Early Warning:** Importfehler sofort erkannt (verhindert broken commits)
- **CI-Prevention:** Verhindert, dass fehlerhafte Commits gepusht werden
- **Developer Experience:** Schnelle Feedback-Schleife
- **Integration Health:** Sicherstellt, dass Integration laden kann

**Implementierung:**

- Ziel: `tests/config/home-assistant.log.1`
- Sucht nach: `ImportError`, `Setup failed for custom integration 'emlog'`, `ModuleNotFoundError`, `AttributeError`
- Exit-Code 1 wenn Fehler gefunden → Commit wird blockiert

**Workflow:**

```bash
# Vor jedem Commit:
make check-logs

# Nur wenn ✅ erfolgreich:
git commit ...
```

---

## 10. Granulare Commits mit Conventional Commits

**Entscheidung:** Ein Commit = Eine logische Änderung mit echtem Scope.

**Begründung:**

- **Semantic Versioning:** Commitlint + Semantic Release erfordern exakte Typisierung
- **Git History:** Lesbar und nachverfolgbar
- **Revertbarkeit:** Jeder Commit kann isoliert rückgängig gemacht werden
- **Review Quality:** Smaller PRs sind einfacher zu reviewen

**Erforderlich:**

```
type(scope): description

type: feat|fix|docs|style|refactor|perf|test|chore|build|ci
scope: coordinator|sensor|config|manifest|const|translations|mock|test|docs|ci|deps|build|chore
```

**Beispiel korrekter Commits:**

```
fix(const): add missing METER_TYPE constants and defaults
build(makefile): add check-logs target for pre-commit validation
feat(translations): add feed-in sensor descriptions
feat(config): implement property-based value resolution
```

**Anti-Pattern (nicht erlaubt):**

```
❌ feat: add new sensor                          # Kein Scope!
❌ fix(config): refactor all components          # Sammel-Commit!
❌ Update stuff in multiple files                # Zu vage!
```

---

## 11. Async Coordinator Pattern

**Entscheidung:** Async HTTP-Polling mit Home Assistant Coordinator.

**Begründung:**

- **HA Best Practice:** Coordinator ist Standard-Pattern
- **Error Handling:** Built-in Retry-Logik und Error Tracking
- **Performance:** Non-blocking I/O
- **Updates:** Automatische Entities-Aktualisierung bei Daten-Change

**Implementierung:**

- `coordinator.py`: HTTP-Get zur Emlog-API
- Timeout: 10 Sekunden pro Request
- Retry: Automatisch bei Timeouts/Verbindungsfehlern
- Update-Interval: Konfigurierbar (default: 30 Sekunden)

---

## 12. Sensor Data Flow & Unique IDs

**Entscheidung:** Konsistente Unique-ID Generierung mit Pattern-Basierung.

**Begründung:**

- **HA Entity Registration:** Eindeutige IDs notwendig
- **Portabilität:** Sensor-IDs bleiben gleich bei Config-Änderungen (wichtig für History)
- **Multi-Meter Support:** Mehrere Geräte unterscheidbar

**Pattern:**

```python
unique_id = f"emlog_{host}_{meter_type}_{meter_index}_{sensor_key}".replace(".", "_")
```

**Beispiel:**

```
emlog_192_168_1_100_strom_1_zaehlerstand_kwh
emlog_192_168_1_100_gas_2_verbrauch_m3
```

---

## 13. Backward Compatibility: YAML Package

**Entscheidung:** Legacy YAML Package (`package/emlog.yaml`) wird parallel gewartet.

**Begründung:**

- **Existing Users:** Wollen nicht erzwungen sein, zu migrieren
- **Advanced Features:** YAML-Package hat Tariff-Switching und Utility-Meter-Templates
- **Graduelle Migration:** User können selber entscheiden, wann sie upgraden
- **Knowledge:** YAML-User haben etablierte Automations basierend auf Package

**Status:**

- HACS Integration: Core-Funktionalität (Sensoren, Basis-Konfiguration)
- YAML Package: Erweiterungen (Kosten, Utility-Meter, Templates)
- **Ziel:** HACS Integration wird YAML-Package Features übernehmen

---

## 14. Testing: Mock Server statt Live Device

**Entscheidung:** Mock-Server (`tests/mock/`) für Development ohne physisches Gerät.

**Begründung:**

- **Reproduzierbarkeit:** Tests sind deterministisch
- **Speed:** Instant Response (nicht 30 Sekunden Polling-Interval)
- **Safety:** Keine Abhängigkeit von Netzwerk/Hardware
- **CI/CD:** Testable in GitHub Actions

**Implementierung:**

- `mock_server.py`: Flask-App mit Emlog-API-Nachahmung
- `meter_1.json`, `meter_2.json`: Realistische Test-Daten
- `docker-compose.test.yml`: Isolated Testing
- `test.sh`: Schneller Validator

---

## Entscheidungs-Checkliste für zukünftige Änderungen

Bevor du eine Änderung machst, frag dich:

- [ ] Gehört die Änderung in eine neue Datei oder besteht eine logische Einheit mit const.py/config_flow.py/sensor.py?
- [ ] Ist ein Fallback-Wert nötig? → Helper-Entity-Kette verwenden
- [ ] Ist es ein optionales Feature? → `CONF_INCLUDE_*` Toggle einführen
- [ ] Wurden `make check-logs` und `make ha-reload` vorher ausgeführt?
- [ ] Ist jeder Commit granular mit echtem Scope? (Keine Sammel-Commits!)
- [ ] Sind Translations aktualisiert (de.json + en.json)?
- [ ] Sind neue Konstanten in const.py dokumentiert?

---

**Letzte Aktualisierung:** 2026-01-15
**Version:** 0.2.0-dev
**Status:** Aktiv in Entwicklung
