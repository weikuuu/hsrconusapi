import pytest


def create_light_cone(client, payload):
    response = client.post("/light-cones", json=payload)
    assert response.status_code == 201
    return response.json()


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "HSR Light Cone Shelf API"}


def test_get_light_cones(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)

    response = client.get("/light-cones")

    assert response.status_code == 200
    assert response.json() == [light_cone_payload]


def test_get_existing_light_cone(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)

    response = client.get(f"/light-cones/{light_cone_payload['id']}")

    assert response.status_code == 200
    assert response.json() == light_cone_payload


def test_get_missing_light_cone_returns_404(client):
    response = client.get("/light-cones/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Light cone not found"}


def test_create_light_cone(client, light_cone_payload):
    response = client.post("/light-cones", json=light_cone_payload)

    assert response.status_code == 201
    assert response.json() == light_cone_payload


def test_create_duplicate_id_returns_409(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)

    response = client.post("/light-cones", json=light_cone_payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Light cone with this id already exists"}


def test_update_light_cone(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)
    updated_payload = {
        **light_cone_payload,
        "name": "Memory's Curtain Never Falls",
        "atk": 500,
        "description": None,
    }

    response = client.put("/light-cones/1", json=updated_payload)

    assert response.status_code == 200
    assert response.json() == updated_payload

    get_response = client.get("/light-cones/1")
    assert get_response.json() == updated_payload


def test_update_with_mismatched_path_and_body_id_returns_400(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)
    mismatched_payload = {**light_cone_payload, "id": 2}

    response = client.put("/light-cones/1", json=mismatched_payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "Path id and body id must match"}


def test_delete_light_cone(client, light_cone_payload):
    create_light_cone(client, light_cone_payload)

    response = client.delete("/light-cones/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Light cone deleted"}
    assert client.get("/light-cones/1").status_code == 404


def test_delete_missing_light_cone_returns_404(client):
    response = client.delete("/light-cones/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Light cone not found"}


@pytest.mark.parametrize(
    "invalid_update",
    [
        {"stars": 6},
        {"name": ""},
        {"level": 0},
        {"atk": -1},
    ],
)
def test_create_rejects_invalid_data(client, light_cone_payload, invalid_update):
    invalid_payload = {**light_cone_payload, **invalid_update}

    response = client.post("/light-cones", json=invalid_payload)

    assert response.status_code == 422
