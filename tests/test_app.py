from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "pytest-user@example.com"
    encoded = urllib.parse.quote(activity, safe='')

    # Sign up
    resp = client.post(f"/activities/{encoded}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    participants = resp2.json()[activity]["participants"]
    assert email in participants

    # Unregister
    resp3 = client.delete(f"/activities/{encoded}/participants?email={email}")
    assert resp3.status_code == 200
    assert "Unregistered" in resp3.json().get("message", "")

    # Verify removed
    resp4 = client.get("/activities")
    assert email not in resp4.json()[activity]["participants"]
