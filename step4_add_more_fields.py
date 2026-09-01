import requests

import csv

# SBA API
url = "https://lending.sba.gov/api/disasters/v1/declarations/"  

# Get data
response = requests.get(url)

data = response.json()

print("Total disasters:", len(data))

## Create a list to store rows
rows = []   

## Go through every disaster
for disaster in data:

    disaster_number = disaster["disaster_number"]
    state = disaster["primary_disaster_state_display"]
    description = disaster["disaster_description"]

    incident_start_date = disaster["incident_start_date"]
    incident_end_date = disaster["incident_end_date"]

    declaration_date = disaster["declaration_date"]
    declaration_type = disaster["declaration_type_display"]
    status = disaster["disaster_status_display"]
    physical_deadline = disaster["physical_deadline_date"]
    eidl_deadline = disaster["eidl_deadline_date"]

    fema_number = disaster["fema_number"]

    # Go through every primary county
    for county in disaster["primary_counties"]:

        row = {
            "disaster_number": disaster_number,
            "state": state,
            "disaster_description": description,
            "incident_start_date": incident_start_date,
            "incident_end_date": incident_end_date,
            "declaration_date": declaration_date,
            "status": status,
            "county_name": county["county_name"],
            "county_fips": county["fips_code_6"],
            "latitude": county["latitude"],
            "longitude": county["longitude"],
            "declaration_type": declaration_type,
            "physical_deadline": physical_deadline,
            "eidl_deadline": eidl_deadline,
            "fema_number": fema_number,
        }

        rows.append(row)

## column_names for csv

column_names = [
    "disaster_number",  
    "state",
    "disaster_description",
    "incident_start_date",
    "incident_end_date",
    "declaration_date",
    "declaration_type",
    "status",
    "physical_deadline",
    "eidl_deadline",
    "fema_number",
    "county_name",
    "county_fips",
    "latitude",
    "longitude",
]


# Save rows into CSV
with open(
    "sba_disaster_counties.csv",
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=column_names
    )

    # Write column names
    writer.writeheader()

    # Write all rows
    writer.writerows(rows)

## Print the number of rows written to the CSV

print("Total rows written to CSV:", len(rows))
print("CSV created successfully.")
print("Total county rows:", len(rows))

