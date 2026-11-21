from app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_names = set(activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json()) == expected_names


def test_signup_adds_participant(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Art Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities["Art Club"]["participants"]


def test_signup_rejects_duplicate(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


def test_signup_rejects_unknown_activity(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Nope/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_rejects_full_activity(client):
    # Arrange
    activity = activities["Basketball Team"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"])]
    email = "late@mergington.edu"

    # Act
    response = client.post("/activities/Basketball Team/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert email not in activity["participants"]


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_student_not_signed_up(client):
    # Arrange
    email = "stranger@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Nope/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_then_unregister_restores_participants(client):
    # Arrange
    before = list(activities["Art Club"]["participants"])
    email = "roundtrip@mergington.edu"

    # Act
    client.post("/activities/Art Club/signup", params={"email": email})
    client.delete("/activities/Art Club/unregister", params={"email": email})

    # Assert
    assert activities["Art Club"]["participants"] == before
