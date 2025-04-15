#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# /src/gpx_generator.py
# Modul zur Erzeugung von GPX-Dateien aus GPS-Daten
# Updated 2025-03-14

"""
Modul zur Erzeugung von GPX-Dateien aus GPS-Daten, die aus Dateien extrahiert wurden.
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any

import gpxpy
import gpxpy.gpx


class GPXGenerator:
    """Klasse zur Erzeugung von GPX-Dateien aus GPS-Daten."""
    
    @staticmethod
    def create_gpx(gps_data_list: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Erstellt eine GPX-Datei aus einer Liste von GPS-Datenpunkten.
        
        Args:
            gps_data_list: Liste von Dictionaries mit GPS-Daten
                         (Breitengrad, Längengrad, Zeitstempel, Name)
            output_path: Pfad, unter dem die GPX-Datei gespeichert wird
            
        Returns:
            bool: True, wenn die GPX-Datei erfolgreich erstellt wurde, sonst False
        """
        if not gps_data_list:
            print("Keine GPS-Daten verfügbar, um GPX-Datei zu erstellen.")
            return False
            
        # GPX-Struktur erstellen
        gpx = gpxpy.gpx.GPX()
        gpx.creator = "gpxFoto - GPS Foto Tracker"
        
        # Datenpunkte nach Zeitstempel sortieren, falls verfügbar
        sorted_data = sorted(
            gps_data_list, 
            key=lambda x: x.get('timestamp', datetime.now())
        )
        
        # Wegpunkte erstellen
        for point in sorted_data:
            # Prüfen, ob wir die minimal erforderlichen Daten haben
            if 'latitude' not in point or 'longitude' not in point:
                continue
                
            # Wegpunkt erstellen
            waypoint = gpxpy.gpx.GPXWaypoint(
                latitude=point['latitude'],
                longitude=point['longitude'],
                time=point.get('timestamp'),
                name=point.get('name', 'Unbekannt')
            )
            
            # Wegpunkt zur GPX-Datei hinzufügen
            gpx.waypoints.append(waypoint)
        
        # Eine Spur mit einem einzelnen Segment für den Pfad erstellen
        track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(track)
        
        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)
        
        # Spurpunkte zum Segment hinzufügen
        for point in sorted_data:
            # Prüfen, ob wir die minimal erforderlichen Daten haben
            if 'latitude' not in point or 'longitude' not in point:
                continue
                
            # Spurpunkt erstellen
            track_point = gpxpy.gpx.GPXTrackPoint(
                latitude=point['latitude'],
                longitude=point['longitude'],
                time=point.get('timestamp')
            )
            
            # Spurpunkt zum Segment hinzufügen
            segment.points.append(track_point)
        
        try:
            # Ausgabepfad normalisieren und validieren
            normalized_path = os.path.normpath(output_path)
            
            # Ausgabeverzeichnis erstellen, falls es nicht existiert
            output_dir = os.path.dirname(os.path.abspath(normalized_path))
            os.makedirs(output_dir, exist_ok=True)
            
            # GPX-Datei schreiben
            with open(normalized_path, 'w') as gpx_file:
                gpx_file.write(gpx.to_xml())
                
            return True
        except Exception as e:
            print(f"Fehler beim Erstellen der GPX-Datei: {e}")
            return False
