import requests
import csv


# SBA API
url = "https://lending.sba.gov/api/disasters/v1/declarations/"

# Get data
response = requests.get(url)

data = response.json()

print("Total disasters:", len(data))


# Create a list to store rows
rows = []


# Go through every disaster
for disaster in data:

    disaster_number = disaster["disaster_number"]
    state = disaster["primary_disaster_state_display"]
    description = disaster["disaster_description"]
    declaration_date = disaster["declaration_date"]
    status = disaster["disaster_status_display"]

    # Go through every primary county
    for county in disaster["primary_counties"]:

        row = {
            "disaster_number": disaster_number,
            "state": state,
            "disaster_description": description,
            "declaration_date": declaration_date,
            "status": status,
            "county_name": county["county_name"],
            "county_fips": county["fips_code_6"],
            "latitude": county["latitude"],
            "longitude": county["longitude"]
        }

        rows.append(row)


# Save rows into CSV
with open(
    "sba_disaster_counties.csv",
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    column_names = [
        "disaster_number",
        "state",
        "disaster_description",
        "declaration_date",
        "status",
        "county_name",
        "county_fips",
        "latitude",
        "longitude"
    ]

    writer = csv.DictWriter(
        csv_file,
        fieldnames=column_names
    )

    # Write column names
    writer.writeheader()

    # Write all rows
    writer.writerows(rows)


print("CSV created successfully.")
print("Total county rows:", len(rows))

