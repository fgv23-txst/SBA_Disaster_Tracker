import pandas as pd

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
         # FILL MISSING COORDINATES USING 2025 CENSUS DATA
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




# ------------------------------------------------------------------------------
                # save the cleaned data to a new CSV
# ------------------------------------------------------------------------------

df.to_csv(
    "sba_disaster_data_clean.csv",
    index=False
)

print("\nClean CSV saved successfully.")