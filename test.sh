#!/bin/bash
# Test Script für Emlog Integration

echo "🚀 Starte Emlog Integration Tests..."

# Stelle sicher, dass wir im richtigen Verzeichnis sind
cd "$(dirname "$0")"

# Starte Mock Server im Hintergrund
echo "📡 Starte Emlog Mock Server..."
docker-compose -f docker-compose.test.yml up -d emlog-mock

# Warte bis Mock Server bereit ist
echo "⏳ Warte auf Mock Server..."
sleep 5

# Teste API Endpunkte
echo "🧪 Teste API Endpunkte..."
curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=1" | head -20
echo -e "\n---"
curl -s "http://localhost:8080/pages/getinformation.php?export&meterindex=2" | head -20

echo -e "\n✅ Mock Server Tests abgeschlossen!"

# Optional: Starte Home Assistant für Integrationstests
read -p "🏠 Home Assistant für Integrationstests starten? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🏠 Starte Home Assistant..."
    docker-compose -f docker-compose.test.yml up homeassistant
fi

# Cleanup
echo "🧹 Räume auf..."
docker-compose -f docker-compose.test.yml down