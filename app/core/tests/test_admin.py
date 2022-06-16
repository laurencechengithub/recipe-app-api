from http import client
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Tests for Django admin."""
    #the test name for admin are not the same as from model starting as "test"
    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="adminTest@example.com",
            password="adminTest123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="userTest@example.com",
            password="userTest123",
            name="Test user",
        )

    def test_users_lists(self):
        """test that users are on the page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """"Test whether the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        #http://localhost:8000/admin/core/user/1/change/ 上敘網址
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
        #makes sure the cliet gets/load the page succesful with http:200

    def test_create_user_page(self):
        """"Test the create user page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)