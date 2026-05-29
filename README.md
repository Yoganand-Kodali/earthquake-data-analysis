# Earthquake Data Analysis

An interactive Python application for acquiring, filtering, and visualizing global seismic activity from 1965 to 2016. Built using only Python's standard library and matplotlib — no pandas or heavy data science frameworks.

---

## What It Does

- Loads **23,406 earthquake records** and **44,554 world city records** from CSV files
- Provides an interactive CLI to filter seismic data by tremor type, date range, magnitude, latitude, and longitude
- Uses the **Haversine formula** to compute real geodesic distances between coordinates
- Generates **3 matplotlib visualizations** from the filtered dataset

---

## Project Structure

```
earthquake-data-analysis/
├── earthquake_analysis.py   # Main application
├── earthquakes.csv          # Seismic event records (23,406 rows)
├── world_cities.csv         # Global city data (44,554 rows)
├── requirements.txt
└── README.md
```

---

## Key Functions

| Function | Description |
|----------|-------------|
| `getCityData()` | Reads world cities CSV → returns `{(lat, lng): city_dict}` |
| `getQuakeData()` | Reads earthquake CSV → returns `{(lat, lng): quake_dict}` with proper datetime parsing |
| `haveDist(loc1, loc2)` | Haversine distance between two coordinates in km |
| `findCities(target, cities, radius)` | Finds all cities within N km of a target location |
| `filter_data(raw_data)` | Runs the full interactive CLI filtering pipeline |
| `fdates()` | Filters by date range with input validation |
| `fmagnitude()` | Filters by magnitude range with input validation |
| `latitude()` | Filters by latitude range with input validation |
| `longitude()` | Filters by longitude range with input validation |

---

## Visualizations

After filtering, the program generates 3 plots:

**1. Geographic Scatter Plot**
Earthquake locations plotted by lat/lng, color-coded by magnitude using the viridis colormap.

**2. Events Per Year Bar Chart**
Number of seismic events aggregated by year across the selected date range.

**3. Average Magnitude Per Year**
Scatter plot showing how average earthquake magnitude changed year over year.

---

## Sample CLI Interaction

```
*** Earthquake Data Analysis ***

Acquired data 44554 cities.
Acquired data 23406 earthquakes.
Skip selection? n

SELECT tremor type:
Enter choices separated by commas
Choices are ...
Earthquake, Explosion, Nuclear Explosion, Rock Burst
Enter values: Nuclear Explosion
Accepted ...
['Nuclear Explosion']
Selected 175 records.

SELECT date mm/dd/yyyy : enter two values separated by comma
range is 12/20/1966 through 06/08/1996
Enter minimum/maximum date values:
Accepted ...
Selected 175 records.

SELECT magnitude : enter two values separated by comma
range is 5.5 through 6.9
Enter minimum/maximum magnitude values:
Accepted ...
Selected 175 records.
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3 |
| Data Parsing | `csv`, `datetime` |
| Geospatial Math | `math` (Haversine formula) |
| Visualization | `matplotlib.pyplot` |
| Aggregation | `collections.defaultdict` |

---

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/yoganand97/earthquake-data-analysis.git
cd earthquake-data-analysis

# Install dependencies
pip install -r requirements.txt

# Run the application
python earthquake_analysis.py
```

> The CSV data files must be in the same directory as the script.

---

## Data

| File | Records | Columns |
|------|---------|---------|
| `earthquakes.csv` | 23,406 | Date, Time, Latitude, Longitude, Type, Depth, Magnitude, Magnitude Type |
| `world_cities.csv` | 44,554 | city, lat, lng, country, iso3, pop |

Earthquake data spans **January 1965 – December 2016**.
Seismic types include: Earthquake, Explosion, Nuclear Explosion, Rock Burst.
