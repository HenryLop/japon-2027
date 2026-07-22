"""
Flight price tracker — Turkish multi-city BOG⇄IST⇄TYO.

Uses SerpAPI (free tier: 100 searches/month).
Get your API key at https://serpapi.com/

Set SERPAPI_KEY as env variable or GitHub Actions secret.
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
PRICES_FILE = SCRIPT_DIR / "prices.csv"
CONFIG_FILE = SCRIPT_DIR / "config.json"

DEFAULT_CONFIG = {
    "routes": [
        {"from": "BOG", "to": "IST", "date": "2027-10-28", "label": "seg1-bog-ist"},
        {"from": "IST", "to": "TYO", "date": "2027-10-31", "label": "seg2-ist-tyo"},
        {"from": "TYO", "to": "IST", "date": "2027-11-20", "label": "seg3-tyo-ist"},
        {"from": "IST", "to": "BOG", "date": "2027-11-23", "label": "seg4-ist-bog"},
    ],
    "currency": "USD",
    "trm": 3950,
    "thresholds_usd_pp": {
        "compra_ya": 1300,
        "justo": 1500,
        "esperar": 1700
    }
}


def load_config():
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
        print(f"Created config at {CONFIG_FILE}")
        return DEFAULT_CONFIG
    return json.loads(CONFIG_FILE.read_text())


def get_verdict(usd_pp, thresholds):
    if usd_pp <= thresholds["compra_ya"]:
        return "COMPRA YA"
    elif usd_pp <= thresholds["justo"]:
        return "JUSTO"
    elif usd_pp <= thresholds["esperar"]:
        return "ESPERAR"
    else:
        return "PARTIR (plan B)"


def search_flights(config):
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        print("SERPAPI_KEY not set. Skipping API search.")
        print("Get a free key at https://serpapi.com/")
        return []

    results = []
    for route in config["routes"]:
        try:
            resp = requests.get("https://serpapi.com/search", params={
                "engine": "google_flights",
                "departure_id": route["from"],
                "arrival_id": route["to"],
                "outbound_date": route["date"],
                "currency": config["currency"],
                "api_key": api_key
            }, timeout=30)
            data = resp.json()

            if "best_flights" in data:
                for flight in data["best_flights"]:
                    price = flight.get("price", 0)
                    results.append({
                        "date_checked": datetime.now().isoformat()[:10],
                        "segment": route["label"],
                        "from": route["from"],
                        "to": route["to"],
                        "travel_date": route["date"],
                        "price_usd": price,
                        "price_cop": int(price * config["trm"]),
                        "airline": flight.get("flights", [{}])[0].get("airline", "Unknown"),
                        "duration": flight.get("total_duration", "N/A"),
                    })
        except Exception as e:
            print(f"Error searching {route['label']}: {e}")

    return results


def save_results(results):
    file_exists = PRICES_FILE.exists()
    fieldnames = [
        "date_checked", "segment", "from", "to", "travel_date",
        "price_usd", "price_cop", "airline", "duration"
    ]
    with open(PRICES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} results to {PRICES_FILE}")


def analyze(results, config):
    if not results:
        return

    total_usd = sum(r["price_usd"] for r in results if isinstance(r["price_usd"], (int, float)))
    usd_pp = total_usd / 2
    cop_total = int(total_usd * config["trm"])
    verdict = get_verdict(usd_pp, config["thresholds_usd_pp"])

    print(f"\n{'='*50}")
    print(f"RESUMEN — Multi-city estimate")
    print(f"{'='*50}")
    print(f"Total (pareja):  USD {total_usd:,.0f}  /  COP {cop_total:,.0f}")
    print(f"Por persona:     USD {usd_pp:,.0f}")
    print(f"Veredicto:       {verdict}")
    print(f"{'='*50}")


if __name__ == "__main__":
    config = load_config()
    print("Searching Turkish multi-city segments...")
    results = search_flights(config)
    if results:
        save_results(results)
        analyze(results, config)
    else:
        print("No results. Check API key and config.")
