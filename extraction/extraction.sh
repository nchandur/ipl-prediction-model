#!/bin/bash

echo "Extracting links..."
python3 extraction/extract_links.py

echo "Extracting scorecards..."
python3 extraction/extraction.py

echo "Extraction Complete!"