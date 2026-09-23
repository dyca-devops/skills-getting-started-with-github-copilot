from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_participant_can_unregister():
    activity_name = "Art Club"
    email = "remove.student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/signup/{email}"
    )
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
