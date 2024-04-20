import os
import googlemaps
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


class GoogleMapsClient:
    def __init__(self, api_key=None):
        # Attempt to load the API key either from an argument or the environment variable
        self.ENV_PATH = Path("..", "..", ".env")
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.api_key = api_key if api_key is not None else os.getenv('MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("No API key provided or found in environment variables")

        # Initialize the Google Maps client with the API key
        self.client = googlemaps.Client(key=self.api_key)

    def geocode(self, address):
        """Geocode an address."""
        try:
            return self.client.geocode(address)
        except Exception as e:
            print(f"Error in geocoding: {e}")
            return None

    def reverse_geocode(self, latitude, longitude):
        """Reverse geocode a pair of latitude and longitude."""
        try:
            return self.client.reverse_geocode((latitude, longitude))
        except Exception as e:
            print(f"Error in reverse geocoding: {e}")
            return None

    def directions(
        self, start_location, end_location, mode='driving', departure_time=None
    ):
        """Get directions between two locations."""
        try:
            return self.client.directions(
                start_location,
                end_location,
                mode=mode,
                departure_time=departure_time or datetime.now(),
            )
        except Exception as e:
            print(f"Error getting directions: {e}")
            return None


# Example usage of the GoogleMapsClient class
if __name__ == "__main__":
    gmaps_client = GoogleMapsClient()

    # Using geocode method
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    geocode_result = gmaps_client.geocode(address)
    if geocode_result:
        print("Geocode result:", geocode_result)

    # # Using reverse geocode method
    # latitude, longitude = 40.714224, -73.961452
    # reverse_result = gmaps_client.reverse_geocode(latitude, longitude)
    # if reverse_result:
    #     print("Reverse geocode result:", reverse_result)

    # # Using directions method
    # start = "Sydney Town Hall"
    # end = "Parramatta, NSW"
    # directions_result = gmaps_client.directions(start, end, mode="transit")
    # if directions_result:
    #     print("Directions result:", directions_result)
