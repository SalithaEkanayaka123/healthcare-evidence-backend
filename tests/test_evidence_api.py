from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_sample_evidence():
    request_body = {
        "title": "Diabetic Retinopathy CNN Study",
        "source": "Research Paper",
        "content": (
            "CNN models can classify diabetic retinopathy images with useful "
            "performance when preprocessing and augmentation techniques are applied properly."
        )
    }

    response = client.post("/api/evidence", json=request_body)

    assert response.status_code == 201

    return response.json()


def test_create_evidence():
    response_body = create_sample_evidence()

    assert response_body["title"] == "Diabetic Retinopathy CNN Study"
    assert response_body["source"] == "Research Paper"
    assert response_body["summary"] is None
    assert "id" in response_body
    assert "created_at" in response_body


def test_get_all_evidence():
    create_sample_evidence()

    response = client.get("/api/evidence")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_evidence_by_id():
    created_evidence = create_sample_evidence()
    evidence_id = created_evidence["id"]

    response = client.get(f"/api/evidence/{evidence_id}")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["id"] == evidence_id
    assert response_body["title"] == created_evidence["title"]


def test_update_evidence():
    created_evidence = create_sample_evidence()
    evidence_id = created_evidence["id"]

    update_body = {
        "title": "Updated Diabetic Retinopathy Study",
        "source": "Updated Research Paper",
        "content": (
            "Updated evidence content with enough characters to pass validation rules."
        )
    }

    response = client.put(f"/api/evidence/{evidence_id}", json=update_body)

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["id"] == evidence_id
    assert response_body["title"] == update_body["title"]
    assert response_body["source"] == update_body["source"]
    assert response_body["content"] == update_body["content"]


def test_generate_summary():
    created_evidence = create_sample_evidence()
    evidence_id = created_evidence["id"]

    response = client.post(f"/api/evidence/{evidence_id}/summary")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["evidence_id"] == evidence_id
    assert "summary" in response_body
    assert response_body["summary"] is not None


def test_delete_evidence():
    created_evidence = create_sample_evidence()
    evidence_id = created_evidence["id"]

    delete_response = client.delete(f"/api/evidence/{evidence_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/evidence/{evidence_id}")

    assert get_response.status_code == 404


def test_get_evidence_not_found():
    response = client.get("/api/evidence/999999")

    assert response.status_code == 404