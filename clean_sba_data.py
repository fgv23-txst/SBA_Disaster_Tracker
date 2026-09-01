import pandas as pd
import geopandas as gpd

# Read the CSV
df = pd.read_csv(
    "sba_disaster_data.csv",
    dtype={"county_fips": str}
)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print(df.head())

print("Total rows:", len(df))
print("Unique disasters:", df["disaster_number"].nunique())
print("Unique counties:", df["county_fips"].nunique())
print("\nMissing values:")
print(df.isnull().sum())
print("\nCounty types:")
print(df["county_type"].value_counts())


duplicates = df.duplicated(
    subset=[
        "disaster_number",
        "county_fips",
        "county_type"
    ]
)

print("\nPossible duplicate rows:", duplicates.sum())




# ------------------------------------------------------------------------------
                            # CHECK COUNTY FIPS
# ------------------------------------------------------------------------------

# To make sure FIPS is stored as text
df["county_fips"] = df["county_fips"].astype(str)

# Add leading zero if needed
df["county_fips"] = df["county_fips"].str.zfill(5)

print("\nFIPS code lengths:")

print(
    df["county_fips"]
    .str.len()
    .value_counts()
)



# Show any FIPS codes that are NOT 5 characters
bad_fips = df[
    df["county_fips"].str.len() != 5
]


print("\nInvalid FIPS records:")
print(len(bad_fips))

print(bad_fips[
    [
        "state",
        "county_name",
        "county_fips"
    ]
].head(20))




# ------------------------------------------------------------------------------
                            # CLEAN LATITUDE / LONGITUDE
# ------------------------------------------------------------------------------

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)



print("\nMissing coordinates before filling:")

print(
    df[["latitude", "longitude"]]
    .isna()
    .sum()
)


# ------------------------------------------------------------------------------
         # FILL MISSING COORDINATES USING  CENSUS DATA
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 2025 CENSUS
# ------------------------------------------------------------------------------
county_ref = pd.read_csv(
    "Data/2025_Gaz_counties_national.txt",
    sep="|",
    dtype={"GEOID": str}
)




census_lookup = county_ref[
    ["GEOID", "INTPTLAT", "INTPTLONG"]
].copy()

df = df.merge(
    census_lookup,
    left_on="county_fips",
    right_on="GEOID",
    how="left"
)

df["latitude"] = df["latitude"].fillna(
    df["INTPTLAT"]
)

df["longitude"] = df["longitude"].fillna(
    df["INTPTLONG"]
)

print("\nMissing coordinates after 2025 Census lookup:")

print(
    df[["latitude", "longitude"]]
    .isna()
    .sum()
)


# -------------------------------------------------------------
# 2021 CENSUS Older county FIPS
# --------------------------------------------------------------

county_2021 = pd.read_csv(
    r"Data/2021_Gaz_counties_national.txt",
    sep="\t",
    dtype={"GEOID": str}
)

# Remove spaces from column names
county_2021.columns = county_2021.columns.str.strip()

# Keep only coordinate columns
lookup_2021 = county_2021[
    ["GEOID", "INTPTLAT", "INTPTLONG"]
].copy()

lookup_2021 = lookup_2021.rename(
    columns={
        "GEOID": "county_fips",
        "INTPTLAT": "new_latitude",
        "INTPTLONG": "new_longitude"
    }
)

# Join 2021 coordinates
df = df.merge(
    lookup_2021,
    on="county_fips",
    how="left"
)

# Fill ONLY coordinates still missing
df["latitude"] = df["latitude"].fillna(
    df["new_latitude"]
)

df["longitude"] = df["longitude"].fillna(
    df["new_longitude"]
)

print("\nMissing coordinates after 2021 Census:")

print(
    df[["latitude", "longitude"]]
    .isna()
    .sum()
)




# -------------------------------------------------------------
#  FOR ALASKA 
# --------------------------------------------------------------


alaska_lookup = {
    "02053": (60.2134905, -163.4359235),
    "02291": (62.7048922, -156.1553811),
    "02272": (61.5295354, -165.5942167),
    "02271": (62.2835555, -163.1901536),
    "02018": (57.0495083, -170.4062251),
    "02051": (60.9097122, -161.4073619),
    "02052": (61.5235547, -158.0361130),
    "02293": (65.6344779, -154.3251960)
}

for fips, coordinates in alaska_lookup.items():

    latitude = coordinates[0]
    longitude = coordinates[1]

    mask = (
        (df["county_fips"] == fips) &
        (df["latitude"].isna())
    )

    df.loc[mask, "latitude"] = latitude
    df.loc[mask, "longitude"] = longitude

print("\nMissing coordinates after Alaska lookup:")

print(
    df[["latitude", "longitude"]]
    .isna()
    .sum()
)


# --------------------------------------------
# ISLAND AREAS 2021 TIGER/LINE counties
# --------------------------------------------

county_shape_2021 = gpd.read_file(
    r"Data/tl_2021_us_county.zip"
)

county_shape_2021["GEOID"] = (
    county_shape_2021["GEOID"]
    .astype(str)
)

island_lookup = county_shape_2021[
    ["GEOID", "INTPTLAT", "INTPTLON"]
].copy()

island_lookup = island_lookup.rename(
    columns={
        "GEOID": "county_fips",
        "INTPTLAT": "island_latitude",
        "INTPTLON": "island_longitude"
    }
)

df = df.merge(
    island_lookup,
    on="county_fips",
    how="left"
)

df["latitude"] = df["latitude"].fillna(
    df["island_latitude"]
)

df["longitude"] = df["longitude"].fillna(
    df["island_longitude"]
)



# --------------------------------------------
# SOUTH DAKOTA OLD FIPS
# --------------------------------------------

mask = (
    (df["county_fips"] == "46113") &
    (df["latitude"].isna())
)

df.loc[mask, "latitude"] = 43.3333930
df.loc[mask, "longitude"] = -102.5614857



print("\nFINAL COORDINATE CHECK:")

print(
    df[["latitude", "longitude"]]
    .isna()
    .sum()
)


#---------------------------------------------------------
# remove extra columns
#----------------------------------------------------------

helper_columns = [
    "GEOID",
    "INTPTLAT",
    "INTPTLONG",
    "new_latitude",
    "new_longitude",
    "island_latitude",
    "island_longitude"
]

df = df.drop(
    columns=helper_columns,
    errors="ignore"
)




# ------------------------------------------------------------------------------
                # save the cleaned data to a new CSV
# ------------------------------------------------------------------------------

df.to_csv(
     r"Data/SBA_disaster_Final.csv",
    index=False
)

print("\nSBA_disaster_Final.csv saved successfully.")