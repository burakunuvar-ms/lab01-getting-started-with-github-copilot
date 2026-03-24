"""
Tests for DELETE /activities/{activity_name}/signup endpoint using the AAA pattern.

Covers:
  - Successful unregister (200)
  - Activity not found (404)
  - Student not signed up (404)
"""

import pytest


class TestUnregisterSuccess:
    """Tests for successful unregister scenarios."""
    
    def test_unregister_removes_participant_and_returns_200(self, client):
        """
        Test that valid unregister removes email from participants and returns 200
        
        AAA Pattern:
          - Arrange: Get existing participant from activity
          - Act: Make DELETE request to /activities/{name}/signup
          - Assert: Verify 200 status and email removed from participants
        """
        # Arrange
        activity_name = "Swimming Team"
        activities_response = client.get("/activities")
        email_to_remove = activities_response.json()[activity_name]["participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email_to_remove in response.json()["message"]
        
        # Verify participant was removed by fetching activities
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email_to_remove not in participants
    
    def test_unregister_response_format(self, client):
        """
        Test that unregister response has correct message format
        
        AAA Pattern:
          - Arrange: Get existing participant
          - Act: Make DELETE request
          - Assert: Verify response JSON structure and message
        """
        # Arrange
        activity_name = "Football Club"
        activities_response = client.get("/activities")
        email = activities_response.json()[activity_name]["participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" == data["message"]


class TestUnregisterActivityNotFound:
    """Tests for unregister from non-existent activity."""
    
    def test_unregister_unknown_activity_returns_404(self, client):
        """
        Test that unregistering from non-existent activity returns 404
        
        AAA Pattern:
          - Arrange: Define fake activity name and email
          - Act: Make DELETE request to /activities/{fake_name}/signup
          - Assert: Verify 404 status and error detail
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@student.uva.nl"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterNotRegistered:
    """Tests for unregister when student is not signed up."""
    
    def test_unregister_not_signed_up_returns_404(self, client):
        """
        Test that unregistering someone not signed up returns 404
        
        AAA Pattern:
          - Arrange: Use email that was never signed up
          - Act: Make DELETE request
          - Assert: Verify 404 status and error message
        """
        # Arrange
        activity_name = "Theatre & Drama Club"
        email = "never_signed_up@student.uva.nl"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
    
    def test_unregister_twice_returns_404(self, client):
        """
        Test that unregistering the same person twice returns 404 on second attempt
        
        AAA Pattern:
          - Arrange: Get existing participant and unregister once
          - Act: Try to unregister the same person again
          - Assert: Verify 404 status on second unregister
        """
        # Arrange
        activity_name = "Philosophy Discussion Group"
        activities_response = client.get("/activities")
        email = activities_response.json()[activity_name]["participants"][0]
        
        # First unregister should succeed
        client.delete(f"/activities/{activity_name}/signup", params={"email": email})
        
        # Act: Try to unregister same person again
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
