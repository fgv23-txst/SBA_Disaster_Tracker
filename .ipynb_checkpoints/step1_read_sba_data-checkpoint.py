import requests


# --------------------------------
# STEP 1: SBA API address
# --------------------------------

url = "https://lending.sba.gov/api/disasters/v1/declarations/"


# --------------------------------
# STEP 2: Get data from SBA
# --------------------------------

response = requests.get(url)

data = response.json()

print("Data downloaded successfully.")
print("Total disasters:", len(data))


# --------------------------------
# STEP 3: Take the first disaster
# --------------------------------

first_disaster = data[0]


# --------------------------------
# STEP 4: Show disaster field names
# --------------------------------

print("\nAvailable Disaster Fields:")

for column in first_disaster.keys():
    print(column)


# --------------------------------
# STEP 5: Take the first county
# --------------------------------

first_county = first_disaster["primary_counties"][0]


# --------------------------------
# STEP 6: Show county field names
# --------------------------------

print("\nAvailable County Fields:")

for column in first_county.keys():
    print(column)


# --------------------------------
# STEP 7: Show basic disaster info
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
# STEP 8: Show ALL primary counties
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