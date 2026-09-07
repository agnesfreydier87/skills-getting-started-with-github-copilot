from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import activities


ACTIVITY_NAME = "Chess Club"
EXISTING_EMAIL = "michael@mergington.edu"
NEW_EMAIL = "new.student@mergington.edu"


def test_root_redirects_to_static_index(client: TestClient):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_current_activity_data(client: TestClient):
    # Arrange
    expected_fields = {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities
    assert set(response.json()[ACTIVITY_NAME]) == expected_fields


def test_signup_adds_participant(client: TestClient):
    # Arrange
    expected_message = f"Signed up {NEW_EMAIL} for {ACTIVITY_NAME}"

    # Act
    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": NEW_EMAIL},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert activities[ACTIVITY_NAME]["participants"].count(NEW_EMAIL) == 1
    assert NEW_EMAIL in activities_response.json()[ACTIVITY_NAME]["participants"]


def test_signup_rejects_duplicate_participant(client: TestClient):
    # Arrange
    initial_participants = deepcopy(activities[ACTIVITY_NAME]["participants"])

    # Act
    response = client.post(
        f"/activities/{ACTIVITY_NAME}/signup",
        params={"email": EXISTING_EMAIL},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activities[ACTIVITY_NAME]["participants"] == initial_participants


def test_signup_rejects_unknown_activity(client: TestClient):
    # Arrange
    initial_activities = deepcopy(activities)

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": NEW_EMAIL},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activities == initial_activities


def test_signup_requires_email(client: TestClient):
    # Arrange
    signup_url = f"/activities/{ACTIVITY_NAME}/signup"

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 422


def test_unregister_removes_participant(client: TestClient):
    # Arrange
    expected_message = f"Unregistered {EXISTING_EMAIL} from {ACTIVITY_NAME}"

    # Act
    response = client.delete(
        f"/activities/{ACTIVITY_NAME}/participants",
        params={"email": EXISTING_EMAIL},
    )
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert EXISTING_EMAIL not in activities[ACTIVITY_NAME]["participants"]
    assert EXISTING_EMAIL not in activities_response.json()[ACTIVITY_NAME][
        "participants"
    ]


def test_unregister_rejects_unknown_participant(client: TestClient):
    # Arrange
    initial_participants = deepcopy(activities[ACTIVITY_NAME]["participants"])

    # Act
    response = client.delete(
        f"/activities/{ACTIVITY_NAME}/participants",
        params={"email": NEW_EMAIL},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
    assert activities[ACTIVITY_NAME]["participants"] == initial_participants


def test_unregister_rejects_unknown_activity(client: TestClient):
    # Arrange
    unknown_activity = "Unknown Activity"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": EXISTING_EMAIL},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_requires_email(client: TestClient):
    # Arrange
    unregister_url = f"/activities/{ACTIVITY_NAME}/participants"

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 422