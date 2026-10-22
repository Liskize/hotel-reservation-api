def create_hotel(client, **overrides):
    payload = {
        "nom": "Hotel Central",
        "ville": "Libreville",
        "adresse": "Boulevard de l'Independance",
        "nombre_chambres": 10,
    }
    payload.update(overrides)
    return client.post("/api/v1/hotels", json=payload)


def create_client(client, **overrides):
    payload = {
        "nom": "Mba",
        "prenom": "Alice",
        "email": "alice.mba@example.com",
        "telephone": "+241060000001",
    }
    payload.update(overrides)
    return client.post("/api/v1/clients", json=payload)


def test_health_and_unknown_route(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "OK"

    response = client.get("/api/v1/inconnue")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Ressource introuvable"


def test_hotel_crud_pagination_and_validation(client):
    response = create_hotel(client)
    assert response.status_code == 201
    hotel_id = response.get_json()["id"]

    create_hotel(client, nom="Residence Ocean", ville="Port-Gentil")
    response = client.get("/api/v1/hotels?ville=libre&page=1&per_page=1")
    body = response.get_json()
    assert response.status_code == 200
    assert body["pagination"]["total"] == 1
    assert body["items"][0]["id"] == hotel_id

    response = client.put(
        f"/api/v1/hotels/{hotel_id}",
        json={"nombre_chambres": 20},
    )
    assert response.status_code == 200
    assert response.get_json()["nombre_chambres"] == 20

    response = create_hotel(client, nom="Invalide", nombre_chambres=0)
    assert response.status_code == 422

    response = client.delete(f"/api/v1/hotels/{hotel_id}")
    assert response.status_code == 204
    assert client.get(f"/api/v1/hotels/{hotel_id}").status_code == 404


def test_client_crud_and_duplicate_email(client):
    response = create_client(client)
    assert response.status_code == 201
    client_id = response.get_json()["id"]

    response = create_client(client, prenom="Autre")
    assert response.status_code == 409

    response = client.put(
        f"/api/v1/clients/{client_id}",
        json={"telephone": "+241060000099"},
    )
    assert response.status_code == 200
    assert response.get_json()["telephone"] == "+241060000099"

    response = client.get("/api/v1/clients?email=alice")
    assert response.status_code == 200
    assert response.get_json()["pagination"]["total"] == 1


def test_reservation_crud_filters_and_business_rules(client):
    hotel_id = create_hotel(client).get_json()["id"]
    client_id = create_client(client).get_json()["id"]
    payload = {
        "hotel_id": hotel_id,
        "client_id": client_id,
        "date_debut": "2026-11-10",
        "date_fin": "2026-11-15",
        "statut": "EN_ATTENTE",
        "montant_total": "250000.00",
    }

    invalid = {**payload, "date_fin": "2026-11-09"}
    assert client.post("/api/v1/reservations", json=invalid).status_code == 422

    missing_hotel = {**payload, "hotel_id": 9999}
    assert client.post("/api/v1/reservations", json=missing_hotel).status_code == 404

    response = client.post("/api/v1/reservations", json=payload)
    assert response.status_code == 201
    reservation_id = response.get_json()["id"]

    assert client.post("/api/v1/reservations", json=payload).status_code == 409

    response = client.get(
        f"/api/v1/reservations?hotel_id={hotel_id}&statut=EN_ATTENTE"
    )
    assert response.status_code == 200
    assert response.get_json()["pagination"]["total"] == 1

    response = client.put(
        f"/api/v1/reservations/{reservation_id}",
        json={"statut": "CONFIRMEE"},
    )
    assert response.status_code == 200
    assert response.get_json()["statut"] == "CONFIRMEE"

    assert client.delete(f"/api/v1/hotels/{hotel_id}").status_code == 409
    assert client.delete(f"/api/v1/clients/{client_id}").status_code == 409
    assert client.delete(f"/api/v1/reservations/{reservation_id}").status_code == 204
    assert client.delete(f"/api/v1/hotels/{hotel_id}").status_code == 204
    assert client.delete(f"/api/v1/clients/{client_id}").status_code == 204
