
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
#reverse for getting the url
#user as the app
#create as the end point
TOKEN_URL = reverse('user:token')

#helper function to create a user for testing
def create_user(**params):
    # **param allows us to add any params
    """"Create and retirn a user"""
    return get_user_model().objects.create_user(**params)

class PublicUserTests(TestCase):

    def setUp(self):
        print("setup")
        self.client = APIClient()
        #create client for testing

    def test_create_user_success(self):
        print("test_create_user_success")
        #the payload that need to add
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test name',
        }
        #makes a http post request to the below url with the payload
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        #after the post action is done,
        #we reterive the object from the database and get the user from the email
        #and check the password if it's the same to what we created above
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password',res.data)

    def test_user_with_email_exists_error(self):

        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email':'test@example.com',
            'password':'pw',
            'name':'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        #and since the password is too short, failed to create that user
        #we expected the user doesn't exist
        #so we check and make sure
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)
        #generate the payload
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        #post the token onto url
        res = self.client.post(TOKEN_URL, payload)
        #check the res include "token"
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')
        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

