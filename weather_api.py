"""
Weather API Service

Handles interactions with weather and location APIs using free services.
"""

import requests


class WeatherService:
    """Service class for weather and location data."""

    def __init__(self):
        # Using free APIs that don't require registration
        self.weather_base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.ip_location_url = "http://ip-api.com/json"
        self.zipcode_url = "https://api.zippopotam.us/us"

    def get_current_location(self):
        """Get current location based on IP address."""
        try:
            response = requests.get(self.ip_location_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    city = data.get("city")
                    state = data.get("regionName")
                    return (city, state)
        except Exception as e:
            print(f"Error getting current location: {e}")
        return None

    def get_location_by_zipcode(self, zipcode):
        """Get location information by zip code."""
        try:
            response = requests.get(f"{self.zipcode_url}/{zipcode}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                city = data.get("post code")  # This might be the place name
                places = data.get("places", [])
                if places:
                    city = places[0].get("place name")
                    state = places[0].get("state abbreviation")
                    return (city, state)
        except Exception as e:
            print(f"Error getting location by zipcode: {e}")
        return None

    def get_coordinates_by_zipcode(self, zipcode):
        """Get latitude and longitude by zip code."""
        try:
            response = requests.get(f"{self.zipcode_url}/{zipcode}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                places = data.get("places", [])
                if places:
                    lat = float(places[0].get("latitude"))
                    lon = float(places[0].get("longitude"))
                    return (lat, lon)
        except Exception as e:
            print(f"Error getting coordinates by zipcode: {e}")
        return None

    def get_current_coordinates(self):
        """Get current coordinates based on IP address."""
        try:
            response = requests.get(self.ip_location_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    lat = data.get("lat")
                    lon = data.get("lon")
                    return (lat, lon)
        except Exception as e:
            print(f"Error getting current coordinates: {e}")
        return None

    def get_weather_by_coordinates(self, lat, lon):
        """Get weather information by coordinates using Open-Meteo API."""
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,weather_code",
                "temperature_unit": "fahrenheit",
                "timezone": "auto",
            }

            response = requests.get(self.weather_base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current", {})
                temperature = current.get("temperature_2m")
                weather_code = current.get("weather_code")

                # Convert weather code to readable condition
                condition = self.weather_code_to_condition(weather_code)

                return (int(temperature), condition)
        except Exception as e:
            print(f"Error getting weather by coordinates: {e}")
        return None

    def get_weather_by_zipcode(self, zipcode):
        """Get weather information by zip code."""
        coordinates = self.get_coordinates_by_zipcode(zipcode)
        if coordinates:
            lat, lon = coordinates
            return self.get_weather_by_coordinates(lat, lon)
        return None

    def get_current_weather(self):
        """Get weather information for current location."""
        coordinates = self.get_current_coordinates()
        if coordinates:
            lat, lon = coordinates
            return self.get_weather_by_coordinates(lat, lon)
        return None

    def weather_code_to_condition(self, code):
        """Convert Open-Meteo weather code to readable condition."""
        weather_codes = {
            0: "clear sky",
            1: "mainly clear",
            2: "partly cloudy",
            3: "overcast",
            45: "fog",
            48: "depositing rime fog",
            51: "light drizzle",
            53: "moderate drizzle",
            55: "dense drizzle",
            56: "light freezing drizzle",
            57: "dense freezing drizzle",
            61: "slight rain",
            63: "moderate rain",
            65: "heavy rain",
            66: "light freezing rain",
            67: "heavy freezing rain",
            71: "slight snow fall",
            73: "moderate snow fall",
            75: "heavy snow fall",
            77: "snow grains",
            80: "slight rain showers",
            81: "moderate rain showers",
            82: "violent rain showers",
            85: "slight snow showers",
            86: "heavy snow showers",
            95: "thunderstorm",
            96: "thunderstorm with slight hail",
            99: "thunderstorm with heavy hail",
        }
        return weather_codes.get(code, "unknown conditions")
