"""
Integration tests for FastAPI endpoints using the AAA (Arrange-Act-Assert) pattern.

Tests verify all HTTP endpoints work correctly through the full request-response cycle:
- GET / (root redirect)
- GET /activities (list all activities)
- POST /activities/{activity_name}/signup (enroll a student)
- POST /activities/{activity_name}/unregister (remove a student)
"""

import pytest


class TestRootEndpoint:
    """Tests for the root GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Verify that GET / redirects to the static HTML frontend.
        
        AAA Pattern:
        - Arrange: Client is already set up via fixture
        - Act: Make GET request to root
        - Assert: Verify 307 redirect status and location header
        """
        # Arrange
        # (client fixture handles setup)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_all_activities_returns_200(self, client):
        """
        Verify that GET /activities returns all available activities with 200 status.
        
        AAA Pattern:
        - Arrange: Client is ready
        - Act: Make GET request to /activities
        - Assert: Verify 200 status and response contains all activities
        """
        # Arrange
        # (client fixture handles setup)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Science Olympiad" in activities
    
    def test_get_activities_includes_required_fields(self, client):
        """
        Verify that each activity has the required fields.
        
        AAA Pattern:
        - Arrange: Client ready
        - Act: Get activities and extract one
        - Assert: Verify required fields exist
        """
        # Arrange
        # (client fixture handles setup)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        first_activity = activities["Chess Club"]
        
        # Assert
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
    
    def test_get_activities_preserves_participant_list(self, client):
        """
        Verify that participant lists are returned correctly.
        
        AAA Pattern:
        - Arrange: Client ready
        - Act: Get activities
        - Assert: Verify Chess Club has its initial participants
        """
        # Arrange
        # (client fixture handles setup)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_participants = activities["Chess Club"]["participants"]
        
        # Assert
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_student_returns_200(self, client, reset_activities, sample_email, valid_activity_name):
        """
        Verify that signing up a new student returns 200 and adds them to activity.
        
        AAA Pattern:
        - Arrange: Set up client, test email, and activity name
        - Act: Make POST request to signup endpoint
        - Assert: Verify 200 status and student is added to participants
        """
        # Arrange
        activity_name = valid_activity_name
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    def test_signup_adds_student_to_participants(self, client, reset_activities, sample_email, valid_activity_name):
        """
        Verify that a signed-up student appears in the activity participants.
        
        AAA Pattern:
        - Arrange: Set up test data
        - Act: Sign up a student, then retrieve activities
        - Assert: Verify student is in the participants list
        """
        # Arrange
        activity_name = valid_activity_name
        email = sample_email
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()
        participants = activities[activity_name]["participants"]
        
        # Assert
        assert email in participants
    
    def test_signup_invalid_activity_returns_404(self, client, reset_activities, sample_email, invalid_activity_name):
        """
        Verify that signing up for a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Set up invalid activity name
        - Act: Attempt to sign up for invalid activity
        - Assert: Verify 404 error response
        """
        # Arrange
        invalid_name = invalid_activity_name
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{invalid_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_student_adds_again(self, client, reset_activities, valid_activity_name):
        """
        Verify that signing up twice adds the student twice (no duplicate prevention).
        
        AAA Pattern:
        - Arrange: Set up activity and a student already in it
        - Act: Sign the same student up again
        - Assert: Verify student appears twice in participants
        """
        # Arrange
        activity_name = valid_activity_name
        email = "doubledup@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # Assert
        assert participants.count(email) == 2


class TestUnregisterEndpoint:
    """Tests for the POST /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_existing_student_returns_200(self, client, reset_activities, valid_activity_name):
        """
        Verify that unregistering an enrolled student returns 200.
        
        AAA Pattern:
        - Arrange: Use a student already in an activity
        - Act: Unregister the student
        - Assert: Verify 200 status and success message
        """
        # Arrange
        activity_name = valid_activity_name
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    def test_unregister_removes_student_from_participants(self, client, reset_activities, valid_activity_name):
        """
        Verify that unregistering removes the student from participants list.
        
        AAA Pattern:
        - Arrange: Set up activity and student to remove
        - Act: Unregister the student, then retrieve activities
        - Assert: Verify student is no longer in participants
        """
        # Arrange
        activity_name = valid_activity_name
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # Assert
        assert email not in participants
    
    def test_unregister_invalid_activity_returns_404(self, client, reset_activities, sample_email, invalid_activity_name):
        """
        Verify that unregistering from non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Set up invalid activity name
        - Act: Attempt to unregister from invalid activity
        - Assert: Verify 404 error
        """
        # Arrange
        invalid_name = invalid_activity_name
        email = sample_email
        
        # Act
        response = client.post(
            f"/activities/{invalid_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_student_not_in_activity_returns_400(self, client, reset_activities, sample_email, valid_activity_name):
        """
        Verify that unregistering a non-enrolled student returns 400.
        
        AAA Pattern:
        - Arrange: Set up activity and student not in it
        - Act: Try to unregister non-enrolled student
        - Assert: Verify 400 error
        """
        # Arrange
        activity_name = valid_activity_name
        email = sample_email  # Not in any activity
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Participant not found in this activity"
    
    def test_unregister_one_instance_when_registered_twice(self, client, reset_activities, valid_activity_name):
        """
        Verify that unregister removes only one instance if student signed up twice.
        
        AAA Pattern:
        - Arrange: Sign up a student twice
        - Act: Unregister the student once
        - Assert: Verify student still exists once in participants
        """
        # Arrange
        activity_name = valid_activity_name
        email = "repeated@mergington.edu"
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        get_response = client.get("/activities")
        participants = get_response.json()[activity_name]["participants"]
        
        # Assert
        assert response.status_code == 200
        assert participants.count(email) == 1
