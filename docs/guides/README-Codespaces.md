# Codespaces Development Guide

Diese Integration funktioniert nahtlos in GitHub Codespaces mit automatischer URL-Konfiguration.

## 🚀 Schnellstart

```bash
# 1. Starte Home Assistant und Mock Server
make dev-up

# Oder einzeln:
make ha-up      # Home Assistant
make mock-up    # Mock Emlog Server
```

## 🔧 Automatische Codespaces-Konfiguration

Das Projekt erkennt automatisch, wenn es in Codespaces läuft und generiert die externe URL dynamisch:

```
https://<codespace-name>-8123.app.github.dev
```

### Wie es funktioniert

1. **`update_ha_config.py`** - Python-Script das:
   - Codespaces-Umgebungsvariablen (`CODESPACE_NAME`, `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`) ausliest
   - Die externe URL automatisch generiert
   - `test_config/configuration.yaml` aktualisiert

2. **Makefile Integration** - Der `make ha-up` Befehl führt automatisch das Update-Script aus

3. **Keine manuellen Eingriffe nötig** - Jede neue Codespaces-Instanz wird sofort konfiguriert

## 📍 URLs

### Lokal (im Codespaces Terminal) - EMPFOHLEN ✓

- UI: `http://localhost:8123` - **Direkt, schnell, keine Auth-Komplexität**
- API: `http://localhost:8123/api/`
- **Beste Option für Development!**

### Extern (über Browser/Netzwerk) - OPTIONAL

- URL wird automatisch generiert: `https://<codespace-name>-8123.app.github.dev`
- ⚠️ Codespaces Tunnel erfordert PKI-Authentifizierung
- API-Zugriff erfordert Bearer Token
- Siehe [CODESPACES-ACCESS.md](./CODESPACES-ACCESS.md) für Workarounds

## 🔐 Authentifizierung

### Benutzer

- **Benutzername:** `bjoern`
- **Passwort:** `bjoern`

### API Token

1. Öffne `https://<codespace-name>-8123.app.github.dev`
2. Melde dich an
3. Gehe zu: Einstellungen → Developer Tools → API
4. Kopiere einen "Langjähriger Zugangstoken"

Oder siehe [test_config/test_token.txt](test_config/test_token.txt) für weitere Optionen.

## 📋 Befehle

```bash
# Development Server starten
make dev-up          # Beide Container
make ha-up          # Nur Home Assistant
make mock-up        # Nur Mock Server

# Logs anschauen
make ha-logs        # HA Logs
make mock-logs      # Mock Server Logs
make dev-logs       # Alle Logs

# Herunterfahren
make dev-down       # Alles stoppen

# Konfiguration aktualisieren
make update-ha-config  # Externe URL neu generieren
```

## 🧪 Integration Testen

```bash
# Mock API testen
curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=1" | python3 -m json.tool

# Alle HA States abrufen (mit Bearer Token)
export TOKEN="<your_token_here>"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8123/api/states | python3 -m json.tool
```

## ⚙️ Konfiguration

Die Konfiguration wird automatisch generiert. Falls manuelle Anpassungen nötig sind:

**Datei:** `test_config/configuration.yaml`

```yaml
homeassistant:
  external_url: 'https://glowing-space-goggles-65pgrpx69jc5577-8123.app.github.dev' # Auto-generiert
  internal_url: 'http://localhost:8123'
```

### Manuelle URL-Erkennung

Falls `update_ha_config.py` nicht automatisch läuft:

```bash
python3 update_ha_config.py
```

## 🐳 Docker Container

```bash
# Alle Container
docker-compose -f tools/docker/compose.yml ps

# Spezifische Logs
docker-compose -f tools/docker/compose.yml logs -f homeassistant
docker-compose -f tools/docker/compose.yml logs -f emlog-mock

# Container neustarten
docker-compose -f tools/docker/compose.yml restart homeassistant
```

## 🔄 Neu in Codespaces?

1. Codespaces startet und aktiviert devcontainer (siehe `.devcontainer/devcontainer.json`)
2. Home Assistant und Mock Server werden im Hintergrund als Docker Container gestartet
3. `update_ha_config.py` wird automatisch ausgeführt (per devcontainer hooks)
4. Codespaces-URL wird in `configuration.yaml` eingetragen
5. HA ist erreichbar unter `https://<name>-8123.app.github.dev`

## 📝 Troubleshooting

### 400 Bad Request bei `https://...app.github.dev`

→ **Lösung:** Das ist die Codespaces Tunnel-Auth. Nutze stattdessen `http://localhost:8123`
→ Siehe [CODESPACES-ACCESS.md](./CODESPACES-ACCESS.md) für externe Zugriffs-Optionen

### Auth-Fehler bei `https://...app.github.dev`

→ Codespaces Tunnel erfordert PKI-Auth. Verwende Bearer Token für API-Zugriffe
→ Oder: Nutze localhost (`http://localhost:8123`)

### HA lädt nicht richtig

→ Container neu starten: `docker-compose -f tools/docker/compose.yml restart homeassistant`

### Mock Server antwortet nicht

→ Prüfe ob Container läuft: `docker ps | grep emlog-mock`
→ Falls nicht: `make mock-up`

### Ports konflikt

→ Andere Prozesse auf Port 8123 oder 8080 beenden
→ Oder Ports in `tools/docker/compose.yml` anpassen

## 🎯 Next Steps

1. **Emlog Integration konfigurieren:**
   - Einstellungen → Geräte & Dienste
   - "+ Integration" → Emlog
   - Host: `emlog-mock` (Docker internen Hostname)
   - Meter-Indizes: 1 (Strom), 2 (Gas)

2. **Entities prüfen:**
   - Einstellungen → Geräte & Dienste → Emlog
   - Alle Sensor-Entities sollten sichtbar sein

3. **HACS verwenden:**
   - Einstellungen → Geräte & Dienste → HACS
   - Community-Integrationen installieren/verwalten
