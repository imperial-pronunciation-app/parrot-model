from enum import Enum


class Language(str, Enum):
    ENG = "eng"
    POR = "por"

MODELS_FOR_LANGUAGES = {
    Language.ENG: "eng2102",
    Language.POR: "uni2005"
}

SUPPORTED_LANGUAGES = [lang.value for lang in Language]

GARBAGE_DETECTABLE_LANGUAGES = [Language.ENG]