import json
from django.test import TestCase
from rest_framework import status

# application
from .models import User
from authentication.serializers import UserSerializer


# Create your tests here.


class AuthenticationViewSetTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            first_name='Abdelrahman',
            last_name='Ahmed',
            username='abdu',
            email='abdelrahman.farag84@gmail.com',
            phone='01069225161'
        )

    # Test users index
    def test_all_users(self):
        response = self.client.get('/api/users', format="json")

        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps(users_serializer.data))
