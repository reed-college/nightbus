import local_config
import googlemaps

key = local_config.GOOGLE_MAPS_API_KEY
gmaps = googlemaps.Client(key=key)

def calculate_duration(origin, destinations):
    ask_google = gmaps.distance_matrix(origin, destinations)
    filter_google_response = ask_google['rows'][0]['elements']

    duration = 0
    for address in filter_google_response:
        duration = duration + address['duration']['value']

    return (duration // 60)

def geocode(address):
    results = gmaps.geocode({address: address})
    result = results[0]['geometry']['location']

    return result
