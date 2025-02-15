import json
from typing import Dict, List, Set, cast

import pytest

from config.config import SUPPORTED_LANGUAGES


@pytest.fixture(scope="module")
def all_phones() -> Set[str]:
    """Loads the complete set of all phones"""
    with open("config/all_phones.txt", "r") as all_file:
        return set(all_file.read().split())

@pytest.fixture(scope="module")
def all_phonemes() -> Set[str]:
    """Loads the complete set of all phonemes"""
    with open("config/all_phonemes.json", "r") as phonemes_file:
        return set(cast(Dict[str, str], json.load(phonemes_file)).keys())

def load_phone_to_phonemes(lang: str) -> Dict[str, str]:
    """Loads phone-to-phoneme mappings for a language."""
    with open(f"config/languages/{lang}/phone_to_phonemes.json", "r") as phone_to_phonemes_file:
        return cast(Dict[str, str], json.load(phone_to_phonemes_file))

def load_prior_phones(lang: str) -> Set[str]:
    """Loads phones with priors for a language."""
    with open(f"config/languages/{lang}/prior.txt", "r") as prior_file:
        return {line.split(" ")[0] for line in prior_file.readlines()}
    
def load_allowed_phones(lang: str) -> Set[str]:
    return set(load_phone_to_phonemes(lang).keys())

@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_no_prior_against_allowed_phones(lang: str) -> None:
    """No phone in phone_to_phonemes.json can have a prior against it in prior.txt."""    
    allowed_phones = load_allowed_phones(lang)
    prior_phones = load_prior_phones(lang)
    
    conflicting_priors = allowed_phones.intersection(prior_phones)
    assert not conflicting_priors, f"Allowed phones with priors in {lang}: {conflicting_priors}"

@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_disallowed_phones_have_prior(lang: str, all_phones: Set[str]) -> None:
    """Every phone in all_phones.txt, but not in phone_to_phonemes.json, must have a prior in prior.txt."""    
    allowed_phones = load_allowed_phones(lang)
    prior_phones = load_prior_phones(lang)

    disallowed_phones = all_phones.difference(allowed_phones)
    missing_priors = disallowed_phones.difference(prior_phones)
    
    assert not missing_priors, f"Disallowed phones without prior in {lang}: {missing_priors}"

@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_phonemes_are_valid(lang: str, all_phonemes: List[str]) -> None:
    """Every phoneme in phone_to_phonemes.json must be in all_phonemes.json."""    
    phone_to_phonemes_data = load_phone_to_phonemes(lang)
    phone_to_phonemes_mapped_phonemes = set(phone_to_phonemes_data.values())

    missing_phoneme_mappings = phone_to_phonemes_mapped_phonemes.difference(all_phonemes)
    assert not missing_phoneme_mappings, f"Phonemes without mapping in {lang}: {missing_phoneme_mappings}"
