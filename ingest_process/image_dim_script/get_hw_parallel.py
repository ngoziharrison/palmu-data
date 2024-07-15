import pandas as pd
from PIL import Image
from io import BytesIO
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os

# Get CSV file to output errors
# Check to see if there is an existing errors csv otherwise create one
if os.path.isfile("errors.csv"): 
    errs = pd.read_csv("errors.csv")
else:
    errs = pd.DataFrame(columns=["csv file", "row number", "error message"])
    
# Get input CSV file path from user and strip extra whitespace
csv_file_path = input("Enter the path to the input CSV file: ").strip()

# Extract file name without extension
file_name = os.path.splitext(os.path.basename(csv_file_path))[0]

# Read CSV file
df = pd.read_csv(csv_file_path)

# Create new columns for height and width
df['media.height'] = None
df['media.width'] = None


# Function to get image dimensions from URL
# If try catch encounters an error will append to the errors csv
def get_image_dimensions(url, index):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        return width, height
    except Exception as e:
        print(f"Error getting dimensions for {url}: {e}")
        errs.loc[len(errs)] = [file_name + ".csv", index, f"Error getting dimensions for {url}: {e}" ]
        return None, None

# Function to update DataFrame with image dimensions
def update_dimensions(index, row):
    if row["Object Type"] == "Work" and (pd.isnull(row["media.height"]) == True or pd.isnull(row["media.width"]) == True):
        image_url_column = 'IIIF Access URL'
        image_url = row[image_url_column]
        width, height = get_image_dimensions(image_url, index)
        df.at[index, 'media.width'] = width
        df.at[index, 'media.height'] = height

# Update DataFrame with image dimensions in parallel using concurrent.futures module
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on your system
    futures = [executor.submit(update_dimensions, index, row) for index, row in df.iterrows()]
    for future in tqdm(futures, total=len(futures), desc="Processing images"):
        future.result()


# Save the updated DataFrame to a new CSV file with original file name
output_csv_file_path = f'{file_name}_dim.csv'
df.to_csv(output_csv_file_path, index=False)

# Check to see if errors were generated, if so export errors file, if not discard
if len(errs) > 0:
    errs.to_csv("errors.csv", index=False)

# Print out a confirmation message
print(f"Image dimensions added and saved to {output_csv_file_path}")