import requests
import csv
import time

#-----------------------------------------------------------------
# SBA API
#-----------------------------------------------------------------
url = "https://lending.sba.gov/api/disasters/v1/declarations/"



#-------------------------------------------------------------------
# Get data
#-------------------------------------------------------------------
response = requests.get(url)

print("SBA API status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Total disasters:", len(data))


# Store all rows
rows = []

#-----------------------------------------------------------------
# Start timer
#-----------------------------------------------------------------
start_time = time.time()

#-----------------------------------------------------------------
# Go through every disaster
#-----------------------------------------------------------------
for number, disaster in enumerate(data, start=1):

    if number % 25 == 0:
        print("Processing", number, "of", len(data))

#-----------------------------------------------------------------
# Disaster information
#-----------------------------------------------------------------
    disaster_number = disaster["disaster_number"]

    state = disaster["primary_disaster_state"]

    description = disaster["disaster_description"]

    incident_start_date = disaster["incident_start_date"]

    incident_end_date = disaster["incident_end_date"]

    declaration_date = disaster["declaration_date"]

    declaration_type = disaster["declaration_type_display"]

    status = disaster["disaster_status_display"]

    physical_deadline = disaster["physical_deadline_date"]

    eidl_deadline = disaster["eidl_deadline_date"]

    fema_number = disaster["fema_number"]


#-----------------------------------------------------------------
# PRIMARY COUNTIES
#-----------------------------------------------------------------

    for county in disaster["primary_counties"]:

        row = {
            "disaster_number": disaster_number,
            "state": county["state"],
            "disaster_description": description,
            "incident_start_date": incident_start_date,
            "incident_end_date": incident_end_date,
            "declaration_date": declaration_date,
            "declaration_type": declaration_type,
            "status": status,
            "physical_deadline_date": physical_deadline,
            "eidl_deadline_date": eidl_deadline,
            "fema_number": fema_number,
            "county_type": "Primary",
            "county_name": county["county_name"],
            "county_fips": county["fips_code_6"],
            "latitude": county.get("latitude", ""),
            "longitude": county.get("longitude", "")
        }

        rows.append(row)


#-----------------------------------------------------------------
# CONTIGUOUS COUNTIES
#-----------------------------------------------------------------

    for county in disaster["contiguous_counties"]:

        row = {
            "disaster_number": disaster_number,
            "state": county["state"],
            "disaster_description": description,
            "incident_start_date": incident_start_date,
            "incident_end_date": incident_end_date,
            "declaration_date": declaration_date,
            "declaration_type": declaration_type,
            "status": status,
            "physical_deadline_date": physical_deadline,
            "eidl_deadline_date": eidl_deadline,
            "fema_number": fema_number,
            "county_type": "Contiguous",
            "county_name": county["county_name"],
            "county_fips": county["fips_code_6"],
            "latitude": county.get("latitude", ""),
            "longitude": county.get("longitude", "")
        }

        rows.append(row)

#-----------------------------------------------------------------
# Main disaster loop ends 
#-----------------------------------------------------------------

end_time = time.time()

print("Loop time:", end_time - start_time, "seconds")



#-----------------------------------------------------------------
# CHECK FOR DISASTERS WITH NO ROWS
#-----------------------------------------------------------------

disasters_with_counties = set()

for row in rows:
    disasters_with_counties.add(
        row["disaster_number"]
    )


all_disasters = set()

for disaster in data:
    all_disasters.add(
        disaster["disaster_number"]
    )


missing_disasters = (
    all_disasters - disasters_with_counties
)

print("\nDisasters with no county rows:")
print(missing_disasters)

#-----------------------------------------------------------------
# CSV columns
#-----------------------------------------------------------------
column_names = [
    "disaster_number",
    "state",
    "disaster_description",
    "incident_start_date",
    "incident_end_date",
    "declaration_date",
    "declaration_type",
    "status",
    "physical_deadline_date",
    "eidl_deadline_date",
    "fema_number",
    "county_type",
    "county_name",
    "county_fips",
    "latitude",
    "longitude"
]

#-----------------------------------------------------------------
# Save CSV
#-----------------------------------------------------------------
with open(
    r"Data/sba_disaster_data.csv",
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=column_names
    )

    writer.writeheader()

    writer.writerows(rows)


print(
    "CSV file 'Data/sba_disaster_data.csv' has been created."
)

print(
    "Total rows written:",
    len(rows)
)