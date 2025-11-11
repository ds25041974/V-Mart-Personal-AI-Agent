#!/bin/bash

# Setup script for Google Maps integration
# Run this to configure the store locator for 1,800+ stores

set -e

echo "🚀 V-Mart Store Locator - Google Maps Setup"
echo "==========================================="
echo ""

# Step 1: Check Python environment
echo "Step 1: Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 found"

# Step 2: Install Google Maps package
echo ""
echo "Step 2: Installing Google Maps Python package..."
pip install --quiet googlemaps requests

if [ $? -eq 0 ]; then
    echo "✓ googlemaps package installed"
else
    echo "❌ Failed to install googlemaps package"
    exit 1
fi

# Step 3: Check for API key
echo ""
echo "Step 3: Checking for Google Maps API key..."
if [ -z "$GOOGLE_MAPS_API_KEY" ]; then
    echo "⚠️  GOOGLE_MAPS_API_KEY not set"
    echo ""
    echo "Please get your API key from:"
    echo "https://console.cloud.google.com/google/maps-apis"
    echo ""
    echo "Then set it:"
    echo "export GOOGLE_MAPS_API_KEY='your-api-key-here'"
    echo ""
    echo "Add to ~/.zshrc to make it permanent:"
    echo "echo 'export GOOGLE_MAPS_API_KEY=\"your-api-key\"' >> ~/.zshrc"
    echo ""
else
    echo "✓ API key found: ${GOOGLE_MAPS_API_KEY:0:10}..."
fi

# Step 4: Test Google Maps connection
echo ""
echo "Step 4: Testing Google Maps connection..."
if [ ! -z "$GOOGLE_MAPS_API_KEY" ]; then
    python3 -c "
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))
try:
    result = gmaps.geocode('Connaught Place, Delhi, India')
    if result:
        print('✓ Google Maps API working!')
    else:
        print('⚠️  API returned empty result')
except Exception as e:
    print(f'❌ API Error: {e}')
"
else
    echo "⏭️  Skipping (no API key)"
fi

# Step 5: Check database
echo ""
echo "Step 5: Checking database..."
DB_PATH="vmart_stores.db"
if [ -f "$DB_PATH" ]; then
    STORE_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM vmart_stores" 2>/dev/null || echo "0")
    COMPETITOR_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM competitor_stores" 2>/dev/null || echo "0")
    echo "✓ Database found"
    echo "  📍 V-Mart stores: $STORE_COUNT"
    echo "  🏪 Competitor stores: $COMPETITOR_COUNT"
else
    echo "ℹ️  Database not found (will be created on first import)"
fi

echo ""
echo "==========================================="
echo "Setup Status:"
echo ""

if [ ! -z "$GOOGLE_MAPS_API_KEY" ]; then
    echo "✅ Ready to import stores!"
    echo ""
    echo "Next steps:"
    echo "1. Prepare CSV with V-Mart store data (533 stores)"
    echo "2. Run: python src/stores/bulk_store_importer.py import-vmart vmart_stores.csv"
    echo "3. Run: python src/stores/bulk_store_importer.py auto-discover 'V2'"
    echo "4. Run: python src/stores/bulk_store_importer.py auto-discover 'Zudio'"
    echo "5. Run: python src/stores/bulk_store_importer.py auto-discover 'Style Bazar'"
else
    echo "⚠️  Please set GOOGLE_MAPS_API_KEY to continue"
    echo ""
    echo "Quick setup:"
    echo "1. Visit: https://console.cloud.google.com/google/maps-apis"
    echo "2. Create/select a project"
    echo "3. Enable: Geocoding API, Places API"
    echo "4. Create credentials → API key"
    echo "5. Run: export GOOGLE_MAPS_API_KEY='your-key'"
    echo "6. Run this script again"
fi

echo ""
