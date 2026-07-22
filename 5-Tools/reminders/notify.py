"""
Deadline reminders — Japan 2027 checklist.

Dates from the master document (2-Datos-del-Viaje/2.1-Datos-e-Items-Completos.md).
"""

import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DEADLINES_FILE = SCRIPT_DIR / "deadlines.json"

DEFAULT_DEADLINES = [
    {
        "task": "Fondo separado",
        "date": "2026-07-01",
        "remind_days_before": [30, 14, 7, 1],
        "notes": "Separar cuenta de ahorro dedicada al viaje"
    },
    {
        "task": "Sistema de vigilancia de vuelos activo",
        "date": "2026-07-31",
        "remind_days_before": [14, 7],
        "notes": "Links de vigilancia + bitacora funcionando"
    },
    {
        "task": "Aporte de ella activo",
        "date": "2026-10-01",
        "remind_days_before": [30, 14, 7],
        "notes": "+600,000/mes COP"
    },
    {
        "task": "Turkish carga inventario 2027",
        "date": "2026-11-01",
        "remind_days_before": [30, 14, 7, 1],
        "notes": "Antes de esta fecha las cotizaciones 2027 NO son fiables"
    },
    {
        "task": "Black Friday (condicional)",
        "date": "2026-11-29",
        "remind_days_before": [14, 7, 3, 1],
        "notes": "Solo si hay tarifa base 2026 clara"
    },
    {
        "task": "Pasaportes",
        "date": "2027-03-31",
        "remind_days_before": [60, 30, 14, 7],
        "notes": "Tramitar/renovar pasaportes colombianos"
    },
    {
        "task": "Vacaciones por escrito",
        "date": "2027-05-31",
        "remind_days_before": [30, 14, 7],
        "notes": "15 dias habiles confirmados con empleador"
    },
    {
        "task": "COMPRAR MULTI-CITY Turkish (~11.8M COP)",
        "date": "2027-06-30",
        "remind_days_before": [60, 30, 14, 7, 3],
        "notes": "Mayor pago del viaje. BOG-IST-TYO-IST-BOG como un PNR"
    },
    {
        "task": "Shuttles MDE-BOG",
        "date": "2027-07-31",
        "remind_days_before": [30, 14, 7],
        "notes": "Avianca/LATAM, comprar mas cerca del viaje"
    },
    {
        "task": "RADICAR VISA JAPON",
        "date": "2027-08-01",
        "remind_days_before": [90, 60, 30, 14, 7, 3, 1],
        "notes": "LA FECHA MAS IMPORTANTE. Presencial en Bogota, min 13 dias habiles, sin opcion expres. Requiere itinerario dia por dia + vuelos."
    },
    {
        "task": "Ryokan Hakone + hotel Kioto",
        "date": "2027-08-31",
        "remind_days_before": [30, 14, 7],
        "notes": "Pico de momiji se llena con anticipacion"
    },
    {
        "task": "Hoteles restantes",
        "date": "2027-09-30",
        "remind_days_before": [30, 14, 7],
        "notes": "Tokio, Kanazawa, Osaka, Hiroshima, Estambul"
    },
    {
        "task": "Trenes (SmartEX)",
        "date": "2027-10-15",
        "remind_days_before": [30, 14, 7],
        "notes": "Hasta 30% descuento comprando anticipado"
    },
    {
        "task": "Visit Japan Web + eSIM",
        "date": "2027-10-20",
        "remind_days_before": [14, 7, 3],
        "notes": "Registro online pre-viaje"
    },
    {
        "task": "Solicitar Stopover Turkish",
        "date": "2027-11-17",
        "remind_days_before": [7, 3, 1],
        "notes": "Con el PNR, 72h antes. Hotel 4* gratis noche del 21 nov"
    },
    {
        "task": "Divisas y maleta",
        "date": "2027-10-27",
        "remind_days_before": [14, 7, 3, 1],
        "notes": "Compra de yenes y preparar equipaje"
    },
    {
        "task": "DESPEGUE",
        "date": "2027-10-28",
        "remind_days_before": [30, 14, 7, 3, 1],
        "notes": "MDE->BOG 13:00, Turkish BOG->IST 17:00"
    }
]


def load_deadlines():
    if not DEADLINES_FILE.exists():
        DEADLINES_FILE.write_text(json.dumps(DEFAULT_DEADLINES, indent=2, ensure_ascii=False))
        print(f"Created deadlines at {DEADLINES_FILE}")
        return DEFAULT_DEADLINES
    return json.loads(DEADLINES_FILE.read_text(encoding="utf-8"))


def check_deadlines():
    deadlines = load_deadlines()
    today = datetime.now().date()
    alerts = []
    upcoming = []

    for d in deadlines:
        deadline_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        days_until = (deadline_date - today).days

        if days_until < 0:
            alerts.append(("OVERDUE", abs(days_until), d))
        elif days_until == 0:
            alerts.append(("TODAY", 0, d))
        elif days_until <= 7:
            alerts.append(("THIS WEEK", days_until, d))
        elif days_until in d["remind_days_before"]:
            upcoming.append((days_until, d))

    if alerts:
        print("=" * 55)
        print("  ALERTAS")
        print("=" * 55)
        for severity, days, d in alerts:
            if severity == "OVERDUE":
                print(f"  !! VENCIDO hace {days} dias: {d['task']}")
            elif severity == "TODAY":
                print(f"  >> HOY: {d['task']}")
            else:
                print(f"  > {days} dias: {d['task']}")
            if d.get("notes"):
                print(f"    {d['notes']}")
            print()

    if upcoming:
        print("=" * 55)
        print("  PROXIMOS")
        print("=" * 55)
        for days, d in sorted(upcoming):
            print(f"  {days} dias — {d['task']} ({d['date']})")
        print()

    if not alerts and not upcoming:
        print("Sin recordatorios para hoy.")

    return alerts


if __name__ == "__main__":
    check_deadlines()
