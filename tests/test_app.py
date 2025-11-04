import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST /activities/{activity_name}/signup
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "anotherstudent@mergington.edu"),
])
def test_signup_for_activity(activity, email):
    # Remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

# Test duplicate signup
def test_duplicate_signup():
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    # Ensure participant is signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

# Test DELETE /activities/{activity_name}/signup
def test_unregister_participant():
    activity = "Chess Club"
    email = "removeme@mergington.edu"
    # Ensure participant is signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

# Test unregister non-existent participant
def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
