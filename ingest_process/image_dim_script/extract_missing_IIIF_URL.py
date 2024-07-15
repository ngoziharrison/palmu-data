import pandas as pd
from PIL import Image
from io import BytesIO
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os

#get folder containing CSVs to check
csvs_file_path = input("Enter the path to the folder containing CSVs: ").strip()
missing = pd.DataFrame(columns=["Item ARK","Parent ARK","File Name","Object Type","coll id","AltIdentifier.local","Collection","Series","Title","AltTitle.other","Description.note","References","Genre","Language","Type.typeOfResource","Date.created","Date.normalized","Note","Subject.coordinates","Subject topic","Inscription","media.format","media.height","media.width","Thumbnail","IIIF Access URL","External item record","Repository","Rights.servicesContact","Acquisition method","Physical status","Violent Content","Series & Collection","Creation date/time","Last modification date/time","Description (Eng)","Description (Ara)","Genre (old)","Inscription (old)","Inscription 2 (old)","Alt Title"])

# Extract the rows missing the IIIF urls and add to a missing csv remove rows missing the IIIF urls from csv
def extract_rows_missing_IIIF_URL(df):
    for index, row in df.iterrows():
        if row["Object Type"] == "Work":
            if pd.isnull(row["IIIF Access URL"]) == True:
                missing.loc[len(missing)] = row
                df.drop(index, inplace = True)

# Loop over files in provided directory
for index, filename in enumerate(os.listdir(csvs_file_path)):
    print(f"Checking {filename}")
    df = pd.read_csv(csvs_file_path + "/" + filename)
    df1 = pd.read_csv(csvs_file_path + "/" + filename)
    extract_rows_missing_IIIF_URL(df1)
    # Check to see if there were any changes made to the data frame, if so, write df1 to the original csv
    if len(df) > len(df1):
        df1.to_csv(csvs_file_path + "/" + filename)
    #if index == 30:
    #    break

# Export missing rows to csv
print("exporting to PalMu_missing.csv")
missing.to_csv("PalMu_missing.csv", index=False)