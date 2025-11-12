"""
Store Management API Routes
Flask blueprint for V-Mart store locations, competitor analysis, and weather data
"""

import os
from datetime import date, datetime

from flask import Blueprint, jsonify, render_template_string, request

from src.stores import (
    LocationService,
    StoreAnalyzer,
    StoreChain,
    StoreDatabase,
    WeatherService,
    create_location_service,
    get_temperature_color,
    get_weather_icon,
    initialize_stores,
)

# Create blueprint
stores_bp = Blueprint("stores", __name__, url_prefix="/stores")

# Initialize services
db = StoreDatabase("data/stores.db")
weather_service = WeatherService(os.getenv("OPENWEATHER_API_KEY"))
analyzer = StoreAnalyzer(db)
location_service = create_location_service()


@stores_bp.route("/initialize", methods=["POST"])
def initialize_database():
    """Initialize database with store data"""
    try:
        vmart_count, competitor_count = initialize_stores(db)
        return jsonify(
            {
                "success": True,
                "message": "Database initialized successfully",
                "vmart_stores": vmart_count,
                "competitor_stores": competitor_count,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/vmart", methods=["GET"])
def get_vmart_stores():
    """Get all V-Mart stores"""
    try:
        city = request.args.get("city")
        state = request.args.get("state")

        if city:
            stores = db.get_vmart_stores_by_city(city)
        elif state:
            stores = db.get_vmart_stores_by_state(state)
        else:
            stores = db.get_all_vmart_stores()

        return jsonify(
            {
                "success": True,
                "count": len(stores),
                "stores": [store.to_dict() for store in stores],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/vmart/<store_id>", methods=["GET"])
def get_vmart_store_details(store_id):
    """Get specific V-Mart store details"""
    try:
        store = db.get_vmart_store(store_id)
        if store:
            return jsonify({"success": True, "store": store.to_dict()})
        else:
            return jsonify({"success": False, "error": "Store not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/competitors", methods=["GET"])
def get_competitor_stores():
    """Get competitor stores"""
    try:
        chain = request.args.get("chain")
        city = request.args.get("city")

        if city:
            stores = db.get_competitor_stores_by_city(city)
        elif chain:
            try:
                chain_enum = StoreChain(chain)
                stores = db.get_competitor_stores(chain_enum)
            except ValueError:
                return jsonify({"success": False, "error": "Invalid chain name"}), 400
        else:
            stores = db.get_competitor_stores()

        return jsonify(
            {
                "success": True,
                "count": len(stores),
                "stores": [store.to_dict() for store in stores],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/weather/<latitude>/<longitude>", methods=["GET"])
def get_weather_for_location(latitude, longitude):
    """Get current weather for a location"""
    try:
        from src.stores.models import GeoLocation

        lat = float(latitude)
        lon = float(longitude)

        # Create temporary location object
        location = GeoLocation(
            latitude=lat,
            longitude=lon,
            address="",
            city=request.args.get("city", "Unknown"),
            state=request.args.get("state", "Unknown"),
            pincode="",
        )

        weather = weather_service.get_current_weather(location)

        if weather:
            return jsonify(
                {
                    "success": True,
                    "weather": weather.to_dict(),
                    "icon": get_weather_icon(weather.weather_condition),
                    "color": get_temperature_color(weather.temperature_celsius),
                }
            )
        else:
            return jsonify({"success": False, "error": "Weather data unavailable"}), 500

    except ValueError:
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/weather/forecast/<latitude>/<longitude>", methods=["GET"])
def get_weather_forecast(latitude, longitude):
    """Get weather forecast for a location"""
    try:
        from src.stores.models import GeoLocation

        lat = float(latitude)
        lon = float(longitude)
        days = int(request.args.get("days", 5))

        location = GeoLocation(
            latitude=lat,
            longitude=lon,
            address="",
            city=request.args.get("city", "Unknown"),
            state=request.args.get("state", "Unknown"),
            pincode="",
        )

        forecast = weather_service.get_forecast_weather(location, days)

        return jsonify(
            {
                "success": True,
                "count": len(forecast),
                "forecast": [w.to_dict() for w in forecast],
            }
        )

    except ValueError:
        return jsonify({"success": False, "error": "Invalid parameters"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/proximity-analysis/<store_id>", methods=["GET"])
def get_proximity_analysis(store_id):
    """Get competitor proximity analysis for a V-Mart store"""
    try:
        radius = float(request.args.get("radius", 5.0))

        analysis = analyzer.analyze_vmart_competition(store_id, radius)

        if analysis:
            return jsonify({"success": True, "analysis": analysis.to_dict()})
        else:
            return jsonify({"success": False, "error": "Store not found"}), 404

    except ValueError:
        return jsonify({"success": False, "error": "Invalid radius"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/proximity-analysis/all", methods=["GET"])
def get_all_proximity_analysis():
    """Get proximity analysis for all V-Mart stores"""
    try:
        radius = float(request.args.get("radius", 5.0))

        analyses = analyzer.analyze_all_vmart_stores(radius)

        return jsonify(
            {
                "success": True,
                "count": len(analyses),
                "analyses": [a.to_dict() for a in analyses],
            }
        )

    except ValueError:
        return jsonify({"success": False, "error": "Invalid radius"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/city/<city_name>", methods=["GET"])
def get_stores_by_city(city_name):
    """Get all stores (V-Mart and competitors) in a city"""
    try:
        data = analyzer.get_stores_by_city(city_name)
        return jsonify({"success": True, **data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/summary", methods=["GET"])
def get_competition_summary():
    """Get overall competition summary"""
    try:
        summary = analyzer.get_competition_summary()
        return jsonify({"success": True, **summary})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/map", methods=["GET"])
def show_stores_map():
    """Show interactive map with all stores"""
    try:
        # Get all stores
        vmart_stores = db.get_all_vmart_stores()
        competitor_stores = db.get_competitor_stores()

        # HTML template with Leaflet.js map
        map_html = """
<!DOCTYPE html>
<html>
<head>
    <title>V-Mart Store Locator - Geo Mapping & Weather</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        #map { 
            height: 100vh; 
            width: 100%; 
        }
        
        .legend {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            font-size: 14px;
            line-height: 24px;
        }
        
        .legend-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }
        
        .legend-item {
            margin: 5px 0;
            display: flex;
            align-items: center;
        }
        
        .legend-marker {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            display: inline-block;
        }
        
        .marker-vmart { background-color: #0066CC; }
        .marker-v2 { background-color: #FF6B35; }
        .marker-zudio { background-color: #9B59B6; }
        .marker-style-bazar { background-color: #E74C3C; }
        .marker-max { background-color: #F39C12; }
        .marker-pantaloons { background-color: #27AE60; }
        .marker-reliance { background-color: #3498DB; }
        .marker-westside { background-color: #8E44AD; }
        .marker-other { background-color: #95A5A6; }
        
        .store-popup {
            font-family: Arial, sans-serif;
            max-width: 300px;
        }
        
        .store-popup h3 {
            color: #0066CC;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .store-popup p {
            margin: 4px 0;
            font-size: 13px;
            color: #555;
        }
        
        .store-popup .chain {
            background: #f0f0f0;
            padding: 3px 8px;
            border-radius: 3px;
            display: inline-block;
            font-size: 11px;
            margin-top: 5px;
            font-weight: bold;
        }
        
        .weather-info {
            background: #e3f2fd;
            padding: 8px;
            border-radius: 5px;
            margin-top: 8px;
            font-size: 12px;
        }
        
        .weather-temp {
            font-size: 18px;
            font-weight: bold;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <script>
        // Initialize map centered on India
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        // Store data
        const vmartStores = {{ vmart_stores | safe }};
        const competitorStores = {{ competitor_stores | safe }};
        
        // Marker colors by chain
        const chainColors = {
            'V-Mart': '#0066CC',
            'V2 Retail': '#FF6B35',
            'Zudio': '#9B59B6',
            'Style Bazar': '#E74C3C',
            'Max Fashion': '#F39C12',
            'Pantaloons': '#27AE60',
            'Reliance Trends': '#3498DB',
            'Westside': '#8E44AD',
            'Other': '#95A5A6'
        };
        
        // Add V-Mart stores
        vmartStores.forEach(store => {
            const marker = L.circleMarker(
                [store.location.latitude, store.location.longitude],
                {
                    radius: 8,
                    fillColor: chainColors['V-Mart'],
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.8
                }
            );
            
            const popupContent = `
                <div class="store-popup">
                    <h3>🏪 ${store.store_name}</h3>
                    <p>📍 ${store.location.address}, ${store.location.city}</p>
                    <p>📞 ${store.phone || 'N/A'}</p>
                    <p>⏰ ${store.opening_hours || 'N/A'}</p>
                    <span class="chain" style="background: ${chainColors['V-Mart']}; color: white;">V-Mart</span>
                    <div class="weather-info" id="weather-${store.store_id}">
                        Loading weather...
                    </div>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            marker.addTo(map);
            
            // Load weather data
            marker.on('popupopen', function() {
                fetchWeather(store.location.latitude, store.location.longitude, store.store_id);
            });
        });
        
        // Add competitor stores
        competitorStores.forEach(store => {
            const color = chainColors[store.chain] || chainColors['Other'];
            
            const marker = L.circleMarker(
                [store.location.latitude, store.location.longitude],
                {
                    radius: 6,
                    fillColor: color,
                    color: '#fff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.7
                }
            );
            
            const popupContent = `
                <div class="store-popup">
                    <h3>🏬 ${store.store_name}</h3>
                    <p>📍 ${store.location.address}, ${store.location.city}</p>
                    <p>⏰ ${store.opening_hours || 'N/A'}</p>
                    <span class="chain" style="background: ${color}; color: white;">${store.chain}</span>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            marker.addTo(map);
        });
        
        // Add legend
        const legend = L.control({position: 'bottomright'});
        
        legend.onAdd = function(map) {
            const div = L.DomUtil.create('div', 'legend');
            div.innerHTML = `
                <div class="legend-title">Store Chains</div>
                <div class="legend-item">
                    <span class="legend-marker marker-vmart"></span> V-Mart
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-v2"></span> V2 Retail
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-zudio"></span> Zudio
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-style-bazar"></span> Style Bazar
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-max"></span> Max Fashion
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-pantaloons"></span> Pantaloons
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-reliance"></span> Reliance Trends
                </div>
                <div class="legend-item">
                    <span class="legend-marker marker-westside"></span> Westside
                </div>
            `;
            return div;
        };
        
        legend.addTo(map);
        
        // Fetch weather data
        async function fetchWeather(lat, lon, storeId) {
            try {
                const response = await fetch(`/stores/weather/${lat}/${lon}`);
                const data = await response.json();
                
                if (data.success) {
                    const weather = data.weather;
                    const weatherDiv = document.getElementById(`weather-${storeId}`);
                    if (weatherDiv) {
                        weatherDiv.innerHTML = `
                            <div>
                                ${data.icon} <span class="weather-temp">${weather.temperature_celsius.toFixed(1)}°C</span>
                            </div>
                            <div>${weather.weather_description}</div>
                            <div style="font-size: 11px; margin-top: 3px;">
                                Humidity: ${weather.humidity}% | Wind: ${weather.wind_speed.toFixed(1)} km/h
                            </div>
                        `;
                    }
                }
            } catch (error) {
                console.error('Error fetching weather:', error);
            }
        }
    </script>
</body>
</html>
        """

        # Prepare data for template
        import json

        vmart_data = json.dumps([s.to_dict() for s in vmart_stores])
        competitor_data = json.dumps([s.to_dict() for s in competitor_stores])

        html = map_html.replace("{{ vmart_stores | safe }}", vmart_data)
        html = html.replace("{{ competitor_stores | safe }}", competitor_data)

        return html

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ========== NEW ENHANCED FEATURES ==========


@stores_bp.route("/geocode", methods=["GET"])
def geocode_location():
    """
    Geocode a location (address or city) to coordinates

    Query params:
        query: Address or city name (e.g., "Mumbai" or "Connaught Place, Delhi")
        prefer: Preferred API - "google" or "weather" (default: "google")
    """
    try:
        query = request.args.get("query")
        prefer = request.args.get("prefer", "google")

        if not query:
            return jsonify(
                {"success": False, "error": "Missing 'query' parameter"}
            ), 400

        location = location_service.geocode(query, prefer=prefer)

        if location:
            return jsonify(
                {
                    "success": True,
                    "location": {
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "address": location.address,
                        "city": location.city,
                        "state": location.state,
                    },
                }
            )
        else:
            return jsonify({"success": False, "error": "Location not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/reverse-geocode", methods=["GET"])
def reverse_geocode_location():
    """
    Reverse geocode coordinates to location name

    Query params:
        lat: Latitude
        lon: Longitude
    """
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        if not lat or not lon:
            return jsonify(
                {"success": False, "error": "Missing lat/lon parameters"}
            ), 400

        result = location_service.reverse_geocode(float(lat), float(lon))

        if result:
            return jsonify({"success": True, "location": result})
        else:
            return jsonify({"success": False, "error": "Location not found"}), 404

    except ValueError:
        return jsonify({"success": False, "error": "Invalid lat/lon values"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/air-quality/<latitude>/<longitude>", methods=["GET"])
def get_air_quality_for_location(latitude, longitude):
    """Get air quality data for coordinates"""
    try:
        from src.stores.models import GeoLocation

        lat = float(latitude)
        lon = float(longitude)

        location = GeoLocation(
            latitude=lat,
            longitude=lon,
            address="",
            city=request.args.get("city", "Unknown"),
            state=request.args.get("state", "Unknown"),
            pincode="",
        )

        air_quality = weather_service.get_air_quality(location)

        if air_quality:
            return jsonify({"success": True, "air_quality": air_quality})
        else:
            return jsonify(
                {"success": False, "error": "Air quality data unavailable"}
            ), 500

    except ValueError:
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/weather-alerts/<latitude>/<longitude>", methods=["GET"])
def get_weather_alerts_for_location(latitude, longitude):
    """Get weather alerts/warnings for coordinates"""
    try:
        from src.stores.models import GeoLocation

        lat = float(latitude)
        lon = float(longitude)

        location = GeoLocation(
            latitude=lat,
            longitude=lon,
            address="",
            city=request.args.get("city", "Unknown"),
            state=request.args.get("state", "Unknown"),
            pincode="",
        )

        alerts = weather_service.get_weather_alerts(location)

        if alerts is not None:
            return jsonify({"success": True, "count": len(alerts), "alerts": alerts})
        else:
            return jsonify(
                {
                    "success": False,
                    "error": "Weather alerts unavailable (requires One Call API 3.0 subscription)",
                }
            ), 503

    except ValueError:
        return jsonify({"success": False, "error": "Invalid coordinates"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/location-with-weather", methods=["GET"])
def get_location_with_weather():
    """
    Get location details WITH weather in one call

    Query params:
        query: City or address name
    """
    try:
        query = request.args.get("query")

        if not query:
            return jsonify(
                {"success": False, "error": "Missing 'query' parameter"}
            ), 400

        result = location_service.get_location_with_weather(query)

        if result:
            return jsonify({"success": True, "data": result})
        else:
            return jsonify({"success": False, "error": "Location not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@stores_bp.route("/capabilities", methods=["GET"])
def get_service_capabilities():
    """Get information about available API capabilities"""
    try:
        caps = location_service.get_capabilities()
        return jsonify({"success": True, "capabilities": caps})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
