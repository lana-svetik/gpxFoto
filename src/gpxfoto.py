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
        "input_dir",
        nargs="?",
    )
    
    parser.add_argument(
        "-o", "--output",
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
    )
    
    return parser.parse_args()


def process_directory(input_dir: str, recursive: bool = False) -> List[dict]:
    """
    Verarbeitet alle Dateien in einem Verzeichnis und extrahiert GPS-Daten.
    
    Args:
        input_dir: Verzeichnis mit Dateien
        recursive: Ob rekursiv in Unterverzeichnissen gesucht werden soll
    
    Returns:
        Liste mit Dictionaries, die die extrahierten GPS-Daten enthalten
    """
    # Prüfen, ob input_dir ein Verzeichnis oder eine Datei ist
    if os.path.isfile(input_dir):
        files = [input_dir]
    else:
        try:
            files = get_image_files(input_dir, recursive)
                
        except FileNotFoundError as e:
            print(f"Fehler: {e}")
            return []
    
    if not files:
        print(f"Keine Dateien gefunden in: {input_dir}")
        return []
    
    # Jede Datei verarbeiten
    gps_data_list = []
    processed_count = 0
    
    for file in files:
        gps_data = ExifReader.extract_gps_data(file)
        
        if gps_data:
            gps_data_list.append(gps_data)
            processed_count += 1
            
    print(f"{processed_count} Dateien mit GPS-Daten verarbeitet.")
    
    return gps_data_list


def main() -> int:
    """
    Haupteinstiegspunkt für die Kommandozeilenschnittstelle.
    
    Returns:
        Exit-Code (0 für Erfolg, ungleich 0 für Fehler)
    """
    # Argumente verarbeiten
    args = parse_args()
    
    # Prüfen, ob eine Eingabe angegeben wurde
    if not args.input_dir:
        print("Fehler: Kein Eingabeordner oder -datei angegeben.")
        print("Verwendung: gpxfoto <ordner_oder_datei> [Optionen]")
        return 1
    
    # Prüfen, ob der Eingabeordner oder die Datei existiert
    if not os.path.exists(args.input_dir):
        print(f"Fehler: Eingabeordner oder -datei existiert nicht: {args.input_dir}")
        return 1
    
    try:
        # GPS-Daten aus Bildern extrahieren
        gps_data_list = process_directory(
            args.input_dir,
            args.recursive
        )
        
        if not gps_data_list:
            print("Keine GPS-Daten zum Erstellen einer GPX-Datei gefunden.")
            return 1
        
        # Ausgabepfad festlegen
        output_path = args.output
        if not output_path:
            if os.path.isfile(args.input_dir):
                # Wenn die Eingabe eine Datei ist, GPX im selben Verzeichnis erstellen
                input_dir = os.path.dirname(args.input_dir)
                base_name = os.path.splitext(os.path.basename(args.input_dir))[0]
                output_path = os.path.join(input_dir, f"{base_name}.gpx")
            else:
                # Wenn die Eingabe ein Verzeichnis ist, Standardnamen verwenden
                output_path = get_default_output_path(args.input_dir)
        
        # Sicherstellen, dass das Ausgabeverzeichnis existiert
        output_dir = os.path.dirname(os.path.abspath(output_path))
        ensure_directory(output_dir)
        
        # GPX-Datei erstellen
        success = GPXGenerator.create_gpx(gps_data_list, output_path)
        
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
