#!/usr/bin/env python3
"""
Fuegt neue Pflanzen hinzu und setzt eine Pflanze in den Ruhestand.

Hintergrund: Die Pflanzen-Liste wird aus den Excel-Zeilen abgeleitet
(ExcelHandler._get_plant_names). Da die Datums-Bloecke bis heute+7 schon
vorgeneriert sind, muessen neue Pflanzen in JEDEN existierenden Block ab
heute eingefuegt werden - sonst tauchen sie erst in einer Woche auf.
"""
import shutil
from datetime import datetime
from pathlib import Path

import openpyxl
from dateutil.parser import parse

DATA_FILE = Path("data/blumen_data.xlsx")

# Spaltenreihenfolge laut Header-Zeile:
# date | plant name | days without water | water | fertilizer |
# days without fertilizer | wash | neemoil | pestmix | nematoden | condition
N_COLS = 11

PLANTS_TO_ADD: list[str] = [
    "Zamioculcas zamiifolia Raven",
    "Gasteria Dragon Skin",
    "Haworthia limifolia Roux",
    "Haworthia cymbiformis",
]

# Wird nur zur Kontrolle geprueft; das eigentliche Ausblenden passiert
# ueber RETIRED_PLANTS in backend/app/core/excel_handler.py
PLANT_TO_RETIRE = "Sansevieria Laurentii"


def parse_date(value):
    """Datum aus Spalte 1 robust lesen (String 'TT.MM.JJJJ' oder datetime)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.strptime(str(value), "%d.%m.%Y").date()
    except ValueError:
        try:
            return parse(str(value), dayfirst=True).date()
        except Exception:
            return None


def build_row(plant_name: str, date_str: str) -> list:
    """
    Baut die Excel-Zeile fuer eine neue Pflanze an einem bestimmten Tag.

    Entscheidung: alle Pflegespalten bleiben leer. Damit liefert
    _get_last_care_date() fuer diese Pflanze None, days_since_watering wird
    None und needs_water bleibt False - bis zum ersten selbst eingetragenen
    Giessen. Keine erfundenen Giessereignisse, die die Periodizitaets-
    berechnung verfaelschen wuerden.

    None statt "" fuer die leeren Zellen: genau so sehen die bereits
    vorgenerierten Zukunftszeilen in der Datei aus.
    """
    return [date_str, plant_name] + [None] * (N_COLS - 2)


def main(data_file: Path = DATA_FILE, do_backup: bool = True):
    if not PLANTS_TO_ADD:
        raise SystemExit("PLANTS_TO_ADD ist leer - bitte Namen eintragen.")

    if do_backup:
        backup = data_file.with_name(
            f"blumen_data - backup {datetime.now():%d_%m_%Y}.xlsx"
        )
        shutil.copy2(data_file, backup)
        print(f"Backup: {backup}")

    wb = openpyxl.load_workbook(data_file)
    ws = wb.active
    today = datetime.now().date()

    # Alle Datums-Bloecke ab heute finden: Datum -> letzte Zeilennummer
    block_last_row: dict = {}
    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        date = parse_date(row[0])
        if date and date >= today:
            block_last_row[date] = idx

    existing = {n.strip().casefold() for n in PLANTS_TO_ADD}
    already = [
        r[1] for r in ws.iter_rows(min_row=2, values_only=True)
        if r[1] and str(r[1]).strip().casefold() in existing
    ]
    if already:
        raise SystemExit(f"Schon vorhanden, Abbruch: {sorted(set(already))}")

    # Von hinten nach vorne einfuegen, damit die Zeilennummern
    # der noch nicht bearbeiteten Bloecke gueltig bleiben
    for date in sorted(block_last_row, reverse=True):
        last_row = block_last_row[date]
        date_str = date.strftime("%d.%m.%Y")
        ws.insert_rows(last_row + 1, amount=len(PLANTS_TO_ADD))
        for offset, plant in enumerate(PLANTS_TO_ADD):
            values = build_row(plant, date_str)
            for col, value in enumerate(values, start=1):
                ws.cell(row=last_row + 1 + offset, column=col, value=value)

    wb.save(data_file)
    print(f"{len(PLANTS_TO_ADD)} Pflanzen in {len(block_last_row)} Tagesbloecke eingefuegt.")
    print(f"Noch offen: '{PLANT_TO_RETIRE}' in RETIRED_PLANTS eintragen "
          f"(backend/app/core/excel_handler.py:12)")


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_FILE
    main(target, do_backup=(target == DATA_FILE))
