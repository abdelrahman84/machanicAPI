import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class CarViewSetTestCase(TestCase):

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

    def test_create_car(self):

        user_access_token = self.get_user_token_helper()

        url = '/api/car/create_car'

        client = user_access_token['client']

        create_care_response = client.post(url, json.dumps({
            "name": "new car",
            "model": 'chevrolet',
            'manufacturing_date': 2008,
            'total_distance': 260.15,
        }), content_type="application/json", safe=False)

        # assert response
        self.assertEqual(create_care_response.status_code,
                         status.HTTP_201_CREATED)
