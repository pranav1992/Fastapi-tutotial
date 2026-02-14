
def test_create_task_success(client):
    response = client.post(
        "/tasks/create-task/",
        json={"name": "Pranav", "description": "101 102"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Pranav"
    assert response.json()["description"] == "101 102"
    assert response.json()["name_lower"] == "pranav"


def test_create_task_duplicate_name(client):
    response = client.post(
        "/tasks/create-task/",
        json={"name": "Pranav", "description": "102"}
    )
    assert response.status_code == 409


def test_get_all_tasks(client):
    response = client.get("/tasks/get-all-tasks/")
    assert response.status_code == 200


def test_assign_task_success_and_duplicate(client):
    user_id = "33333333-3333-3333-3333-333333333333"
    task_id = "44444444-4444-4444-4444-444444444444"

    first = client.post(
        "/tasks/assign-task/",
        params={"user_id": user_id, "task_id": task_id},
    )
    assert first.status_code == 200

    duplicate = client.post(
        "/tasks/assign-task/",
        params={"user_id": user_id, "task_id": task_id},
    )
    assert duplicate.status_code == 400
    message = duplicate.json()["message"]
    assert f"User '{user_id}' is already assigned" in message
