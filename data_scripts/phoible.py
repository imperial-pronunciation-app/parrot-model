import csv
import json

import pandas as pd


input_file = '/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phoible.csv'
output_file = '/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phoible_2176.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
  open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    if reader.fieldnames is None:
        raise ValueError("Input file does not contain fieldnames.")
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    writer.writeheader()
    for row in reader:
     if row['InventoryID'] == '2176':
      writer.writerow(row)
      
# Load the filtered CSV file
df = pd.read_csv(output_file)

# Keep only the specified columns
df = df[['GlyphID', 'Phoneme', 'Allophones']]

# Save the updated DataFrame back to the CSV file
df.to_csv(output_file, index=False)

# Load the filtered CSV file
df = pd.read_csv(output_file)

# Create a dictionary mapping each phone in an allophone to the corresponding phoneme
phone_to_phoneme = {}
for _, row in df.iterrows():
  phoneme = row['Phoneme']
  allophones = row['Allophones'].split()
  for phone in allophones:
    phone_to_phoneme[phone] = phoneme

# Save the dictionary to a JSON file
json_output_file = output_file.replace('.csv', '.json')
with open(json_output_file, 'w', encoding='utf-8') as jsonfile:
  json.dump(phone_to_phoneme, jsonfile, ensure_ascii=False, indent=4)