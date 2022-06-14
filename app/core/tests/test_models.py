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
        print("=== run test create user ===")
        user = get_user_model().objects.create_user(
            email = email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normailized(self):
        print("=== run test user email normalize===")
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sampl123")
            self.assertEqual(user.email, expected)