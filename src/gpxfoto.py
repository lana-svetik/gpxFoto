#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# /src/gpxfoto.py
# Hauptmodul des gpxFoto-Tools
# Updated 2025-03-25

"""
Hauptmodul des gpxFoto-Tools.

Dieses Modul bietet die Hauptfunktionalität des gpxFoto-Tools,
einschließlich der Kommandozeilenoberfläche und der Hauptverarbeitungslogik
zur Extraktion von GPS-Daten und Erstellung von GPX-Tracks.
"""

import argparse
import os
import sys
from typing import List, Optional

from .exif_reader import ExifReader
from .gpx_generator import GPXGenerator
from .utils import get_image_files, ensure_directory, get_default_output_path


def parse_args() -> argparse.Namespace:
    """
    Verarbeitet die Kommandozeilenargumente.
    
    Returns:
        Verarbeitete Argumente als Namespace-Objekt
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "input_paths",
        nargs="+",
    )
    
    parser.add_argument(
        "-o", "--output",
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
    )
    
    return parser.parse_args()


def process_path(input_path: str, recursive: bool = False) -> List[dict]:
    """
    Verarbeitet einen Pfad (Datei oder Verzeichnis) und extrahiert GPS-Daten.
    
    Args:
        input_path: Pfad zur Datei oder zum Verzeichnis
        recursive: Ob rekursiv in Unterverzeichnissen gesucht werden soll
    
    Returns:
        Liste mit Dictionaries, die die extrahierten GPS-Daten enthalten
    """
    # Prüfen, ob input_path ein Verzeichnis oder eine Datei ist
    if os.path.isfile(input_path):
        files = [input_path]
    else:
        try:
            files = get_image_files(input_path, recursive)
                
        except FileNotFoundError as e:
            print(f"Fehler: {e}")
            return []
    
    if not files:
        print(f"Keine Dateien gefunden in: {input_path}")
        return []
    
    # Jede Datei verarbeiten
    gps_data_list = []
    processed_count = 0
    skipped_count = 0
    
    for file in files:
        gps_data = ExifReader.extract_gps_data(file)
        
        if gps_data:
            gps_data_list.append(gps_data)
            processed_count += 1
        else:
            skipped_count += 1
            
    print(f"{processed_count} Dateien mit GPS-Daten verarbeitet, {skipped_count} Dateien ohne GPS-Daten übersprungen.")
    
    return gps_data_list


def main() -> int:
    """
    Haupteinstiegspunkt für die Kommandozeilenschnittstelle.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    # Argumente verarbeiten
    args = parse_args()
    
    # Prüfen, ob Eingaben angegeben wurden
    if not args.input_paths:
        print("Fehler: Keine Eingabeordner oder -dateien angegeben.")
        print("Verwendung: gpxfoto <ordner_oder_datei> [weitere_ordner_oder_dateien...] [Optionen]")
        return 1
    
    # Alle GPS-Daten aus allen Eingabepfaden sammeln
    all_gps_data = []
    
    for input_path in args.input_paths:
        # Prüfen, ob der Eingabeordner oder die Datei existiert
        if not os.path.exists(input_path):
            print(f"Fehler: Eingabeordner oder -datei existiert nicht: {input_path}")
            continue
        
        try:
            # GPS-Daten aus Dateien extrahieren und zur Gesamtliste hinzufügen
            gps_data_list = process_path(
                input_path,
                args.recursive
            )
            all_gps_data.extend(gps_data_list)
            
        except Exception as e:
            print(f"Fehler bei der Verarbeitung von {input_path}: {e}")
    
    if not all_gps_data:
        print("Keine GPS-Daten zum Erstellen einer GPX-Datei gefunden.")
        return 1
    
    try:
        # Ausgabepfad festlegen
        output_path = args.output
        if not output_path:
            # Bestimme den Basisordner (Ordner des ersten Eingabepfads)
            if os.path.isfile(args.input_paths[0]):
                base_dir = os.path.dirname(args.input_paths[0])
            else:
                base_dir = args.input_paths[0]
            
            # Immer gpxFoto.gpx als Namen verwenden
            output_path = os.path.join(base_dir, "gpxFoto.gpx")
        
        # Sicherstellen, dass das Ausgabeverzeichnis existiert
        output_dir = os.path.dirname(os.path.abspath(output_path))
        ensure_directory(output_dir)
        
        # GPX-Datei erstellen
        success = GPXGenerator.create_gpx(all_gps_data, output_path)
        
        if success:
            print(f"GPX-Datei erfolgreich erstellt: {output_path}")
            return 0
        else:
            print("Fehler beim Erstellen der GPX-Datei.")
            return 1
            
    except Exception as e:
        print(f"Fehler: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
