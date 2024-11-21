import geopandas as gpd
from shapely.geometry import Point

# Load the dataset
from geopandas.datasets import get_path

cities = gpd.read_file(get_path('naturalearth_cities'))

# Filter for European capitals (manually or with an additional dataset)
european_capitals = [
    "London", "Paris", "Berlin", "Rome", "Madrid", "Vienna", "Warsaw", "Athens"
    # Add more capital city names as required
]

european_cities = cities[cities['name'].isin(european_capitals)]

# Reproject to a metric CRS (EPSG:3035)
european_cities = european_cities.to_crs(epsg=3035)

# Compute pairwise distances
distances = european_cities.geometry.apply(
    lambda city: european_cities.distance(city)
)

# Convert distances to a DataFrame for readability
import pandas as pd
distance_df = pd.DataFrame(distances.values.tolist(),
                           index=european_cities['name'],
                           columns=european_cities['name'])
distance_df_km = distance_df / 1000
print(distance_df_km)
