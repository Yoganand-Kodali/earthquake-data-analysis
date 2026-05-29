'''
Program     : Earthquake Data Analysis
Filename    : earthquake_analysis.py
Author      : Yoganand Kodali
Description :
    An interactive Python application for acquiring, filtering,
    and visualizing global earthquake data (1965–2016).

    Features:
    - Loads 23,406 earthquake records and 44,554 world city records from CSV
    - Interactive CLI to filter by tremor type, date range, magnitude,
      latitude, and longitude
    - Haversine distance calculation to find cities near earthquake epicenters
    - 3 matplotlib visualizations:
        1. Scatter plot: earthquake locations with magnitude color-mapping
        2. Bar chart: number of seismic events per year
        3. Scatter plot: average magnitude per year

    Data files required:
        earthquakes.csv   — seismic event records
        world_cities.csv   — global city coordinates and populations
'''

import matplotlib.pyplot as plt
import csv
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from collections import defaultdict


# ─────────────────────────────────────────────
# Load World City Data
# ─────────────────────────────────────────────

def getCityData():
    '''
    Reads city data from world_cities.csv and returns a dictionary
    keyed by (latitude, longitude) tuples.

    Returns:
        dict: { (lat, lng): { city, country, iso3, pop } }
    '''
    with open('world_cities.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = [i for i in reader]

    cityData = {}
    badRecords = []

    for i in data:
        i['lat'] = float(i['lat'])
        i['lng'] = float(i['lng'])
        try:
            i['pop'] = int(i['pop'])
        except ValueError:
            badRecords.append(i)
            i['pop'] = 0
        cityData[(i.pop('lat'), i.pop('lng'))] = i

    return cityData


cityDict = getCityData()


# ─────────────────────────────────────────────
# HAVERSINE DISTANCE CALCULATION
# ─────────────────────────────────────────────

def coord2rad(location):
    '''Converts (lat, lng) tuple in degrees to radians dictionary.'''
    return {'lat': radians(location[0]), 'long': radians(location[1])}


def haveDist(loc1, loc2, units='km'):
    '''
    Calculates the great-circle distance between two geographic coordinates
    using the Haversine formula.

    Args:
        loc1 (tuple): (latitude, longitude) in degrees
        loc2 (tuple): (latitude, longitude) in degrees
        units (str):  'km' for kilometers (default), otherwise miles

    Returns:
        float: Distance between the two locations
    '''
    loc1 = coord2rad(loc1)
    loc2 = coord2rad(loc2)

    dlon = loc2['long'] - loc1['long']
    dlat = loc2['lat'] - loc1['lat']

    a = sin(dlat / 2)**2 + cos(loc1['lat']) * cos(loc2['lat']) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 if units == 'km' else 3956

    return c * r


# ─────────────────────────────────────────────
# Find Nearby Cities
# ─────────────────────────────────────────────

def findCities(target_location, cities, radius):
    '''
    Returns a list of cities within a given radius of a target location.

    Args:
        target_location (tuple): (lat, lng) of the target
        cities (dict):           city dictionary from getCityData()
        radius (float):          search radius in km

    Returns:
        list of dicts: [ { city, country, pop, distance } ]
    '''
    closeCities = []
    for k, v in cityDict.items():
        distance = round(haveDist(target_location, k), 1)
        if distance < radius:
            closeCities.append({
                'city': v['city'],
                'country': v['country'],
                'pop': v['pop'],
                'distance': distance
            })
    return closeCities


# ─────────────────────────────────────────────
# Load Earthquake Data
# ─────────────────────────────────────────────

def getQuakeData():
    '''
    Reads earthquake data from earthquakes.csv and returns a dictionary
    keyed by (latitude, longitude) tuples.

    Returns:
        dict: { (lat, lng): { Type, Depth, Magnitude, 'Magnitude Type', datetime } }
    '''
    with open('earthquakes.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = [i for i in reader]

    qDict = {}
    for i in data:
        i['Latitude'] = float(i['Latitude'])
        i['Longitude'] = float(i['Longitude'])
        i['Magnitude'] = float(i['Magnitude'])

        a = i['Date'] + ' ' + i['Time']
        try:
            i['datetime'] = datetime.strptime(a, '%m/%d/%Y %H:%M:%S')
        except ValueError:
            i['datetime'] = datetime.fromisoformat(i['Date']).replace(tzinfo=None)
            i['datetime'] = datetime.strftime(i['datetime'], '%m/%d/%Y %H:%M:%S')
            i['datetime'] = datetime.strptime(i['datetime'], '%m/%d/%Y %H:%M:%S')

        i.pop('Date')
        i.pop('Time')
        qDict[(i.pop('Latitude'), i.pop('Longitude'))] = i

    return qDict


qDict = getQuakeData()


# ─────────────────────────────────────────────
# Interactive Filtering UI
# ─────────────────────────────────────────────

def latitude(input_data):
    '''Filters earthquake records by latitude range via user input.'''
    lat = [k[0] for (k, v) in list(input_data.items())]
    print(f'\nSELECT latitude : enter two values separated by comma\nrange is {min(lat)} through {max(lat)}')

    while True:
        lat_input = input('Enter minimum/maximum latitude values: ')
        if not lat_input:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [min(lat), max(lat)])))
            break
        lat_input = [float(i) for i in lat_input.split(',')]
        lat_input.sort()
        if float(lat_input[0]) <= min(lat) or float(lat_input[1]) >= max(lat):
            print(f'One or more values out-of-range: <({float(lat_input[0])}, {float(lat_input[1])})>')
        else:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [float(i) for i in lat_input])))
            break

    selected_data = {}
    for (k, v) in list(input_data.items()):
        if lat_input:
            if float(lat_input[0]) <= k[0] <= float(lat_input[1]):
                selected_data[k] = v
        else:
            selected_data = input_data

    print(f'Selected {len(list(selected_data.items()))} records.')
    return selected_data


def longitude(input_data):
    '''Filters earthquake records by longitude range via user input.'''
    lng = [k[1] for (k, v) in list(input_data.items())]
    print(f'\nSELECT longitude : enter two values separated by comma\nrange is {min(lng)} through {max(lng)}')

    while True:
        lng_input = input('Enter minimum/maximum longitude values: ')
        if not lng_input:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [min(lng), max(lng)])))
            break
        lng_input = [float(i) for i in lng_input.split(',')]
        lng_input.sort()
        if float(lng_input[0]) <= min(lng) or float(lng_input[1]) >= max(lng):
            print(f'One or more values out-of-range: <({float(lng_input[0])}, {float(lng_input[1])})>')
        else:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [float(lng_input[0]), float(lng_input[1])])))
            break

    selected_data = {}
    for (k, v) in list(input_data.items()):
        if lng_input:
            if float(lng_input[0]) <= k[1] <= float(lng_input[1]):
                selected_data[k] = v
        else:
            selected_data = input_data

    print(f'Selected {len(list(selected_data.items()))} records.')
    return selected_data


def fdates(input_data):
    '''Filters earthquake records by date range via user input.'''
    dates = [datetime.strftime(v['datetime'], '%m/%d/%Y') for (k, v) in list(input_data.items())]
    dates.sort(key=lambda date: datetime.strptime(date, '%m/%d/%Y'))
    print(f'\nSELECT date mm/dd/yyyy : enter two values separated by comma\nrange is {dates[0]} through {dates[-1]}')

    while True:
        dt_input = input('Enter minimum/maximum date values: ')
        if not dt_input:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [dates[0], dates[-1]])))
            break
        dt_input = sorted([datetime.strptime(i, '%m/%d/%Y') for i in dt_input.split(',')])
        if dt_input[0] <= datetime.strptime(dates[0], '%m/%d/%Y') or dt_input[1] >= datetime.strptime(dates[-1], '%m/%d/%Y'):
            print(f'One or more values out-of-range: <({dt_input[0]}, {dt_input[1]})>')
        else:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [datetime.strftime(i, '%m/%d/%Y') for i in dt_input])))
            break

    selected_data = {}
    for (k, v) in list(input_data.items()):
        if dt_input:
            if dt_input[0].date() <= v['datetime'].replace(tzinfo=None).date() <= dt_input[1].date():
                selected_data[k] = v
        else:
            selected_data = input_data

    print(f'Selected {len(list(selected_data.items()))} records.')
    return selected_data


def fmagnitude(input_data):
    '''Filters earthquake records by magnitude range via user input.'''
    magnitude = [v['Magnitude'] for (k, v) in list(input_data.items())]
    print(f'\nSELECT magnitude : enter two values separated by comma\nrange is {min(magnitude)} through {max(magnitude)}')

    while True:
        mag_input = input('Enter minimum/maximum magnitude values: ')
        if not mag_input:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [min(magnitude), max(magnitude)])))
            break
        mag_input = [float(i) for i in mag_input.split(',')]
        mag_input.sort()
        if float(mag_input[0]) <= min(magnitude) or float(mag_input[1]) >= max(magnitude):
            print(f'One or more values out-of-range: <({float(mag_input[0])}, {float(mag_input[1])})>')
        else:
            print('Accepted ...')
            print(dict(zip(['min', 'max'], [float(mag_input[0]), float(mag_input[1])])))
            break

    selected_data = {}
    for (k, v) in list(input_data.items()):
        if mag_input:
            if float(mag_input[0]) <= v['Magnitude'] <= float(mag_input[1]):
                selected_data[k] = v
        else:
            selected_data = input_data

    print(f'Selected {len(list(selected_data.items()))} records.')
    return selected_data


def filter_data(raw_data):
    '''
    Runs the full interactive filtering pipeline in sequence:
    date → magnitude → latitude → longitude

    Args:
        raw_data (dict): Full earthquake dictionary

    Returns:
        dict: Filtered earthquake records
    '''
    selected_data = raw_data

    while True:
        selected = fdates(selected_data)
        if input('\nWant to move on to the next item? ') not in ['n', 'no']:
            break
    selected_data = selected

    while True:
        selected = fmagnitude(selected_data)
        if input('\nWant to move on to the next item? ') not in ['n', 'no']:
            break
    selected_data = selected

    while True:
        selected = latitude(selected_data)
        if input('\nWant to move on to the next item? ') not in ['n', 'no']:
            break
    selected_data = selected

    while True:
        selected = longitude(selected_data)
        if input('\nWant to move on to analysis? ') not in ['n', 'no']:
            break

    return selected


# ─────────────────────────────────────────────
# MAIN — Run Interactive Analysis
# ─────────────────────────────────────────────

if __name__ == '__main__':

    print('\n*** Earthquake Data Analysis ***')
    print(f'\nAcquired data {len(cityDict.items())} cities.')
    print(f'Acquired data {len(qDict.items())} earthquakes.')

    # Tremor type selection
    tremors = sorted(list(set([v['Type'] for (k, v) in list(qDict.items())])))
    n = input('Skip selection? ')

    if n in ['n', 'no']:
        print(f'SELECT tremor type:\nEnter choices separated by commas\nChoices are ...\n{", ".join(tremors)}')
        tremors_input = input('Enter values: ').split(',')
        tremors_list = [i for i in tremors for j in tremors_input if i[:3] == j[:3]]
        print('Accepted ...')
        print(tremors_list)

        for (k, v) in list(qDict.items()):
            if v['Type'] in tremors_list:
                qDict[k] = v
            else:
                qDict.pop(k)

        print(f'Selected {len(list(qDict.items()))} records.')
    else:
        tremors_list = tremors
        print('Accepted ...')
        print(tremors_list)

    ui5 = input('\nWant to move on to the next item? ')

    if ui5 not in ['n', 'no']:
        selected_data = list(filter_data(qDict).items())
        print(f'\nANALYZED {len(selected_data)} earthquake records:')
        print('(see plots for results)')

    # ─── Prepare plot data ───
    selected_data.sort(key=lambda x: x[1]['Magnitude'])

    lats = [lat for (lat, lng), _ in selected_data]
    lngs = [lng for (lat, lng), _ in selected_data]
    mags = [v['Magnitude'] for _, v in selected_data]

    event_year = defaultdict(lambda: {'events': [], 'magnitudes': []})
    for (k, v) in selected_data:
        year = v['datetime'].year
        event_year[year]['events'].append(v)
        event_year[year]['magnitudes'].append(v['Magnitude'])
    event_year = dict(sorted(event_year.items()))

    title_dates = [datetime.strftime(v['datetime'], '%m/%d/%Y') for (k, v) in selected_data]
    title_dates.sort(key=lambda date: datetime.strptime(date, '%m/%d/%Y'))
    title = f'{title_dates[0]} to {title_dates[-1]}'
    suptitle = ' / '.join(tremors_list)

    # ─── Plot 1: Location scatter ───
    plt.figure(figsize=(12, 7))
    plt.scatter(lngs, lats, s=5, c=mags, cmap='viridis')
    plt.colorbar(label='magnitude', orientation='horizontal', shrink=0.65)
    plt.xlabel('Longitude in degrees')
    plt.ylabel('Latitude in degrees')
    plt.title(title)
    plt.suptitle(suptitle)
    plt.show()

    # ─── Plot 2: Events per year bar chart ───
    plt.figure(figsize=(12, 7))
    plt.bar(list(event_year.keys()), [len(data['events']) for data in event_year.values()])
    plt.xlabel('Year')
    plt.ylabel('Number of Events')
    plt.title(title)
    plt.suptitle(suptitle)
    plt.show()

    # ─── Plot 3: Average magnitude per year ───
    plt.figure(figsize=(12, 7))
    plt.scatter(
        list(event_year.keys()),
        [sum(v['magnitudes']) / len(v['magnitudes']) for (k, v) in event_year.items()]
    )
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.title(title)
    plt.suptitle(suptitle)
    plt.show()
