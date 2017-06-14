import googlemaps

key = "AIzaSyD99n_ZeIWtWv3oMH7heZGAfWJM6uVQBLQ"

gmaps = googlemaps.Client(key=key)

origin = "Reed College"
waypoints = ["7900 NE 33rd Dr.,Portland, OR", "Bagdhad Theatre", "Moreland Theatre", "Salem, OR"]
destination = "5418 SE Mitchel St., Portland, OR"

response = gmaps.distance_matrix(origin, waypoints)

filtered_response = response['rows'][0]['elements']

duration = 0
for element in filtered_response:
    duration += element['duration']['value']

# Change the unit to minutes
duration = duration//60
print(duration)
print()
print(response['rows'][0]['elements'][0]['duration']['text'])
