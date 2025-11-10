import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserProfileModel:
    """Test cases for the UserProfile model."""
    
    def test_userprofile_get_full_name_returns_first_and_last_name(self):
        """Test that get_full_name() returns first_name and last_name."""
        UserProfile = get_user_model()
        
        user = UserProfile.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        
        assert user.get_full_name() == "John Doe"
    
    def test_userprofile_authenticates_with_email(self):
        """Test that authentication works using email instead of username."""
        UserProfile = get_user_model()
        
        user = UserProfile.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        
        # Verify we can authenticate with email
        from django.contrib.auth import authenticate
        auth_user = authenticate(email="test@example.com", password="testpass123")
        assert auth_user is not None
        assert auth_user == user

