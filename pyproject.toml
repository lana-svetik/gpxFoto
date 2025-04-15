[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gpxfoto"
description = "Ein Tool zur Erzeugung von GPX-Tracks aus geogetaggten Dateien"
readme = "README.md"
requires-python = ">=3.7"
license = {text = "MIT"}
authors = [
    {name = "Svetlana Sibiryakova"}
]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "Pillow>=9.0.0",
    "gpxpy>=1.5.0",
]
dynamic = ["version"]

[project.urls]
"Homepage" = "https://github.com/lana-svetik/gpxFoto"
"Bug Tracker" = "https://github.com/lana-svetik/gpxFoto/issues"

[project.scripts]
gpxfoto = "src.gpxfoto:main"

[tool.setuptools.dynamic]
version = {attr = "src.__version__"}
