import json


# Load the phones from the all_phones.txt file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/phone_info/all_phones.txt', 'r') as all_file:
    all_phones = set(all_file.read().split())

# Load the phones from the allowed_phones.txt file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/phone_info/allowed_phones.txt', 'r') as allowed_file:
    allowed_phones = set(allowed_file.read().split())

# Load the phoible_2176.json file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phoible_2176.json', 'r') as phoible_file:
    phoible_data = json.load(phoible_file)

# Load the phonemes.json file
with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/resources/phonemes.json', 'r') as phonemes_file:
    phonemes_data = json.load(phonemes_file)

with open('/home/euan/Documents/imperial/third_year/segp/parrot-model/app/prior.txt', 'r') as prior_file:
    prior_data = prior_file.readlines()

# Extract phones from prior.txt
prior_phones = set()
for line in prior_data:
    phone, _ = line.split(" ")
    prior_phones.add(phone)

# Calculate disallowed phones
disallowed_phones = all_phones.difference(allowed_phones)

# Extract mapped phones
phoible_mapped_phones = set(phoible_data.keys())

# Phonemes in phoible_2176.json, may exceed those that have allowed phones mapping to them
phoible_mapped_phonemes = set(phoible_data.values())

phonemes_with_respelling = set(phonemes_data.keys())

# 1. Every phone in allowed_phones.txt should have a phone->phoneme mapping in phoible_2176.json
if len(allowed_phones.difference(phoible_mapped_phones)) > 0:
    print("The following allowed phones do not have a phoible_2176 mapping")
    print(allowed_phones.difference(phoible_mapped_phones))
    exit(1)

# 2. No phone in allowed_phones.txt can have a prior against it in prior.txt
if len(allowed_phones.intersection(prior_phones)) > 0:
    print("The following allowed phones have a prior against them")
    print(allowed_phones.intersection(prior_phones))
    exit(1)

# 3. Every phone in all_phones.txt, but not allowed_phones.txt, must have a prior against it in prior.txt
if len(disallowed_phones.difference(prior_phones)) > 0:
    print("The following disallowed phones do not have a prior against them")
    print(disallowed_phones.difference(prior_phones))
    exit(1)

# 4. Every phoneme that can be produced from phoible_2176.json must have a mapping in phonemes.json
if len(phoible_mapped_phonemes.difference(phonemes_with_respelling)) > 0:
    print("The following phonemes in phoible_2176.json do not have a mapping in phonemes.json")
    print(phoible_mapped_phonemes.difference(phonemes_with_respelling))
    exit(1)
