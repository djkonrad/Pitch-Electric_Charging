import json
import ssl
import pprint
import urllib.request
import reverse_geocoder as rg
from urllib.parse import urlencode
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    return result

coords = []
places_stopped = []

#parameters
dir_endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyASU7ZbDGGc70Ak7_cAWl1-Ox3UnvYA0Ms'
starting_range = int(input("Enter EV range in KM -----> "))
origin = input("Enter Starting Point -----> ").replace(' ','+')
destination = input("Enter Ending Point -----> ").replace(' ','+')

#formatting the url
dir_params = {"origin": origin, "destination": destination, "key": api_key}
dir_url_params = urlencode(dir_params)
dir_url = f"{dir_endpoint}{dir_url_params}"
#print(dir_url)

#send a resquest to Google Maps
dir_response = urllib.request.urlopen(dir_url).read()

# use the response data
directions = json.loads(dir_response)
routes = directions['routes']
legs = routes[0]['legs']

# steps[] is a list of every turn the navigation makes to get from origin to destination
steps = legs[0]['steps']

#keep track of battery range as we go
current_range = starting_range #kilometers
current_range *= 1000 #multiply by 1000 to convert to meters
current_step = 0 #meters

num_stops = 0 # keep track of number of stops
total_distance = 0 #keep track of total distance in meters

for i in range(len(steps)):
    current_step = steps[i]['distance']['value']
    if current_step >= current_range:
        num_stops += 1 #need to make a stop to charge battery
        current_range = starting_range*1000
        coords.append((steps[i]['start_location']['lat'],steps[i]['start_location']['lng']))

    #else
    current_range -= current_step
    total_distance += current_step

#converts lats and langs to city/town names
for i in range(num_stops):
    places_stopped.append(reverseGeocode(coords[i]))

#prints trip data along with locations stopped
print("Total Distance: " + str(total_distance/1000) + " km") #divide by 1000 to output result in km
print("Remaining Battery Range: " + str(current_range/1000) + " km") ##divide by 1000 to output result in km
print("Total Stops: " + str(num_stops))
print("Locations Stopped: ")
pprint.pprint(places_stopped)