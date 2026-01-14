#!/usr/bin/env python3
"""
Mock Emlog Server für Entwicklung und Tests
Simuliert die Emlog API Endpunkte
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

MOCK_DATA_DIR = os.environ.get('MOCK_DATA_DIR', './mock_data')

def load_mock_data(meter_index):
    """Lädt Mock-Daten für einen bestimmten Meter-Index"""
    filename = f"meter_{meter_index}.json"
    filepath = os.path.join(MOCK_DATA_DIR, filename)

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    # Fallback: Generiere dynamische Daten
    return generate_dynamic_data(meter_index)

def generate_dynamic_data(meter_index):
    """Generiert dynamische Mock-Daten"""
    import random
    import time

    base_consumption = 1000 + (meter_index * 500)  # Basisverbrauch
    current_time = time.time()

    # Simuliere leicht steigenden Verbrauch
    consumption_offset = (current_time % 86400) / 86400 * 10  # Täglicher Zyklus

    if meter_index == 1:  # Strom
        return {
            "product": "Emlog Strom",
            "version": "1.2.3",
            "Zaehlerstand_Bezug": {
                "Stand180": base_consumption + consumption_offset
            },
            "Wirkleistung_Bezug": {
                "Leistung170": 2.5 + random.uniform(-0.5, 0.5)
            },
            "Kwh_Bezug": {
                "Kwh180": 15.7 + random.uniform(-2, 2)
            },
            "Betrag_Bezug": {
                "Betrag180": 3.25 + random.uniform(-0.5, 0.5)
            }
        }
    else:  # Gas
        return {
            "product": "Emlog Gas",
            "version": "1.2.3",
            "Zaehlerstand_Bezug": {
                "Stand180": base_consumption + consumption_offset
            },
            "Wirkleistung_Bezug": {
                "Leistung170": 0.8 + random.uniform(-0.1, 0.1)
            },
            "Kwh_Bezug": {
                "Kwh180": 8.3 + random.uniform(-1, 1)
            },
            "Betrag_Bezug": {
                "Betrag180": 1.85 + random.uniform(-0.2, 0.2)
            }
        }

@app.route('/pages/getinformation.php')
def get_information():
    """Haupt-API-Endpunkt"""
    meter_index = int(request.args.get('meterindex', 1))

    if request.args.get('export'):
        data = load_mock_data(meter_index)
        return jsonify(data)

    return jsonify({"error": "Export parameter required"}), 400

@app.route('/')
def index():
    """Einfache Status-Seite"""
    return f"""
    <h1>Emlog Mock Server</h1>
    <p>Running on port 8080</p>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/pages/getinformation.php?export&meterindex=1">Strom (Index 1)</a></li>
        <li><a href="/pages/getinformation.php?export&meterindex=2">Gas (Index 2)</a></li>
    </ul>
    """

if __name__ == '__main__':
    # Erstelle Mock-Daten-Verzeichnis falls nicht vorhanden
    os.makedirs(MOCK_DATA_DIR, exist_ok=True)

    print(f"Starting Emlog Mock Server on port 8080")
    print(f"Mock data directory: {MOCK_DATA_DIR}")
    app.run(host='0.0.0.0', port=8080, debug=True)