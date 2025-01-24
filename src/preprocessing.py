"""Dataset Preprocessing Class"""

import pandas as pd

def load_data():
    """Load the full dataset into a pandas DataFrame.

    Dataset is rows of Eurovision voting record with additional
    data about the countries giving and receiving the vote and
    the distance between the capital cities.

    Returns: pd.DataFrame
    """
    country_data = load_country_data()


def load_country_data():
    
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
