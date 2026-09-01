import csv
import json


#-----------------------------------------------------
# INPUT AMD OUTPUT FILES
#-----------------------------------------------------


csv_file_path = r"Data/SBA_disaster_Final.csv"
json_file_path = r"Data/SBA_disaster_Final.json"

#-----------------------------------------------------
# Store CSV rows 
#-----------------------------------------------------

Data= []



#-----------------------------------------------------
# Read the final CSV
#-----------------------------------------------------

with open(csv_file_path, encoding="utf-8") as csv_file:

    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        Data.append(row)



#-----------------------------------------------------
# Save as JSON
#-----------------------------------------------------


with open(
    json_file_path,
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        Data,
        json_file,
        indent=4
    )

print("SBA_disaster_Final.json created successfully.")
print("Total records:", len(Data))
        