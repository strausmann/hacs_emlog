# 🚀 Getting Started Guides

Praktische Anleitungen für Installation und Entwicklung der Emlog Integration.

## 📖 Verfügbare Guides

### Für Benutzer

- **[Installation](./README.md)** (ToDo) - Emlog Integration in Home Assistant installieren
- **[Konfiguration](./CONFIGURATION.md)** (ToDo) - Integration konfigurieren
- **[Sensor-Referenz](./SENSORS.md)** (ToDo) - Verfügbare Sensoren

### Für Entwickler

- **[Entwicklungs-Umgebung](./README-Codespaces.md)** - Entwicklung in Codespaces
- **[Zugriff & Setup](./CODESPACES-ACCESS.md)** - Umgebung konfigurieren
- **[Beitragen](./CONTRIBUTING.md)** - Contributing Guidelines
- **[Testing Guide](./TESTING.md)** (ToDo) - Tests schreiben und ausführen

### Spezielle Themen

- **[Sicherheit](../SECURITY.md)** - Security Policy und Vulnerabilities
- **[Architektur](../architecture/)** - Technisches Design
- **[Mock Server](./MOCK-SERVER.md)** (ToDo) - Mock Server für Tests

## 🎯 Schnelleinstieg

### Benutzer: Integration installieren

```
1. Home Assistant öffnen
2. HACS → Integration → Suche "Emlog"
3. Installieren und neu starten
4. Einstellungen → Geräte & Dienste → Emlog
5. Meter IP und Indizes eingeben
```

### Entwickler: Entwicklungs-Umgebung

```bash
# Repository klonen
git clone https://github.com/strausmann/hacs_emlog.git
cd hacs_emlog

# Development-Umgebung starten
make dev-up

# Home Assistant öffnet sich auf http://localhost:8123
```

## 📚 Weitere Ressourcen

- [Home Assistant Dokumentation](https://www.home-assistant.io/docs/)
- [HACS Dokumentation](https://hacs.xyz/docs/)
- [GitHub Repository](https://github.com/strausmann/hacs_emlog)
- [Status Report](../STATUS-REPORT.md)

---

Benötigst du weitere Hilfe? Öffne ein [GitHub Issue](https://github.com/strausmann/hacs_emlog/issues/new).
