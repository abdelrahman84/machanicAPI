import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# application
from .models import User


# Create your tests here.


class AuthenticationViewSetTestCase(TestCase):

    user_password = "1234bB1$"

    def verify_email_helper(self):

        user = {
            "name": "abdu",
            "email": "abdelrahman.farag114@gmail.com",
            "phone": "01069225161"}
        response = self.client.post(
            '/api/users', json.dumps(user), format="json", content_type="application/json")

        verify_token = json.loads(
            response.content.decode('utf-8'))['verify_token']

        verify_response = self.client.post('/api/verify_token', json.dumps({
            "verify_token": verify_token,
            "password": self.user_password}), format="json", content_type="application/json")

        return {'verify_response': verify_response, 'user': user}

    def get_user_token_helper(self):

        verify_response = self.verify_email_helper()

        # get user object from verify_email_helper
        user = verify_response['user']

        # login with user.email, and user.password
        login_response = self.client.post('/api/login', json.dumps({
            "email": user['email'],
            "password": self.user_password}), format="json", content_type="application/json")

        access_token = login_response.data['access']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        return {'client': client, 'user': user}

    def setUp(self):
        User.objects.create(
            name='Abdelrahman',
            email='abdelrahman.farag84@gmail.com',
            phone='01069225161'
        )

    # Test creating user
    def test_creating_user(self):
        response = self.client.post('/api/users', json.dumps({
            "name": "abdu",
            "email": "abdelrahman.farag114@gmail.com",
            "phone": "01069225161"}), format="json", content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test verify email
    def test_verify_email(self):

        verify_response = self.verify_email_helper()

        self.assertEqual(
            verify_response['verify_response'].status_code, status.HTTP_200_OK)

    # Test login user
    def test_login(self):
        verify_response = self.verify_email_helper()

        # get user object from verify_email_helper
        user = verify_response['user']

        # login with user.email, and user.password
        login_response = self.client.post('/api/login', json.dumps({
            "email": user['email'],
            "password": self.user_password}), format="json", content_type="application/json")

        # assert result status code is 200, response has access, refresh tokens, and user object
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(login_response.data['refresh'])
        self.assertIsNotNone(login_response.data['access'])
        self.assertIsNotNone(login_response.data['user'])

   # Test update name

    def test_update_name(self):

        user_access_token = self.get_user_token_helper()

        url = '/api/updateUser'

        client = user_access_token['client']

        update_name_response = client.put(url, json.dumps({
            "name": 'new name'}), content_type="application/json", safe=False)

        jsonResponse = update_name_response.json()

        # assert response
        self.assertEqual(update_name_response.status_code, status.HTTP_200_OK)
        self.assertEqual(jsonResponse['updated_name'], 'new name')
