from fastapi.testclient import TestClient

from app.main import app


def test_audio_phonemes() -> None:
  client = TestClient(app)
  
  with open('tests/assets/hello.wav', 'rb') as f:
    files = {"audio_file": f}
    response = client.post("/api/v1/infer_phonemes", files=files)
  print(response.json())
  assert "phonemes" in response.json()
  