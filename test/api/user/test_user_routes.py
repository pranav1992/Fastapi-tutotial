def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={"name": "Pranav", "employee_id": "101"}
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == "101"


def test_create_user_duplicate_employee_id(client):
    client.post(
        "/users/",
        json={"name": "Pranav", "employee_id": "102"}
    )

    response = client.post(
        "/users/",
        json={"name": "Other", "employee_id": "102"}
    )

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]
