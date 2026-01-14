#!/bin/bash
# Script zur dynamischen Generierung der Codespaces-URL für Home Assistant

# Prüfe ob wir in Codespaces sind
if [ "$CODESPACES" != "true" ]; then
    echo "✓ Not running in Codespaces - using localhost"
    exit 0
fi

# Prüfe ob die nötigen Variablen vorhanden sind
if [ -z "$CODESPACE_NAME" ] || [ -z "$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" ]; then
    echo "✗ Missing Codespaces environment variables"
    exit 1
fi

# Generiere die externe URL
CODESPACES_URL="https://${CODESPACE_NAME}-8123.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"

echo "🔧 Detected Codespaces environment:"
echo "   Codespace: $CODESPACE_NAME"
echo "   Domain: $GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN"
echo "   URL: $CODESPACES_URL"

# Aktualisiere die configuration.yaml mit der dynamischen URL
CONFIG_FILE="test_config/configuration.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "✗ Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Erstelle einen temporären Backup
cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"

# Ersetze die externe URL
python3 << PYTHON_EOF
import re

config_file = "$CONFIG_FILE"

with open(config_file, 'r') as f:
    content = f.read()

# Ersetze external_url
old_external = r'external_url: "https://[^"]+"'
new_external = f'external_url: "{CODESPACES_URL}"'
content = re.sub(old_external, new_external, content)

# Ersetze auch in cors_allowed_origins
old_cors = r'- "https://[^"]*app\.github\.dev[^"]*"'
new_cors = f'- "{CODESPACES_URL}"'
content = re.sub(old_cors, new_cors, content)

with open(config_file, 'w') as f:
    f.write(content)

print(f"✓ Updated configuration.yaml with Codespaces URL")
PYTHON_EOF

echo "✓ Setup complete - Codespaces URL configured for Home Assistant"
echo ""
echo "Access Home Assistant at:"
echo "  🌐 $CODESPACES_URL"
echo ""
