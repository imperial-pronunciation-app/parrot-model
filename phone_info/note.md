# Notes

Contains scripts checking the validity of the phone and phoneme set-up

1. Every phone in allowed_phones.txt must have a mapping in phoible_2176.json
2. No phone in allowed_phones.txt can have a prior against it in prior.txt
3. Every phone in all_phones.txt, but not allowed_phones.txt, must have a prior against it in prior.txt
4. Every phoneme that can be produced from phoible_2176.json must have a mapping in phonemes.json
