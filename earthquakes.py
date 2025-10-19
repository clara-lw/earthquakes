# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    data = json.loads(text)
    with open('earthquake.json', 'w') as f:
         json.dump(data, f, indent=4)

    with open('earthquake.json', 'r') as f:
        loaded_data = json.load(f)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return loaded_data

def count_earthquakes(loaded_data):
    """Get the total number of earthquakes in the response."""
    return len(loaded_data["features"])


def get_magnitude(loaded_data):
    """Retrive the magnitude of an earthquake item."""
    return loaded_data["properties"]["mag"]


def get_location(loaded_data):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = loaded_data["geometry"]["coordinates"]
    latitude = coordinates[0]
    longitude = coordinates[1]
    return (latitude,longitude)


def get_maximum(loaded_data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    mag = [get_magnitude(x) for x in loaded_data["features"]]
    max_mag = max(mag)
    print(max_mag)
    for y in loaded_data["features"]:
         if get_magnitude(y) == max_mag:
             max_location = get_location(y)
             break
    return max_mag, max_location
    


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")