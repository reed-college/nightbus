import os
import googlemaps

def calculate_duration(origin, destinations):
    
    key = "AIzaSyDK9cnUO7ivzLXGMxizbxt5y-sng3IjTIo"
#    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=key)

    ask_google = gmaps.distance_matrix(origin, destinations)

    filter_google_response = ask_google['rows'][0]['elements']

    duration = 0
    for address in filter_google_response:
        duration = duration + address['duration']['value']

    return (duration // 60)

