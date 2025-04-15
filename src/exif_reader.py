#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# /src/exif_reader.py
# Modul zum Extrahieren von EXIF-GPS-Daten aus Dateien
# Updated 2025-03-17

"""
Modul zum Extrahieren von EXIF-GPS-Daten aus Dateien.

Dieses Modul liest EXIF-Metadaten aus Dateien und extrahiert
GPS-Koordinaten und Zeitstempel für die GPX-Erzeugung.
"""

import os
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ExifReader:
    """Klasse zum Lesen von EXIF-Daten aus Dateien, mit Fokus auf GPS-Informationen."""

    @staticmethod
    def extract_gps_data(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Extrahiert GPS-Daten aus einer Datei.

        Args:
            file_path: Pfad zur Datei

        Returns:
            Dictionary mit GPS-Informationen (Breitengrad, Längengrad, Zeitstempel)
            oder None, wenn GPS-Daten nicht extrahiert werden können
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            
            if not exif_data:
                return None
                
            # Alle EXIF-Tags abrufen
            labeled_exif = {
                TAGS.get(key, key): value
                for key, value in exif_data.items()
            }
            
            # Prüfen, ob GPS-Informationen vorhanden sind
            if 'GPSInfo' not in labeled_exif:
                return None
                
            gps_info = labeled_exif['GPSInfo']
            
            # GPS-Daten abrufen
            gps_data = {
                GPSTAGS.get(key, key): value
                for key, value in gps_info.items()
            }
            
            # Koordinaten extrahieren
            if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                lat = ExifReader._convert_to_degrees(gps_data['GPSLatitude'])
                lon = ExifReader._convert_to_degrees(gps_data['GPSLongitude'])
                
                # Referenz prüfen (N/S, E/W)
                if 'GPSLatitudeRef' in gps_data and gps_data['GPSLatitudeRef'] == 'S':
                    lat = -lat
                if 'GPSLongitudeRef' in gps_data and gps_data['GPSLongitudeRef'] == 'W':
                    lon = -lon
                    
                result = {
                    'latitude': lat,
                    'longitude': lon,
                    'name': os.path.basename(file_path)
                }
                
                # Zeitstempel abrufen
                if 'DateTime' in labeled_exif:
                    date_str = labeled_exif['DateTime']
                    try:
                        timestamp = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                        result['timestamp'] = timestamp
                    except ValueError:
                        result['timestamp'] = datetime.now()
                else:
                    result['timestamp'] = datetime.now()
                
                return result
            
            return None
                
        except Exception as e:
            print(f"Fehler beim Extrahieren von EXIF-Daten aus {file_path}: {e}")
            return None
            
    @staticmethod
    def _convert_to_degrees(value: Tuple) -> float:
        """
        Konvertiert GPS-Koordinaten von Grad, Minuten, Sekunden-Format nach Dezimalgrad.
        
        Args:
            value: Tupel von (Grad, Minuten, Sekunden)
            
        Returns:
            Dezimalgrad als Float
        """
        degrees = float(value[0])
        minutes = float(value[1])
        seconds = float(value[2])
            
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
