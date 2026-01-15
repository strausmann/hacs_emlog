#!/usr/bin/env python3
"""
Mock Emlog Server für Entwicklung und Tests
Simuliert die Emlog API Endpunkte
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import threading
import time
import random
import math
from datetime import datetime

app = Flask(__name__)
CORS(app)

MOCK_DATA_DIR = os.environ.get("MOCK_DATA_DIR", "./mock_data")
STATE_FILE = os.environ.get("STATE_FILE", "/app/state.json")

# Globale Zustände pro Zähler (1=Strom, 2=Gas)
STATE = {}
STATE_LOCK = threading.Lock()

# Konsumraten (kWh/Tag) werden bei Container-Laufzeit einmal festgelegt
ELECTRICITY_DAILY_KWH = random.uniform(30.0, 40.0)
GAS_DAILY_KWH = random.uniform(60.0, 80.0)

# Inkrement alle 10 Sekunden
TICK_SECONDS = 10
ELECTRICITY_INC_KWH = ELECTRICITY_DAILY_KWH / (86400 / TICK_SECONDS)
GAS_INC_KWH = GAS_DAILY_KWH / (86400 / TICK_SECONDS)

# Näherung für Gas-Umrechnung kWh -> m³ (typisch ca. 10 kWh/m³)
GAS_KWH_PER_M3 = 10.0
GAS_INC_M3 = GAS_INC_KWH / GAS_KWH_PER_M3


def load_initial_data(meter_index):
    """Lädt Initialdaten direkt aus mock_data (ohne dynamik)."""
    filename = f"meter_{meter_index}.json"
    filepath = os.path.join(MOCK_DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    # Fallback: generiere Basisdaten
    return generate_dynamic_data(meter_index)


def save_state():
    """Persistiert den Zustand auf Disk, damit ein Restart überlebt wird."""
    with STATE_LOCK:
        try:
            with open(STATE_FILE, "w") as f:
                json.dump(STATE, f)
        except Exception as e:
            print(f"Failed to save state: {e}")


def load_state():
    """Lädt Zustand von Disk, falls vorhanden; sonst aus Initialdaten."""
    global STATE
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                STATE = json.load(f)
                return
        except Exception as e:
            print(f"Failed to load state, using initial: {e}")

    # Initial aus mock_data
    STATE = {
        "1": load_initial_data(1),
        "2": load_initial_data(2),
    }
    save_state()


def generate_dynamic_data(meter_index):
    """Generiert dynamische Mock-Daten basierend auf der vollständigen Emlog API"""
    base_consumption = 1000 + (meter_index * 500)  # Basisverbrauch
    current_time = time.time()

    # Simuliere leicht steigenden Verbrauch
    consumption_offset = (current_time % 86400) / 86400 * 10  # Täglicher Zyklus

    if meter_index == 1:  # Strom
        return {
            "product": "Emlog - Electronic Meter Log",
            "version": 1.16,
            "Zaehlerstand_Bezug": {"Stand180": base_consumption + consumption_offset, "Stand181": 0, "Stand182": 0},
            "Zaehlerstand_Lieferung": {"Stand280": 0, "Stand281": 0, "Stand282": 0},
            "Wirkleistung_Bezug": {
                "Leistung170": 2.5 + random.uniform(-0.5, 0.5),
                "Leistung171": 0,
                "Leistung172": 0,
                "Leistung173": 0,
            },
            "Wirkleistung_Lieferung": {"Leistung270": 0, "Leistung271": 0, "Leistung272": 0, "Leistung273": 0},
            "Kwh_Bezug": {"Kwh180": 15.7 + random.uniform(-2, 2), "Kwh181": 0, "Kwh182": 0},
            "Kwh_Lieferung": {"Kwh280": 0, "Kwh281": 0, "Kwh282": 0},
            "Betrag_Bezug": {
                "Betrag180": 3.25 + random.uniform(-0.5, 0.5),
                "Betrag181": 0,
                "Betrag182": 0,
                "Waehrung": "EUR",
            },
            "Betrag_Lieferung": {"Betrag280": 0, "Betrag281": 0, "Betrag282": 0, "Waehrung": "EUR"},
            "DiffBezugLieferung": {"Betrag": -(3.25 + random.uniform(-0.5, 0.5))},
        }
    else:  # Gas
        return {
            "product": "Emlog - Electronic Meter Log",
            "version": 1.16,
            "Zaehlerstand_Bezug": {"Stand180": base_consumption + consumption_offset, "Stand181": 0, "Stand182": 0},
            "Zaehlerstand_Lieferung": {"Stand280": 0, "Stand281": 0, "Stand282": 0},
            "Wirkleistung_Bezug": {
                "Leistung170": 0.8 + random.uniform(-0.1, 0.1),
                "Leistung171": 0,
                "Leistung172": 0,
                "Leistung173": 0,
            },
            "Wirkleistung_Lieferung": {"Leistung270": 0, "Leistung271": 0, "Leistung272": 0, "Leistung273": 0},
            "Kwh_Bezug": {"Kwh180": 8.3 + random.uniform(-1, 1), "Kwh181": 0, "Kwh182": 0},
            "Kwh_Lieferung": {"Kwh280": 0, "Kwh281": 0, "Kwh282": 0},
            "Betrag_Bezug": {
                "Betrag180": 1.85 + random.uniform(-0.2, 0.2),
                "Betrag181": 0,
                "Betrag182": 0,
                "Waehrung": "EUR",
            },
            "Betrag_Lieferung": {"Betrag280": 0, "Betrag281": 0, "Betrag282": 0, "Waehrung": "EUR"},
            "DiffBezugLieferung": {"Betrag": -(1.85 + random.uniform(-0.2, 0.2))},
        }


@app.route("/pages/getinformation.php")
def get_information():
    """Haupt-API-Endpunkt"""
    try:
        meter_index = str(int(request.args.get("meterindex", 1)))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid meterindex"}), 400

    if "export" in request.args:
        with STATE_LOCK:
            data = STATE.get(meter_index)
            # Sicherstellen, dass wir immer ein Dict liefern
            if data is None:
                try:
                    data = load_initial_data(int(meter_index))
                    STATE[meter_index] = data
                    save_state()
                except Exception as e:
                    print(f"Error loading data for meter {meter_index}: {e}")
                    return jsonify({"error": "Failed to load meter data"}), 500
            # Erstelle eine Kopie, um Lock-Probleme zu vermeiden
            import copy

            return jsonify(copy.deepcopy(data))

    return jsonify({"error": "Export parameter required"}), 400


@app.route("/")
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


def update_loop():
    """Erhöht alle 10s die Werte realistisch und persistiert den Zustand."""
    tick_counter = 0
    while True:
        time.sleep(TICK_SECONDS)
        tick_counter += 1
        try:
            with STATE_LOCK:
                # Strom (Index 1)
                s = STATE.get("1")
                if s:
                    # Zählerstand (kWh) - monoton steigend
                    s["Zaehlerstand_Bezug"]["Stand180"] = (
                        float(s["Zaehlerstand_Bezug"]["Stand180"]) + ELECTRICITY_INC_KWH
                    )
                    # Tagesverbrauch (kWh) - monoton steigend
                    s["Kwh_Bezug"]["Kwh180"] = float(s["Kwh_Bezug"]["Kwh180"]) + ELECTRICITY_INC_KWH

                    # Wirkleistung (W) - realistische Haushalts-Leistung (150-300W durchschnittlich)
                    # Berechne durchschnittliche Watt: (kWh/Tag) / 24h
                    # Aber: kWh/Tag ist schon in kWh, also: (kWh/24) * 1000 W/kW = Watt
                    # Für 35 kWh/Tag: 35/24 = 1.458 kWh/h = 1458 W (FALSCH!)
                    # Richtig: 35 kWh/Tag = 35000 Wh/Tag; 35000Wh / 24h / 60min / 60s = 405 W durchschnittlich
                    # ODER: (35 kWh / 24h) * 1000 W/kW = 1458W (das ist kWh/h in Watt - aber kWh ist bereits ENERGIE!)
                    # Korrektur: Durchschnittliche MOMENTANE Leistung sollte VIEL kleiner sein
                    # Bei 35 kWh/Tag über 24h: durchschnittlich 35000Wh / 86400s = 0.405 W (!!! das ist viel zu klein)
                    # Ah, ich sehe meinen Fehler: 35 kWh/Tag ist nicht klein, aber 1458W durchschnitt ist auch nicht realistisch
                    # Realität: Ein Haushalt mit 35 kWh/Tag hat durchschnittlich ~150-200W wenn man "Wirkleistung" meint
                    # Aber ein Emlog misst ja momentane Leistung die schwankt. Realistische Werte: 100-500W
                    # Für simulierte realistische Haushalts-Last: sanfte Schwankung um 200W mit 10-50W Varianz
                    realistic_avg_w = 200.0  # Realistische durchschnittliche Haushaltsleistung (~200W)
                    # Leichte tägliche Schwankung simulieren (weniger nachts, mehr tagsüber)
                    hour_of_day = (tick_counter * TICK_SECONDS) % 86400 / 3600.0
                    daily_factor = 0.5 + 0.5 * (1.0 + (0.5 * (math.sin(hour_of_day * 3.14159 / 12.0)))) / 2.0
                    base_power = realistic_avg_w * daily_factor
                    # Kleine Schwankungen hinzufügen (±10%)
                    fluctuation = random.uniform(-10, 10)
                    s["Wirkleistung_Bezug"]["Leistung170"] = max(0.0, base_power + fluctuation)

                    # Betrag (angenommen 0.30 EUR/kWh)
                    s["Betrag_Bezug"]["Betrag180"] = float(s["Betrag_Bezug"]["Betrag180"]) + ELECTRICITY_INC_KWH * 0.30
                    s["DiffBezugLieferung"]["Betrag"] = -abs(float(s["Betrag_Bezug"]["Betrag180"]))

                # Gas (Index 2)
                g = STATE.get("2")
                if g:
                    # Zählerstand (m³) aus kWh via Näherung - monoton steigend
                    g["Zaehlerstand_Bezug"]["Stand180"] = float(g["Zaehlerstand_Bezug"]["Stand180"]) + GAS_INC_M3
                    # Tagesverbrauch (kWh) - monoton steigend
                    g["Kwh_Bezug"]["Kwh180"] = float(g["Kwh_Bezug"]["Kwh180"]) + GAS_INC_KWH

                    # Wirkleistung (W) - für Gas, typisch viel niedriger (Heizung hat weniger momentane Spitzen)
                    # Bei 75 kWh/Tag Gas: realistische durchschnittliche Leistung ~150-200W
                    realistic_avg_w_gas = 150.0
                    # Stärkere tägliche Variation (nachts mehr Heizung)
                    hour_of_day = (tick_counter * TICK_SECONDS) % 86400 / 3600.0
                    daily_factor_gas = 1.5 - 0.5 * (1.0 + (0.7 * (math.sin(hour_of_day * 3.14159 / 12.0)))) / 2.0
                    base_power_gas = realistic_avg_w_gas * daily_factor_gas
                    # Kleine Schwankungen hinzufügen (±5%)
                    fluctuation_gas = random.uniform(-7, 7)
                    g["Wirkleistung_Bezug"]["Leistung170"] = max(0.0, base_power_gas + fluctuation_gas)

                    # Betrag (angenommen 0.11 EUR/kWh)
                    g["Betrag_Bezug"]["Betrag180"] = float(g["Betrag_Bezug"]["Betrag180"]) + GAS_INC_KWH * 0.11
                    g["DiffBezugLieferung"]["Betrag"] = -abs(float(g["Betrag_Bezug"]["Betrag180"]))
        except Exception as e:
            print(f"Error in update_loop: {e}")


if __name__ == "__main__":
    # Erstelle Mock-Daten-Verzeichnis falls nicht vorhanden
    os.makedirs(MOCK_DATA_DIR, exist_ok=True)

    # Zustand laden oder initialisieren
    load_state()

    print(f"Starting Emlog Mock Server on port 8080")
    print(f"Mock data directory: {MOCK_DATA_DIR}")
    print(f"State file: {STATE_FILE}")
    print(f"Electricity daily: {ELECTRICITY_DAILY_KWH:.2f} kWh -> +{ELECTRICITY_INC_KWH:.6f} kWh per {TICK_SECONDS}s")
    print(f"Gas daily: {GAS_DAILY_KWH:.2f} kWh -> +{GAS_INC_KWH:.6f} kWh per {TICK_SECONDS}s (~+{GAS_INC_M3:.6f} m³)")

    # Hintergrund-Thread starten
    t = threading.Thread(target=update_loop, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
