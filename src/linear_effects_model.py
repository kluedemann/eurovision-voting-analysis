import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import csv

# Load the data
votes = pd.read_csv("data/votes.csv")
distances = pd.read_csv("data/distances.csv")

# read csv file to a list of dictionaries
with open("data/country_info.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    country_info = [row for row in csv_reader]


print(votes.head())
print(distances.head())
print(country_info)

# Helper functions


def get_country_capital(code_to_find, countries):
    return next(
        (
            country["capital"]
            for country in countries
            if country["code"] == code_to_find
        ),
        None,
    )


import pandas as pd
import csv


def transform_distances_to_codes(distances, country_info_file):
    """
    Transforms a distances CSV with capitals as labels to one with country codes as labels.

    Args:
        distances_file (str): Path to the CSV file with distances (capitals as labels).
        country_info_file (str): Path to the CSV file mapping capitals to country codes.
        output_file (str, optional): Path to save the transformed CSV. If None, it won't save.

    Returns:
        pd.DataFrame: Transformed DataFrame with country codes as labels.
    """
    # Load the distances and country info

    # Read country info into a dictionary for quick lookups
    with open(country_info_file, "r") as file:
        csv_reader = csv.DictReader(file)
        capital_to_code = {row["capital"]: row["code"] for row in csv_reader}

    distances.rename(
        columns=lambda col: capital_to_code.get(
            col, col
        ),  # Replace capital with code in columns
        inplace=True,
    )

    distances["name"] = distances["name"].apply(lambda x: capital_to_code.get(x, x))

    return distances


# Transform distances
transformed_distances = transform_distances_to_codes(distances, "data/country_info.csv")

print(transformed_distances.head())

## data preparation/ exploration


## Linear Effects Model
print(votes.head())
smf.mixedlm(
    formula="total_votes ~ distance + year", data=votes, groups=votes["from_country_id"]
).fit().summary()

# Check the assumptions of the linear effects model
