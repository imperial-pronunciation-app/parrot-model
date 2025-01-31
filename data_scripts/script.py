import json


# Load the JSON data
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phoible_2176.json', 'r') as json_file:
  phoible_data = json.load(json_file)

# Extract allophones
allophones = set()
for entry in phoible_data:
  if 'allophones' in entry:
    allophones.update(entry['allophones'].split())

# Load the phones from the text file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/all_phones.txt', 'r') as txt_file:
  all_phones = set(txt_file.read().split())

# Calculate the difference
difference = all_phones.difference(allophones)

# Print the difference
print("Phones in all_phones.txt but not in phoible_2176.json:")
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/prior.txt', 'w') as output_file:
  for phone in difference:
    output_file.write(f"{phone} -10.0\n")