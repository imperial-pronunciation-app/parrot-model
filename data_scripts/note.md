allowed_phones.txt contains all phones that we can allow Allosaurus to output (because we have mappings for them).
Any phone not in allowed_phones, but producable by Allosaurus, needs a very low prior in prior.txt

Note: This is not just English phones, as we need American pronunciations as well.

Changes:
Add {'ɫ', 'b̥', 'ɾ'} to allowed_phones as they have a phoible_2176 mapping
Remove {'t̠', 'ɘ', 'iː', 'x', 'ɛː', 'aː', 'ɔː', 'ʍ', 'ɑː', 'əː', 'ʉː', 'ɜː', 'ɒ', 'r', 'ɯ', 'ə', 'uː', 'oː', 'ʉ', 'd̠', 'ɵː', 'øː', 'ɐ', 'ɻ', 'ɪ̯', 'a', 'ɐː', 'ɒː', 'ʔ', 'eː', 'e̞'} from allowed_phones and add priors, as they have no phoible_2176 mapping

Remove {'d̠ʒ',tʰ', 'pʰ', 't̠ʃ', 'ɚ', } from phoible_2176 as they are unused phonemes in English, but add back later if they have corresponding phones, and just map phone to same phoneme
Add respellings (maybe) for {'ɹ', 't', 'p', 'k', 't', 'p', 'ɔ', 'u', 'i', 'ɑ'} to phonemes.json

Replace ei -> eɪ in phoible_2176