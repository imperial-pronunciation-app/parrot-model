from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.config import GARBAGE_DETECTABLE_LANGUAGES, SUPPORTED_LANGUAGES, Language


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Provides a reusable FastAPI TestClient instance with proper lifespan handling."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def hello_wav() -> bytes:
    """Loads the hello.wav test file."""
    return Path("tests/assets/hello.wav").read_bytes()

@pytest.fixture
def garbage_wav() -> bytes:
    """Loads the i_am_a_mouse.wav test file."""
    return Path("tests/assets/i_am_a_mouse.wav").read_bytes()

@pytest.mark.parametrize("lang", GARBAGE_DETECTABLE_LANGUAGES)
def test_valid_phoneme_and_word_inference(client: TestClient, hello_wav: bytes, lang: Language) -> None:
    response = client.post(
        f"/api/v1/{lang}/pronunciation_inference",
        files={"audio_file": ("hello.wav", hello_wav, "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["phonemes"] is not None
    assert data["words"] == ["hello"]

@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_valid_phoneme_inference(client: TestClient, hello_wav: bytes, lang: Language) -> None:
    response = client.post(
        f"/api/v1/{lang}/pronunciation_inference",
        files={"audio_file": ("hello.wav", hello_wav, "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["phonemes"] is not None

@pytest.mark.parametrize("lang", GARBAGE_DETECTABLE_LANGUAGES)
def test_garbage_detection(client: TestClient, garbage_wav: bytes, lang: Language) -> None:
    response = client.post(
        f"/api/v1/{lang}/pronunciation_inference",
        files={"audio_file": ("i_am_a_mouse.wav", garbage_wav, "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert not data["success"]
    assert data["phonemes"] == []
    assert data["words"] == []

def test_invalid_language(client: TestClient) -> None:
    response = client.post(
        "/api/v1/xyz/pronunciation_inference",
        files={"audio_file": ("test.wav", b"testdata", "audio/wav")},
        data={"attempt_word": "hello"}
    )
    assert response.status_code == 422
