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

### Schnellstart mit Make-Befehlen

Die Entwicklungsumgebung kann einfach mit Make-Befehlen gesteuert werden:

```bash
# Hilfe anzeigen
make help

# Vollständige Entwicklungsumgebung starten
make dev-setup

# Einzelne Services verwalten
make mock-up          # Mock Server starten
make ha-up           # Home Assistant starten
make mock-down       # Mock Server stoppen
make ha-down         # Home Assistant stoppen

# Tests durchführen
make test            # Vollständige Tests
make test-api        # Nur API Tests
make lint            # Code-Qualitätsprüfungen

# Status und Logs
make status          # Service Status anzeigen
make dev-logs        # Logs beider Services
make mock-logs       # Nur Mock Server Logs
make ha-logs         # Nur Home Assistant Logs

# Aufräumen
make clean           # Services stoppen
make full-clean      # Vollständiges Cleanup
```

### Lokale Entwicklungsumgebung

Das Projekt enthält eine vollständige Entwicklungsumgebung für GitHub Codespaces:

- **Dev Container**: Vollständige Python/Home Assistant Umgebung
- **Mock Server**: Simuliert Emlog API ohne echte Hardware
- **Test Scripts**: Automatisierte Tests für API und Integration

### Mit Mock Server testen

Für Tests ohne echte Hardware:

1. **Mock Server starten:**
   ```bash
   ./test.sh
   # oder manuell:
   docker-compose -f docker-compose.test.yml up -d emlog-mock
   ```

2. **Home Assistant starten:**
   ```bash
   docker-compose -f docker-compose.test.yml up homeassistant
   ```

3. **Integration über UI konfigurieren:**
   - Öffne Home Assistant im Browser (http://localhost:8123)
   - Gehe zu **Einstellungen > Geräte & Dienste**
   - Klicke **"Integration hinzufügen"**
   - Suche nach **"Emlog"**
   - Konfiguriere:
     - **Host/IP**: `emlog-mock`
     - **Strom Meterindex**: `1`
     - **Gas Meterindex**: `2`
     - **Scan-Intervall**: `30`

### Mit echter Emlog Hardware

Bei echter Hardware:
1. Stelle sicher, dass der Emlog Server im gleichen Netzwerk erreichbar ist
2. Verwende die echte IP-Adresse in der Konfiguration
3. Bei Bedarf Tailscale oder VPN für Remote-Zugriff einrichten

## Releases & Versionierung

Dieses Projekt verwendet [Semantic Release](https://semantic-release.gitbook.io/) für automatisierte Versionierung und Releases:

- **Automatische Releases**: Bei jedem Push zu `main` wird automatisch ein neues Release erstellt
- **Conventional Commits**: Bitte verwenden Sie [Conventional Commits](https://www.conventionalcommits.org/) Format
- **Versionierung**: Semantic Versioning (MAJOR.MINOR.PATCH) basierend auf Commit-Typen:
  - `feat:` → Minor-Version erhöhen
  - `fix:` → Patch-Version erhöhen
  - `BREAKING CHANGE:` → Major-Version erhöhen

### Interaktive Commits
Verwenden Sie `npm run commit` für eine interaktive Commit-Erstellung mit deutschen Prompts:

```bash
npm run commit
```

Dies führt Sie durch:
- Auswahl des Commit-Typs (feat, fix, docs, etc.)
- Scope der Änderung
- Betreff und Beschreibung
- Breaking Changes
- Issue-Referenzen

### Commitlint
Alle Commits werden automatisch auf Conventional Commits Format validiert.

### Changelog
Alle Änderungen werden automatisch in der [CHANGELOG.md](CHANGELOG.md) dokumentiert.

## Contributing

Möchten Sie zur Weiterentwicklung beitragen? Schauen Sie sich unsere [Contributing Guidelines](CONTRIBUTING.md) an!

Dort finden Sie:
- Detaillierte Anleitungen für die Entwicklungsumgebung
- Informationen zur Architektur und Datenflüssen
- Test-Strategien und Qualitätsstandards
- Richtlinien für Pull Requests

## Support
Issues/Feature Requests bitte über GitHub Issues.
