from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_evidence():
    request_body = {
        "title": "Diabetic Retinopathy CNN Study",
        "source": "Research Paper",
        "content": "CNN models can classify diabetic retinopathy images with useful performance when preprocessing and augmentation techniques are applied properly."
    }

    response = client.post("/api/evidence", json=request_body)

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["title"] == request_body["title"]
    assert response_body["source"] == request_body["source"]
    assert response_body["content"] == request_body["content"]
    assert response_body["summary"] is None
    assert "id" in response_body
    assert "created_at" in response_body