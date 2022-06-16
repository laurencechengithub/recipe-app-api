
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
#reverse for getting the url
#user as the app
#create as the end point

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



