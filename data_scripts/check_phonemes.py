import json


# Load the phones from the all_phones.txt file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/data_scripts/all_phones.txt', 'r') as all_file:
    all_phones = set(all_file.read().split())

# Load the phones from the allowed_phones.txt file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/data_scripts/allowed_phones.txt', 'r') as allowed_file:
    allowed_phones = set(allowed_file.read().split())

# Load the phoible_2176.json file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phoible_2176.json', 'r') as phoible_file:
    phoible_data = json.load(phoible_file)

# Load the phonemes.json file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phonemes.json', 'r') as phonemes_file:
    phonemes_data = json.load(phonemes_file)

with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/prior.txt', 'r') as prior_file:
    prior_data = prior_file.readlines()

# Extract phones from prior.txt
prior_phones = set()
for line in prior_data:
  phone, _ = line.split(" ")
  prior_phones.add(phone)

# Calculate disallowed phones
disallowed_phones = all_phones.difference(allowed_phones)

# Extract allophones from all keys
phoible_mapped_phones = set(phoible_data.keys())

# Print the difference for phones
print("Allowed phones with no phoible phone->phoneme mapping:")
print(allowed_phones.difference(phoible_mapped_phones))

# Print the difference for phones
print("Phones with phoible phone->phoneme mapping but not allowed:")
print(phoible_mapped_phones.difference(allowed_phones))

# Calculate phones in all_phones.txt with a phoneme mapping in phoible_2176.json, but not in allowed_phones.txt
all_phones_mapped = phoible_mapped_phones.intersection(all_phones)
disallowed_mapped = all_phones_mapped.difference(allowed_phones)

# Print the difference for phones
print("Disallowed phones with a phoible phone->phoneme mapping:")
print(disallowed_mapped)

# Extract phonemes from phoible_2176.json
phoible_mapped_phonemes = set(phoible_data.values())

phonemes_with_respelling = set(phonemes_data.keys())

# Print the difference for phonemes
print("Phonemes in phoible_2176.json with no respelling in phonemes.json:")
print(phoible_mapped_phonemes.difference(phonemes_with_respelling))

# Print the difference for phonemes
print("Phonemes in phonemes.json but not in phoible_2176.json:")
print(phonemes_with_respelling.difference(phoible_mapped_phonemes))


# 1. Check that no phone that is in allowed_phones.txt has a prior against it in prior.txt
print("Allowed phones with a prior against them:")
print(allowed_phones.intersection(prior_phones))

# 2. Check that any disallowed phone (i.e. in all_phones.txt but not allowed_phones.txt) has a prior against it in prior.txt
print("Disallowed phones with no prior against them:")
print(disallowed_phones.difference(prior_phones))