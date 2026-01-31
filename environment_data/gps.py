"""
GPS Location Module

This module handles GPS/geolocation logic using streamlit_js_eval.
"""

from typing import Optional, Dict


def get_gps_location() -> Optional[Dict[str, float]]:
    """
    Get user's GPS coordinates using streamlit_js_eval.
    
    This function safely extracts latitude and longitude from the geolocation
    result. It handles cases where:
    - User denies location permission
    - GPS data is unavailable
    - Location is null or malformed
    
    Returns:
        Optional[Dict[str, float]]: Dictionary with 'latitude' and 'longitude'
                                    Returns None if location unavailable
    """
    try:
        # Import streamlit_js_eval inside function to avoid import errors
        # when running outside Streamlit context
        from streamlit_js_eval import get_geolocation
        
        # Get geolocation from browser
        geo_data = get_geolocation()
        
        # Check if we got valid data
        if geo_data is None:
            print("Warning: GPS location is None (permission denied or unavailable)")
            return None
        
        # Extract latitude and longitude
        latitude = geo_data.get("coords", {}).get("latitude")
        longitude = geo_data.get("coords", {}).get("longitude")
        
        # Validate the coordinates
        if latitude is None or longitude is None:
            print("Warning: GPS coordinates are incomplete")
            return None
        
        # Ensure coordinates are within valid ranges
        if not (-90 <= latitude <= 90):
            print(f"Warning: Invalid latitude value: {latitude}")
            return None
        
        if not (-180 <= longitude <= 180):
            print(f"Warning: Invalid longitude value: {longitude}")
            return None
        
        return {
            "latitude": float(latitude),
            "longitude": float(longitude)
        }
        
    except ImportError:
        print("Error: streamlit_js_eval is not installed or not available")
        return None
    except Exception as e:
        print(f"Error getting GPS location: {str(e)}")
        return None

