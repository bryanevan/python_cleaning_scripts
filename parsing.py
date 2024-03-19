import sys

sys.path.append("/opt/anaconda3/lib/python3.11/site-packages")
import pandas as pd
import re

# Define your patterns outside the functions for global use
zip_code_pattern = r"\b\d{5}(?:-\d{4})?\b"
state_pattern = r"\b(?:California|Nevada|New York|CA|NV|AZ|NY|TX|FL)\b"


def load_city_names(file_path):
    city_names_set = set()
    with open(file_path, "r") as file:
        for line in file:
            city_names_set.add(line.strip())
    return city_names_set


def parse_address_components(address, city_names_set):
    if pd.isna(address):
        return pd.Series(
            [None, None, None, None],
            index=["house_street", "city", "state", "zip_code"],
        )

    # Regular expressions to extract ZIP code and state
    zip_code_match = re.search(zip_code_pattern, address)
    state_match = re.search(state_pattern, address)

    zip_code = zip_code_match.group(0) if zip_code_match else None
    state = state_match.group(0) if state_match else None

    found_city = None
    for city_name in city_names_set:
        if city_name in address:
            found_city = city_name
            break

    house_street = (
        address.split(found_city)[0].strip().replace(",", "") if found_city else None
    )

    return pd.Series(
        [house_street, found_city, state, zip_code],
        index=["house_street", "city", "state", "zip_code"],
    )


def export_dataframe(df, output_file_path):
    df.to_csv(output_file_path, index=False)


# Usage example
city_names_path = "/Users/bryanevan/CF/ANACONDA/place-city.ndjson"
city_names_set = load_city_names(city_names_path)

data = pd.read_csv("/Users/bryanevan/Downloads/raw.csv")

# Assuming lambda is necessary for DataFrame.apply()
data[["house_street", "city", "state", "zip_code"]] = data["principal_address"].apply(
    lambda x: parse_address_components(x, city_names_set)
)

output_path = "/Users/bryanevan/Downloads/cleaned.csv"
export_dataframe(data, output_path)
