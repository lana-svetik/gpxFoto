# gpxFoto

Ein leichtgewichtiges Command-Line-Tool (CLI) zur Erstellung von GPX-Tracks aus geogetaggten Fotos. Erstellt unter Anleitung von Claude 3.7 Sonnet.

## Beschreibung

gpxFoto extrahiert GPS-Metadaten aus deinen Dateien und erstellt daraus GPX-Dateien, die in verschiedenen Kartenanwendungen und GPS-Geräten verwendet werden können.

Dieses Projekt wurde in Anlehnung an [pixTrail](https://github.com/sukitsubaki/pixTrail) entwickelt und stellt eine zusätzliche Implementation des Konzepts mit leicht unterschiedlichem Fokus dar.

## Funktionen

- Extraktion von GPS-Daten (Breitengrad, Längengrad, Zeitstempel) aus EXIF-Metadaten
- Unterstützung für verschiedene Dateiformate (JPG, PNG, TIFF, RAW-Formate)
- Einfache Drag-and-Drop-Funktionalität im Terminal
- Sortierung der Wegpunkte nach Zeitstempel

## Installation

```bash
pip install gpxfoto
```

Oder direkt aus dem Repository:

```bash
git clone https://github.com/lana-svetik/gpxFoto.git
cd gpxFoto
pip install -e .
```

## Verwendung

```bash
gpxfoto /pfad/zu/deinen/dateien
```

Optional kannst du den Ausgabepfad angeben:

```bash
gpxfoto /pfad/zu/deinen/dateien -o /pfad/zur/ausgabe.gpx
```

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
