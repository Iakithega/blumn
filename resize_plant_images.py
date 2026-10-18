#!/usr/bin/env python
"""Skaliert die Pflanzenbilder auf Web-Groesse herunter.

Hintergrund: Die Originale kommen direkt aus der Handykamera (4000x3000 px).
Angezeigt werden sie in overview/page.tsx als 400x320 CSS-Pixel Kachel.
Ein 4000x3000 JPEG belegt im Browser 4000*3000*4 Bytes = 45,8 MB als
dekodiertes Bitmap - unabhaengig davon, wie gut die Datei komprimiert ist.
Ueber alle 35 Bilder summiert das auf knapp 1 GB RAM im Browser-Tab.

Nur Herunterskalieren senkt den RAM-Verbrauch. Bessere JPEG-Kompression
spart Bandbreite, aber kein einziges Byte Arbeitsspeicher.

Aufruf:
    .venv/Scripts/python.exe resize_plant_images.py --dry-run   # nur zeigen
    .venv/Scripts/python.exe resize_plant_images.py             # schreiben
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

IMAGE_DIR = Path(__file__).parent / "frontend" / "public" / "plant_images"

# Die Kachel in overview/page.tsx: maxWidth 400, height 320, objectFit cover.
DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 320

# Die kurze Bildkante wird auf diesen Wert gedeckelt. 800 deckt die Kachel auf
# einem 2x-Retina-Display (800x640 echte Pixel) in beiden Formaten vollstaendig
# ab - bewusst grosszuegig gewaehlt, damit nichts pixelig wirkt.
MAX_SHORT_EDGE = 800


def target_size(width: int, height: int) -> tuple[int, int]:
    """Bestimmt die Zielaufloesung fuer ein Bild der Groesse width x height.

    Gibt (neue_breite, neue_hoehe) zurueck. Das Seitenverhaeltnis MUSS
    erhalten bleiben, sonst verzerrt objectFit: 'cover' die Pflanzen.

    Gibt die unveraenderte Groesse zurueck, wenn das Bild schon klein genug
    ist - kleine Bilder sollen nicht hochskaliert werden (das kostet nur
    Qualitaet und Speicher).

    Begrenzt wird die KURZE Kante, nicht die lange. Grund: objectFit 'cover'
    skaliert mit max(boxBreite/bildBreite, boxHoehe/bildHoehe), um die Kachel
    vollstaendig zu fuellen - gemessen wird das Bild also an seiner knappsten
    Dimension. Wuerde man die lange Kante deckeln, kaeme ein Hochformat wie
    2606x3928 bei 531x800 heraus und waere auf der Breite sichtbar unscharf.
    """
    short = min(width, height)
    if short <= MAX_SHORT_EDGE:
        return width, height

    scale = MAX_SHORT_EDGE / short
    return round(width * scale), round(height * scale)


# JPEG-Qualitaet beim Speichern. Beeinflusst NUR die Dateigroesse, nicht den
# RAM-Verbrauch im Browser (der haengt allein an Breite*Hoehe*4). Deshalb hier
# bewusst hoch angesetzt - der Speichergewinn bleibt davon unberuehrt.
JPEG_QUALITY = 90


def process(path: Path, dry_run: bool) -> tuple[int, int, int, int]:
    """Verarbeitet ein Bild.

    Gibt (bytes_vorher, bytes_nachher, ram_vorher, ram_nachher) zurueck.
    Der RAM-Wert ist Breite*Hoehe*4 - das dekodierte Bitmap im Browser.
    Er ist die eigentlich relevante Kennzahl, nicht die Dateigroesse.
    """
    size_before = path.stat().st_size

    with Image.open(path) as img:
        # Handyfotos speichern die Ausrichtung als EXIF-Tag statt die Pixel
        # zu drehen. exif_transpose dreht die Pixel und entfernt das Tag -
        # ohne das landen Hochformat-Bilder nach dem Resize quer.
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")

        old_w, old_h = img.size
        new_w, new_h = target_size(old_w, old_h)

        ram_before = old_w * old_h * 4
        ram_after = new_w * new_h * 4

        if (new_w, new_h) == (old_w, old_h):
            print(f"  uebersprungen (schon klein genug)  {old_w}x{old_h}  {path.name}")
            return size_before, size_before, ram_before, ram_after
        print(
            f"  {old_w}x{old_h} -> {new_w}x{new_h}   "
            f"RAM {ram_before / 1024 / 1024:.1f} MB"
            f" -> {ram_after / 1024 / 1024:.1f} MB   {path.name}"
        )

        if dry_run:
            return size_before, size_before, ram_before, ram_after

        # LANCZOS ist der hochwertigste Downscale-Filter in Pillow - beim
        # starken Verkleinern von Fotos sichtbar sauberer als BILINEAR.
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # optimize + progressive: kleinere Datei, laedt sichtbar angenehmer.
        resized.save(
            path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
        )

    return size_before, path.stat().st_size, ram_before, ram_after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur anzeigen, was passieren wuerde - nichts ueberschreiben.",
    )
    args = parser.parse_args()

    images = sorted(IMAGE_DIR.glob("*.jpg"))
    if not images:
        print(f"Keine Bilder gefunden in {IMAGE_DIR}", file=sys.stderr)
        return 1

    mode = "DRY RUN - es wird nichts geschrieben" if args.dry_run else "SCHREIBE"
    print(f"{mode}  |  {len(images)} Bilder in {IMAGE_DIR}\n")

    total_before = total_after = 0
    ram_before = ram_after = 0
    for path in images:
        before, after, rb, ra = process(path, args.dry_run)
        total_before += before
        total_after += after
        ram_before += rb
        ram_after += ra

    mb = 1024 * 1024
    print()
    print(f"{'':26}{'vorher':>12}{'nachher':>12}{'Faktor':>9}")
    print(
        f"{'Dateien (Netzwerk)':26}{total_before / mb:>9.1f} MB"
        f"{total_after / mb:>9.1f} MB{total_before / max(total_after, 1):>8.1f}x"
    )
    print(
        f"{'Dekodiert (Browser-RAM)':26}{ram_before / mb:>9.1f} MB"
        f"{ram_after / mb:>9.1f} MB{ram_before / max(ram_after, 1):>8.1f}x"
    )
    if args.dry_run:
        print()
        print("Dry run: Dateigroesse unveraendert, da nichts geschrieben wurde.")
        print("Der RAM-Wert ist echt - er haengt allein an der Aufloesung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
