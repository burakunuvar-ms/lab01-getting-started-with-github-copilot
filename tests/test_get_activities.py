"""
Tests for GET endpoints using the AAA (Arrange-Act-Assert) pattern.

Covers:
  - GET / (root redirect)
  - GET /activities (retrieve all activities)
"""

import pytest


class TestRootRedirect:
    """Tests for the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html
        
        AAA Pattern:
          - Arrange: No setup needed, using the client fixture
          - Act: Make GET request to /
          - Assert: Verify 307 status code and location header
        """
        # Arrange
        # (implicit: client fixture)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Tests for the GET /activities endpoint."""
    
    def test_get_all_activities_returns_200(self, client):
        """
        Test that GET /activities returns 200 status
        
        AAA Pattern:
          - Arrange: No setup needed
          - Act: Make GET request to /activities
          - Assert: Verify 200 status
        """
        # Arrange
        # (implicit: client fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_all_activities_returns_correct_structure(self, client):
        """
        Test that GET /activities returns all 9 activities with required fields
        
        AAA Pattern:
          - Arrange: Define expected activity fields
          - Act: Make GET request to /activities
          - Assert: Verify all activities present with correct structure
        """
        # Arrange
        expected_activity_fields = {"description", "schedule", "max_participants", "participants"}
        expected_activity_count = 9
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == expected_activity_count
        
        # Verify each activity has required fields and participants is a list
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str), f"Activity name must be string, got {type(activity_name)}"
            assert isinstance(activity_data, dict), f"Activity data must be dict, got {type(activity_data)}"
            assert activity_data.keys() == expected_activity_fields, \
                f"Activity '{activity_name}' missing required fields"
            assert isinstance(activity_data["participants"], list), \
                f"Participants must be list, got {type(activity_data['participants'])}"
    
    def test_get_activities_participants_initially_populated(self, client):
        """
        Test that initial activities have participants pre-populated
        
        AAA Pattern:
          - Arrange: Define expected initial participant counts
          - Act: Make GET request to /activities
          - Assert: Verify participant counts match expectations
        """
        # Arrange
        expected_participants = {
            "Cycling Club": 2,
            "Dutch Language Circle": 2,
            "Data Science Society": 2,
            "Swimming Team": 2,
            "Football Club": 2,
            "Photography Workshop": 2,
            "Theatre & Drama Club": 2,
            "Philosophy Discussion Group": 2,
            "Environmental Science Club": 2,
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, expected_count in expected_participants.items():
            actual_count = len(activities[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} has {actual_count} participants, expected {expected_count}"
