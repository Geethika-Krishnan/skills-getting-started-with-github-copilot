"""Tests for the Mergington High School API"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app

client = TestClient(app)


class TestActivitiesEndpoint:
    """Tests for the /activities endpoint"""

    def test_get_activities_returns_200(self):
        """Test that GET /activities returns a 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self):
        """Test that GET /activities returns a dictionary"""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_chess_club(self):
        """Test that activities include Chess Club"""
        response = client.get("/activities")
        activities = response.json()
        assert "Chess Club" in activities

    def test_activity_has_required_fields(self):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data


class TestSignupEndpoint:
    """Tests for the /activities/{activity_name}/signup endpoint"""

    def test_signup_returns_200(self):
        """Test that signing up returns a 200 status code"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200

    def test_signup_returns_success_message(self):
        """Test that signup returns a success message"""
        response = client.post(
            "/activities/Art%20Studio/signup?email=test2@mergington.edu"
        )
        assert response.status_code == 200
        assert "message" in response.json()

    def test_signup_with_invalid_activity_returns_404(self):
        """Test that signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/Fake%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404

    def test_signup_duplicate_returns_400(self):
        """Test that signing up twice for same activity returns 400"""
        email = "duplicate@mergington.edu"
        # First signup should succeed
        response1 = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        assert response2.status_code == 400


class TestUnregisterEndpoint:
    """Tests for the /activities/{activity_name}/unregister endpoint"""

    def test_unregister_returns_200(self):
        """Test that unregistering returns a 200 status code"""
        email = "unregister@mergington.edu"
        # First sign up
        client.post(f"/activities/Tennis%20Club/signup?email={email}")
        
        # Then unregister
        response = client.delete(
            f"/activities/Tennis%20Club/unregister?email={email}"
        )
        assert response.status_code == 200

    def test_unregister_with_invalid_activity_returns_404(self):
        """Test that unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Fake%20Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404

    def test_unregister_non_registered_user_returns_400(self):
        """Test that unregistering a non-registered user returns 400"""
        response = client.delete(
            "/activities/Debate%20Team/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
