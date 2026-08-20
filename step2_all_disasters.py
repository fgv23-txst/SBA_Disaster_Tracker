import requests

# SBA API
url = "https://lending.sba.gov/api/disasters/v1/declarations/"

# Get data
response = requests.get(url)

data = response.json()

print("Total disasters:", len(data))

print("\nDisaster and County Records:\n")

# Go through every disaster
for disaster in data:

    disaster_number = disaster["disaster_number"]
    state = disaster["primary_disaster_state_display"]
    description = disaster["disaster_description"]

    # Go through every primary county in that disaster
    for county in disaster["primary_counties"]:

        county_name = county["county_name"]

        print(
            disaster_number,
            "|",
            state,
            "|",
            description,
            "|",
            county_name
        )