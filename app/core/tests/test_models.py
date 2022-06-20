"""Test for models"""

from django.test import TestCase
#get_user_model function from default django user model sets
from django.contrib.auth import get_user_model

#Recipe====
from decimal import Decimal
from core import models

#tags=====
def create_test_user(email='user@example', password='test123'):
    """create and return a test user"""
    return get_user_model().objects.create_user(email,password)

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
            ['test4@example.COM','test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sampl123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_will_raise_error(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("","test123")

    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(
            email="testsuperuser@example.com",
            password="test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        "Test creating a tag is succesful?"
        user = create_test_user()
        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)