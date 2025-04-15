#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Svetlana Sibiryakova
# setup.py
# Setup-Skript für die Installation des gpxFoto-Pakets
# Updated 2025-04-11

"""
Setup-Skript für die Installation des gpxFoto-Pakets.
"""

from setuptools import setup, find_packages
import os
import re

# Versionsnummer aus __init__.py lesen
with open(os.path.join('src', '__init__.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version_string = version_match.group(1)
    else:
        raise RuntimeError("Version nicht gefunden")

# README lesen für die lange Beschreibung
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="gpxfoto",
    version=version_string,
    author="Svetlana Sibiryakova",
    description="Ein Tool zur Erzeugung von GPX-Tracks aus geogetaggten Dateien",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lana-svetik/gpxFoto",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'Pillow>=9.0.0',
        'gpxpy>=1.5.0',
    ],
    entry_points={
        'console_scripts': [
            'gpxfoto=src.gpxfoto:main',
        ],
    },
)
