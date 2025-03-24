from io import StringIO

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command


class ProfilesTest(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_settings(self):
        self.assertIn("interview.profiles", settings.INSTALLED_APPS)
        self.assertEqual(settings.AUTH_USER_MODEL, "profiles.UserProfile")

    def test_user_model_attributes(self):

        # Check if the required attributes are present in the user model class
        self.assertTrue(hasattr(self.user_model, "username"))
        self.assertTrue(hasattr(self.user_model, "email"))
        self.assertTrue(hasattr(self.user_model, "password"))
        self.assertTrue(hasattr(self.user_model, "first_name"))
        self.assertTrue(hasattr(self.user_model, "last_name"))
        self.assertTrue(hasattr(self.user_model, "date_joined"))
        self.assertTrue(hasattr(self.user_model, "last_login"))
        self.assertTrue(hasattr(self.user_model, "is_staff"))
        self.assertTrue(hasattr(self.user_model, "is_superuser"))
        self.assertTrue(hasattr(self.user_model, "is_admin"))
        self.assertTrue(hasattr(self.user_model, "is_active"))

        self.assertTrue(hasattr(self.user_model, "USERNAME_FIELD"))
        self.assertEqual(self.user_model.USERNAME_FIELD, "email")

        self.assertTrue(hasattr(self.user_model, "get_full_name"))
        self.assertTrue(hasattr(self.user_model, "get_username"))
        self.assertTrue(hasattr(self.user_model, "is_authenticated"))

        self.assertTrue(getattr(self.user_model, "avatar").field.type == "ImageField")

        self.assertTrue(hasattr(self.user_model, "objects"))
        self.assertTrue(getattr(self.user_model, "objects").__class__.__name__ == "UserManager")

    def test_model_instance(self):
        user_model = get_user_model()
        self.assertEqual(user_model.objects.count(), 0)
        user = user_model.objects.create_user(
            username="model_test",
            email="model_test@example.com",
            password="model_test_password",
            first_name="Model",
            last_name="Test",
        )
        self.assertEqual(user_model.objects.count(), 1)
        self.assertTrue(user.check_password("model_test_password"))
        self.assertFalse(user.check_password("wrong"))
        self.assertEqual(user.get_full_name(), "Model Test")
        self.assertEqual(user.USERNAME_FIELD, "email")

    def test_model_manager(self):
        user_model = get_user_model()
        self.assertTrue(hasattr(user_model.objects, "create_user"))
        self.assertTrue(hasattr(user_model.objects, "create_superuser"))

    def test_createsuperuser(self):
        out = StringIO()

        user_model = get_user_model()
        email = "test@example.com"
        password = "testpassword"

        call_command(
            'createsuperuser',
            interactive=False,
            email=email,
            stdout=out,
            noinput=True,
        )

        # Set password manually since --noinput doesn't set it
        user = user_model.objects.get(email=email)
        user.set_password(password)
        user.save()

        self.assertTrue(user_model.objects.filter(email=email).exists())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
