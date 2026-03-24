"""
Tests for POST /activities/{activity_name}/signup endpoint using the AAA pattern.

Covers:
  - Successful signup (200)
  - Activity not found (404)
  - Student already signed up (400)
  - Activity is full (400)
"""

import pytest


class TestSignupSuccess:
    """Tests for successful signup scenarios."""
    
    def test_signup_adds_participant_and_returns_200(self, client):
        """
        Test that valid signup adds email to participants and returns 200
        
        AAA Pattern:
          - Arrange: Define activity and email
          - Act: Make POST request to /activities/{name}/signup
          - Assert: Verify 200 status and email in participants
        """
        # Arrange
        activity_name = "Cycling Club"
        email = "newstudent@student.uva.nl"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        
        # Verify participant was added by fetching activities
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants
    
    def test_signup_response_format(self, client):
        """
        Test that signup response has correct message format
        
        AAA Pattern:
          - Arrange: Define activity and email
          - Act: Make POST request to /activities/{name}/signup
          - Assert: Verify response JSON structure
        """
        # Arrange
        activity_name = "Data Science Society"
        email = "test@student.uva.nl"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" == data["message"]


class TestSignupActivityNotFound:
    """Tests for signup with non-existent activity."""
    
    def test_signup_unknown_activity_returns_404(self, client):
        """
        Test that signup to non-existent activity returns 404
        
        AAA Pattern:
          - Arrange: Define fake activity name
          - Act: Make POST request to /activities/{fake_name}/signup
          - Assert: Verify 404 status and error detail
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@student.uva.nl"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestSignupAlreadyRegistered:
    """Tests for signup when student is already registered."""
    
    def test_signup_already_registered_returns_400(self, client):
        """
        Test that signing up for same activity twice returns 400
        
        AAA Pattern:
          - Arrange: Get existing participant from activity
          - Act: Try to sign up same email twice
          - Assert: Verify 400 status on second signup
        """
        # Arrange
        activity_name = "Cycling Club"
        existing_participant = client.get("/activities").json()[activity_name]["participants"][0]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_participant}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"


class TestSignupActivityFull:
    """Tests for signup when activity is at capacity."""
    
    def test_signup_full_activity_returns_400(self, client):
        """
        Test that signing up for a full activity returns 400
        
        AAA Pattern:
          - Arrange: Get activity with capacity=1, fill it, prepare new email
          - Act: Try to sign up when activity is full
          - Assert: Verify 400 status and error message
        """
        # Arrange
        activity_name = "Photography Workshop"  # max_participants: 12
        
        # Get current participants
        activities_response = client.get("/activities")
        activity = activities_response.json()[activity_name]
        current_count = len(activity["participants"])
        max_participants = activity["max_participants"]
        
        # Fill the activity by signing up new participants
        new_emails = [f"filler{i}@student.uva.nl" for i in range(max_participants - current_count)]
        for email in new_emails:
            client.post(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Try to sign up one more (should fail)
        overflow_email = "overflow@student.uva.nl"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": overflow_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
