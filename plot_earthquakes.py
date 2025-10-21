import requests
import json
from datetime import date
from collections import Counter
import statistics
import matplotlib.pyplot as plt


#retreive data from file that was saved in pervious exercise
def get_data():
    with open('earthquake.json', 'r') as f:
        earthquake_data = json.load(f)
    return earthquake_data

#function to retreive the year that an earthquake happened
def get_year(earthquake_data):
    timestamp = earthquake_data['properties']['time']
    #time is represented in milliseconds since the Unix epoch - therefore dividing by 1000 would convert to seconds
    year = date.fromtimestamp(timestamp/1000).year
    return year

#function to retreive the magnitude of an earthquake
def get_magnitude(earthquake_data):
    return earthquake_data["properties"]["mag"]

#function to find the frequencies of earthquakes per year
def get_frequency_per_year(earthquake_data):
    year = [get_year(y) for y in earthquake_data["features"]]
    f=Counter(year)
    return f

#function to find the average magnitude of earthquakes per year
def get_magnitude_per_year(earthquake_data):
    mags_by_year = {}
    for f in earthquake_data['features']:
        y = get_year(f)
        m = get_magnitude(f)
        mags_by_year.setdefault(y, []).append(m)
    avg_mag_per_year = {y: statistics.mean(ms) for y, ms in mags_by_year.items()}
    return avg_mag_per_year

#function to plot the year vs frequency of earthquake occurences
def plot_mag_per_year(earthquake_data):
    fig, ax = plt.subplots(figsize=(6,4))

    x = get_frequency_per_year(earthquake_data).keys()
    y1 = get_frequency_per_year(earthquake_data).values()
    y2 = get_magnitude_per_year(earthquake_data).values()

    ax.plot(x,y1,color = 'red', label = 'Frequency')
    ax.set_xlabel('Year')
    ax.set_ylabel('Frequency')

    ax2 = ax.twinx()
    ax2.plot(x,y2,color = 'green', label = 'Average Magnitude')
    ax2.set_ylabel('Average Magnitude')

    ax.legend(loc='lower right')
    ax2.legend(loc='upper right')

    plt.title('Average Magnitude and Frequency of Earthquakes per Year')
    
    return plt.show()


data = get_data()
print(get_frequency_per_year(data))
print(get_magnitude_per_year(data))

plot_mag_per_year(data)

    
    

