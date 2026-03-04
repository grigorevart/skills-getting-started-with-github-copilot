"""
Unit tests for activity management business logic using AAA (Arrange-Act-Assert) pattern.

These tests verify the core data structures and validation logic for activities:
- Activity data structure integrity
- Participant management
- Capacity constraints
- Input validation
"""

import pytest
from src.app import activities


class TestActivityDataStructure:
    """Tests for the activity data structure and initialization."""
    
    def test_all_activities_exist(self):
        """
        Verify all 9 expected activities are initialized in the system.
        
        AAA Pattern:
        - Arrange: Activities are already loaded
        - Act: Count the activities
        - Assert: Verify count equals 9
        """
        # Arrange
        # (activities dict is already initialized from app)
        
        # Act
        activity_count = len(activities)
        
        # Assert
        assert activity_count == 9
    
    def test_each_activity_has_required_fields(self):
        """
        Verify that every activity has all required fields.
        
        AAA Pattern:
        - Arrange: Activities are loaded
        - Act: Check each activity for required fields
        - Assert: All activities have description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        activities_by_field = {
            name: all(field in activity for field in required_fields)
            for name, activity in activities.items()
        }
        
        # Assert
        assert all(activities_by_field.values()), "Not all activities have required fields"
    
    def test_activities_have_max_participants_set(self):
        """
        Verify that each activity has a valid max_participants value.
        
        AAA Pattern:
        - Arrange: Activities are loaded
        - Act: Extract max_participants values
        - Assert: All values are positive integers
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        max_participants = [
            activity["max_participants"]
            for activity in activities.values()
        ]
        
        # Assert
        assert all(isinstance(mp, int) and mp > 0 for mp in max_participants)
        assert len(max_participants) == 9
    
    def test_activities_have_participants_list(self):
        """
        Verify that each activity has a participants list initialized.
        
        AAA Pattern:
        - Arrange: Activities loaded
        - Act: Check participants field type
        - Assert: All are lists with valid emails
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        participants_lists = [
            activity["participants"]
            for activity in activities.values()
        ]
        
        # Assert
        assert all(isinstance(p_list, list) for p_list in participants_lists)
        assert all(isinstance(email, str) and "@" in email for plist in participants_lists for email in plist)


class TestParticipantManagement:
    """Tests for adding and removing participants from activities."""
    
    def test_add_participant_increases_count(self, reset_activities):
        """
        Verify that adding a participant increases the count.
        
        AAA Pattern:
        - Arrange: Get initial participant count for Chess Club
        - Act: Add a new participant
        - Assert: Verify count increased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        initial_count = len(activities[activity_name]["participants"])
        new_email = "new.student@mergington.edu"
        
        # Act
        activities[activity_name]["participants"].append(new_email)
        new_count = len(activities[activity_name]["participants"])
        
        # Assert
        assert new_count == initial_count + 1
    
    def test_remove_participant_decreases_count(self, reset_activities):
        """
        Verify that removing a participant decreases the count.
        
        AAA Pattern:
        - Arrange: Get initial participant count and existing email
        - Act: Remove an existing participant
        - Assert: Verify count decreased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        activities[activity_name]["participants"].remove(email_to_remove)
        new_count = len(activities[activity_name]["participants"])
        
        # Assert
        assert new_count == initial_count - 1
    
    def test_participant_email_stored_correctly(self, reset_activities):
        """
        Verify that participant emails are stored exactly as provided.
        
        AAA Pattern:
        - Arrange: Create a specific email
        - Act: Add email to activity
        - Assert: Verify stored email matches exactly
        """
        # Arrange
        activity_name = "Programming Class"
        test_email = "test.exact@mergington.edu"
        
        # Act
        activities[activity_name]["participants"].append(test_email)
        participants = activities[activity_name]["participants"]
        
        # Assert
        assert test_email in participants
        assert participants[-1] == test_email


class TestActivityValidation:
    """Tests for validation and constraints in activity management."""
    
    def test_chess_club_starts_with_two_participants(self):
        """
        Verify the initial state of Chess Club.
        
        AAA Pattern:
        - Arrange: Access Chess Club activity
        - Act: Get participants list
        - Assert: Verify exactly 2 initial participants
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        chess_club = activities["Chess Club"]
        participants = chess_club["participants"]
        
        # Assert
        assert len(participants) == 2
        assert "michael@mergington.edu" in participants
        assert "daniel@mergington.edu" in participants
    
    def test_basketball_team_max_capacity(self):
        """
        Verify Basketball Team capacity constraint.
        
        AAA Pattern:
        - Arrange: Get Basketball Team activity
        - Act: Extract max_participants
        - Assert: Verify capacity is 15
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        basketball = activities["Basketball Team"]
        max_cap = basketball["max_participants"]
        
        # Assert
        assert max_cap == 15
    
    def test_tennis_club_max_capacity(self):
        """
        Verify Tennis Club capacity constraint.
        
        AAA Pattern:
        - Arrange: Get Tennis Club activity
        - Act: Extract max_participants
        - Assert: Verify capacity is 10
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        tennis_club = activities["Tennis Club"]
        max_cap = tennis_club["max_participants"]
        
        # Assert
        assert max_cap == 10
    
    def test_activity_description_not_empty(self):
        """
        Verify all activities have non-empty descriptions.
        
        AAA Pattern:
        - Arrange: Load activities
        - Act: Gather all descriptions
        - Assert: All descriptions are non-empty strings
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        descriptions = [
            activity["description"]
            for activity in activities.values()
        ]
        
        # Assert
        assert all(desc and isinstance(desc, str) and len(desc) > 0 for desc in descriptions)
    
    def test_activity_schedule_format(self):
        """
        Verify all activities have properly formatted schedules.
        
        AAA Pattern:
        - Arrange: Load activities
        - Act: Check schedule fields
        - Assert: All schedules are non-empty strings
        """
        # Arrange
        # (activities dict is ready)
        
        # Act
        schedules = [
            activity["schedule"]
            for activity in activities.values()
        ]
        
        # Assert
        assert all(
            isinstance(schedule, str) and len(schedule) > 0
            for schedule in schedules
        )
        # Verify schedules mention times
        assert all(any(digit in schedule for digit in "0123456789") for schedule in schedules)


class TestActivityLookup:
    """Tests for activity lookup and retrieval logic."""
    
    def test_lookup_valid_activity_succeeds(self):
        """
        Verify that valid activity names can be looked up.
        
        AAA Pattern:
        - Arrange: Define a valid activity name
        - Act: Look up activity in activities dict
        - Assert: Activity exists and is accessible
        """
        # Arrange
        activity_name = "Science Olympiad"
        
        # Act
        activity_exists = activity_name in activities
        activity = activities.get(activity_name) if activity_exists else None
        
        # Assert
        assert activity_exists
        assert activity is not None
        assert activity["description"] == "Compete in science competitions and experiments"
    
    def test_lookup_invalid_activity_returns_none(self):
        """
        Verify that invalid activity names are not found.
        
        AAA Pattern:
        - Arrange: Define an invalid activity name
        - Act: Look up activity in activities dict
        - Assert: Activity does not exist
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        
        # Act
        activity_exists = activity_name in activities
        
        # Assert
        assert not activity_exists
    
    def test_all_nine_activities_are_accessible_by_name(self):
        """
        Verify that all 9 activities can be looked up by their names.
        
        AAA Pattern:
        - Arrange: Get all activity names
        - Act: Look up each name
        - Assert: All exist in the activities dict
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Club",
            "Science Olympiad"
        ]
        
        # Act
        found_activities = [name for name in expected_activities if name in activities]
        
        # Assert
        assert len(found_activities) == 9
        assert found_activities == expected_activities
