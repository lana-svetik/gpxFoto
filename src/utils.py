#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# /src/utils.py
# Hilfsfunktionen für das gpxFoto-Paket
# Updated 2025-03-17

"""
Hilfsfunktionen für das gpxFoto-Paket.
"""

import os
import glob
from typing import List, Tuple


def get_image_files(directory: str, recursive: bool = False) -> List[str]:
    """
    Holt eine Liste von Dateien aus einem Verzeichnis.
    
    Args:
        directory: Verzeichnis, in dem nach Dateien gesucht werden soll
        recursive: Ob rekursiv in Unterverzeichnissen gesucht werden soll
        
    Returns:
        Liste von Dateipfaden
    """
    # Verzeichnispfad normalisieren, um '..' aufzulösen und ein einheitliches Format zu gewährleisten
    normalized_directory = os.path.normpath(directory)
    
    # Unterstützte Dateierweiterungen
    file_extensions = ('*.jpg', '*.jpeg', '*.png', '*.tiff', '*.arw', '*.dng')
    
    # Prüfen, ob das Verzeichnis existiert
    if not os.path.isdir(normalized_directory):
        raise FileNotFoundError(f"Verzeichnis nicht gefunden: {normalized_directory}")
    
    # Liste zum Speichern gefundener Dateien
    files = []
    
    # Suchmuster
    pattern = os.path.join(normalized_directory, '**') if recursive else normalized_directory
    
    # Dateien finden
    for ext in file_extensions:
        if recursive:
            search_pattern = os.path.join(pattern, ext)
            files.extend(glob.glob(search_pattern, recursive=True))
        else:
            search_pattern = os.path.join(pattern, ext)
            files.extend(glob.glob(search_pattern))
    
    return sorted(files)


def ensure_directory(directory: str) -> bool:
    """
    Stellt sicher, dass ein Verzeichnis existiert, erstellt es, wenn nicht.
    
    Args:
        directory: Verzeichnispfad, dessen Existenz sichergestellt werden soll
        
    Returns:
        True, wenn das Verzeichnis existiert oder erfolgreich erstellt wurde, sonst False
    """
    try:
        # Verzeichnispfad normalisieren
        normalized_directory = os.path.normpath(directory)
        os.makedirs(normalized_directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Fehler beim Erstellen des Verzeichnisses {directory}: {e}")
        return False


def get_default_output_path(input_dir: str, filename: str = None) -> str:
    """
    Generiert einen Standardausgabepfad für die GPX-Datei basierend auf dem Eingabeverzeichnis.
    
    Args:
        input_dir: Eingabeverzeichnispfad
        filename: Name der Ausgabedatei (wenn None, verwende "gpxFoto.gpx")
        
    Returns:
        Standardausgabepfad für die GPX-Datei
    """
    if filename is None:
        filename = "gpxFoto.gpx"
    
    return os.path.join(input_dir, filename)


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """
    Validiert GPS-Koordinaten.
    
    Args:
        latitude: Zu validierende Breitengradwert (-90 bis 90)
        longitude: Zu validierende Längengradwert (-180 bis 180)
        
    Returns:
        Tupel von (ist_gültig, Fehlermeldung)
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False, "Koordinaten müssen numerische Werte sein"
    
    if not (-90 <= latitude <= 90):
        return False, f"Ungültiger Breitengradwert: {latitude}. Muss zwischen -90 und 90 liegen."
        
    if not (-180 <= longitude <= 180):
        return False, f"Ungültiger Längengradwert: {longitude}. Muss zwischen -180 und 180 liegen."
        
    return True, ""
