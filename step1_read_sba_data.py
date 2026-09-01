import requests


# --------------------------------
# SBA API address
# --------------------------------

url = "https://lending.sba.gov/api/disasters/v1/declarations/"


# --------------------------------
# Get data from SBA
# --------------------------------

response = requests.get(url)

data = response.json()

print("Data downloaded successfully.")
print("Total disasters:", len(data))


# --------------------------------
# Take the first disaster
# --------------------------------

first_disaster = data[0]


# --------------------------------
# Show disaster field names
# --------------------------------

print("\nAvailable Disaster Fields:")

for column in first_disaster.keys():
    print(column)


# --------------------------------
# Take the first county
# --------------------------------

first_county = first_disaster["primary_counties"][0]


# --------------------------------
# Show county field names
# --------------------------------

print("\nAvailable County Fields:")

for column in first_county.keys():
    print(column)


# --------------------------------
# Show basic disaster info
# --------------------------------

print("\nFirst Disaster Information:")

print("Disaster Number:", first_disaster["disaster_number"])

print(
    "Description:",
    first_disaster["disaster_description"]
)

print(
    "State:",
    first_disaster["primary_disaster_state_display"]
)

print(
    "Declaration Date:",
    first_disaster["declaration_date"]
)

print(
    "Status:",
    first_disaster["disaster_status_display"]
)


# --------------------------------
#Show ALL primary counties
# --------------------------------

print("\nPrimary Counties:")

for county in first_disaster["primary_counties"]:

    print(
        "County:",
        county["county_name"]
    )

    print(
        "FIPS:",
        county["fips_code_6"]
    )

    print(
        "Latitude:",
        county["latitude"]
    )

    print(
        "Longitude:",
        county["longitude"]
    )

    print("--------------------")