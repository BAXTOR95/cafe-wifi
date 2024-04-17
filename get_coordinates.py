import requests
from bs4 import BeautifulSoup


def get_coordinates(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the meta tag that contains the location coordinates
    meta_tag = soup.find('meta', attrs={'property': 'og:image'})
    if meta_tag and 'center' in meta_tag['content']:
        # Extract the content and split by slashes to find the part with coordinates
        parts = meta_tag['content'].split('/')
        for part in parts:
            if 'center' in part:
                coordinates = part.split('=')[1]
                return tuple(coordinates.split('%2C'))
    return None


url = 'https://goo.gl/maps/D7o4qtj6UzzhVgsk6'
coords = get_coordinates(url)
if coords:
    print(f"Latitude: {coords[0]}, Longitude: {coords[1]}")
else:
    print("Coordinates not found in the URL.")
