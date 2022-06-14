"""Test for models"""

from django.test import TestCase
#get_user_model function from default django user model sets
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        "Test creating a user with an email"
        email = "test@example.com"
        password = "test123"
        #below calls the usermodel.objects and creates one user pass in the email and pssd
        user = get_user_model().objects.create_user(
            email = email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
