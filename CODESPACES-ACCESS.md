# Codespaces-Zugriff - Anleitung

## Problem: 400 Bad Request bei Codespaces HTTPS URL

GitHub Codespaces nutzt einen **Tunnel mit PKI-Authentifizierung**, der den Zugriff auf `https://<name>-8123.app.github.dev` schützt.

### Root Cause
- Codespaces leitet zur GitHub Authentifizierung um
- Der Tunnel erfordert spezielle Headers/Auth
- Home Assistant und der Tunnel kommunizieren nicht gut miteinander

## ✅ Lösung: Verwende Localhost für Entwicklung

```bash
# Im Codespaces Terminal (funktioniert immer):
http://localhost:8123
```

**Vorteile:**
- ✓ Direkter Zugriff ohne Tunnel-Umleitung
- ✓ Schneller
- ✓ Keine Auth-Komplexität
- ✓ Perfect für lokale Entwicklung

## 🌐 Externe HTTPS URL (Optional)

Falls du die Codespaces URL brauchst (z.B. für externe API-Tests):

### Option 1: Token-basierter Zugriff
```bash
# 1. Hole dir einen Bearer Token aus test_config/test_token.txt
export TOKEN="<your_token>"

# 2. Benutze den Token mit curl
curl -H "Authorization: Bearer $TOKEN" \
  https://glowing-space-goggles-65pgrpx69jc5577-8123.app.github.dev/api/states
```

### Option 2: Tunnel Debug-Modus
```bash
# Öffne in Browser (mit Tunnel-Auth):
https://glowing-space-goggles-65pgrpx69jc5577-8123.app.github.dev

# Melde dich über GitHub Codespaces Tunnel an
# (Der Tunnel handled die Auth automatisch)
```

## 🚀 Empfohlener Dev-Workflow

```bash
# Terminal 1: Home Assistant starten
make ha-up

# Terminal 2: Im Browser öffnen
http://localhost:8123  # Einfach, ohne Auth

# Login:
# Benutzername: bjoern
# Passwort: bjoern
```

## 📝 Externe Tests (außerhalb von Codespaces)

Falls du von außen auf die Codespaces-Instanz zugreifst:

```bash
# Mit Bearer Token
EXTERNAL_URL="https://glowing-space-goggles-65pgrpx69jc5577-8123.app.github.dev"
TOKEN="<your_bearer_token>"

curl -H "Authorization: Bearer $TOKEN" \
  $EXTERNAL_URL/api/states | python3 -m json.tool
```

## 🔑 Token Management

Siehe [test_config/test_token.txt](../test_config/test_token.txt) für:
- Token Generierung (docker command)
- API Zugriff Beispiele
- Python/Bash Code Snippets

## ❓ Häufige Fragen

**F: Warum funktioniert `https://...app.github.dev` nicht?**
A: Codespaces Tunnel erfordert spezielle PKI-Auth, die mit HA nicht automatisch funktioniert.

**F: Kann ich https:// verwenden?**
A: Ja - lokal über SSH-Forwarding oder mit Token-Auth über die externe URL.

**F: Wird die externe URL nicht mehr benötigt?**
A: Doch! Sie ist in der Konfiguration für API-Zugriffe wichtig. Aber für UI-Zugriffe ist localhost einfacher.

---

**TL;DR:** Verwende `http://localhost:8123` für Development. Funktioniert sofort ohne Auth-Komplexität!
