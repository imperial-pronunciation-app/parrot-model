import pytest
from fastapi.testclient import TestClient

from app.main import app
from config.config import SUPPORTED_LANGUAGES


@pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
def test_valid_phoneme_inference(lang: str) -> None:
    with TestClient(app) as client:
        with open('tests/assets/hello.wav', 'rb') as f:
            files = {"audio_file": f}
            data = {"attempt_word": "hello"}
            response = client.post(f"/api/v1/{lang}/infer_phonemes", files=files, data=data)
        assert response.status_code == 200
        assert "phonemes" in response.json()

def test_invalid_language() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/xyz/infer_phonemes",
            files={"audio_file": ("test.wav", b"testdata", "audio/wav")},
            data={"attempt_word": "hello"}
        )
        assert response.status_code == 400
        assert response.json()["detail"].startswith("Unsupported language")
