"""
Currency tracker — USD/COP and USD/JPY.

Uses the free ExchangeRate API (no key required).
"""

import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
HISTORY_FILE = SCRIPT_DIR / "rate_history.csv"


def get_rates():
    resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=15)
    data = resp.json()
    return {
        "COP": data["rates"]["COP"],
        "JPY": data["rates"]["JPY"],
    }


def save_history(rates):
    file_exists = HISTORY_FILE.exists()
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("date,usd_cop,usd_jpy\n")
        f.write(f"{datetime.now().isoformat()[:10]},{rates['COP']:.2f},{rates['JPY']:.2f}\n")


if __name__ == "__main__":
    rates = get_rates()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"Exchange rates ({today}):")
    print(f"  1 USD = {rates['COP']:,.2f} COP")
    print(f"  1 USD = {rates['JPY']:,.2f} JPY")
    print(f"  TRM de trabajo: 3,950 COP (delta: {rates['COP'] - 3950:+,.0f})")

    save_history(rates)

    budget_usd = [8500, 9400, 10300]
    print(f"\nPresupuesto a tasa real:")
    for usd in budget_usd:
        print(f"  USD {usd:,} = COP {usd * rates['COP']:,.0f} = JPY {usd * rates['JPY']:,.0f}")
