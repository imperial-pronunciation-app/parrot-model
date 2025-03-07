import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.config import SUPPORTED_LANGUAGES, Language


@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_valid_phoneme_inference(lang: Language) -> None:
    with TestClient(app) as client:
        with open('tests/assets/hello.wav', 'rb') as f:
            files = {"audio_file": f}
            response = client.post(f"/api/v1/{lang}/infer_word_phonemes", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["success"]
        assert data["phonemes"] is not None
        assert data["words"] == ["hello"]

@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_garbage_detection(lang: Language) -> None:
    with TestClient(app) as client:
        with open('tests/assets/i_am_a_mouse.wav', 'rb') as f:
            files = {"audio_file": f}
            response = client.post(f"/api/v1/{lang}/infer_word_phonemes", files=files)
        assert response.status_code == 200
        data = response.json()
        assert not data["success"]
        assert data["phonemes"] == []
        assert data["words"] == []

def test_invalid_language() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/xyz/infer_word_phonemes",
            files={"audio_file": ("test.wav", b"testdata", "audio/wav")},
            data={"attempt_word": "hello"}
        )
        assert response.status_code == 400
        assert response.json()["detail"].startswith("Unsupported language")
