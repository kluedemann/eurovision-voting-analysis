"""Dataset Preprocessing Class"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.datasets import get_path


WB_COLS = [
    'GDP per capita (current US$)', 
    'Population, total'
]

RELIGION_COLS = [
    'chrstprotpct', 
    'chrstcatpct', 
    'chrstorthpct', 
    'judgenpct', 
    'islmgenpct', 
    'nonreligpct'
]



def load_data(world_bank_cols=WB_COLS, religion_cols=RELIGION_COLS):
    """Load the full dataset into a pandas DataFrame.

    Dataset is rows of Eurovision voting record with additional
    data about the countries giving and receiving the vote and
    the distance between the capital cities.

    Params:
        world_bank_cols - list of columns of world bank data to use

    Returns: pd.DataFrame
    """
    country_data = load_country_data()
    coordinates = load_coordinates(country_data['capital'])
    country_coords = country_data.merge(coordinates, left_on="capital", right_on="city")

    gdp_data = load_world_bank_data(world_bank_cols)
    europe_gdp_data = country_coords.merge(gdp_data, left_on="iso-alpha-3", right_on="Country Code")


def load_religion_data(columns=[]):
    """Load WRP National religious demographic data.
    Source: https://correlatesofwar.org/data-sets/world-religion-data/
    
    Params:
        columns - list of data columns to select
        
        
    Returns: pd.DataFrame

    """
    pass


def load_world_bank_data(columns=[]):
    """Load the world bank data for each country and year.
    Source:https://databank.worldbank.org/indicator/NY.GDP.PCAP.CD/1ff4a498/Popular-Indicators

    Params:
        columns - list of data columns to select

    Returns: pd.DataFrame
        Country Code - 3 letter COW code
        Year
        [columns]
    """
    gdp_raw = pd.read_csv("../data/World_Bank_Data.csv")

    gdp_data = gdp_raw.drop(["Country Name", "Series Code"], axis=1)
    gdp_data = gdp_data.iloc[:-5] # Remove metadata
    gdp_data = gdp_data.set_index(["Country Code","Series Name"])
    gdp_data = gdp_data.stack().unstack(1)

    gdp_data = gdp_data[columns].reset_index()
    gdp_data["Year"] = gdp_data["level_1"].str.split().str.get(0)
    gdp_data["Year"] = pd.to_numeric(gdp_data["Year"])
    gdp_data = gdp_data.drop(["Series Name","level_1"], axis=1)

    return gdp_data


def load_coordinates(capitals):
    """Load the coordinates for each European capital.
    Note: Uses EPSG:3035 projection. Fairly accurate within Europe
    Source: https://www.naturalearthdata.com/

    Params:
        capitals - the pd.Series of capital city names
        
    Returns: gpd.GeoDataFrame
        city - the capital city name
        geometry - the point object for the city
        x_coord - the EPSG:3035 projected x-coordinate
        y_coord - the EPSG:3035 projected y-coordinate
    """
    # Filter for European capitals (manually or with an additional dataset)
    cities = gpd.read_file(get_path('naturalearth_cities'))
    european_cities = cities[cities['name'].isin(capitals)]

    # Reproject to a metric CRS (EPSG:3035)
    european_cities = european_cities.to_crs(epsg=3035)
    european_cities['x_coord'] = european_cities["geometry"].x
    european_cities['y_coord'] = european_cities["geometry"].y
    european_cities = european_cities.rename(columns={"name":"city"})
    return european_cities


def load_country_data():
    """Load information about each Eurovision participant country.
    
    Returns: pd.DataFrame
        name - English country name
        capital - capital city
        iso-alpha-2 - ISO-3166-1 2 letter code
        iso-alpha-3 - ISO-3166-1 3 letter code
        StateAbb - 3 letter COW code
    """
    iso_codes = load_iso_codes()
    capitals = load_capitals()
    merged_countries = capitals.merge(iso_codes, left_on="code", right_on="iso-alpha-2")
    merged_countries = merged_countries.drop("code", axis=1)
    
    cow_codes = load_cow_codes()
    merged_countries = merged_countries.merge(cow_codes.drop_duplicates(), left_on="name", right_on="StateNme", how="left")
    merged_countries = merged_countries.drop(['CCode', 'StateNme'], axis=1)
    return merged_countries


def load_cow_codes():
    """Load Correlates of War (COW) codes for each country.
    
    Source: https://correlatesofwar.org/data-sets/cow-country-codes-2/

    Returns: pd.DataFrame
        StateAbb - 3 letter COW country abbreviation
            Note: Does not match ISO-3166-1
        CCode - numeric COW country code
        StateNme - country name (English)
    """
    cow_codes = pd.read_csv("../data/COW-country-codes.csv")
    return cow_codes


def load_capitals():
    """Load capitals of countries that participated in Eurovision.

    Sources: Manually combined
        https://eurovisionworld.com/eurovision/2023
        https://en.wikipedia.org/wiki/List_of_national_capitals

    Returns: pd.DataFrame
        name - country name (English)
        code - ISO-3166-1 alpha-2 country code
        capital - capital city
    """
    capitals = pd.read_csv("../data/country_info.csv")
    return capitals


def load_iso_codes():
    """Load the mapping between ISO-3166-1 country codes.

    Source: https://www.iso.org/obp/ui/#search (copy-paste)
    
    Returns: pd.DataFrame
        iso-alpha-2 - the ISO-3166-1 alpha-2 country code (2 letters)
        iso-alpha-3 - the ISO-3166-1 aplha-3 country code (3 letters)
    """
    codes_raw = pd.read_csv("../data/country_codes_raw.csv")
    codes = codes_raw.dropna()
    codes = codes[["iso-alpha-2", "iso-alpha-3"]]
    codes["iso-alpha-2"] = codes["iso-alpha-2"].str.lower()
    return codes
