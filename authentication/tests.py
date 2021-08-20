import json
from django.test import TestCase
from rest_framework import status

# application
from .models import User


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

	# Test creating user
	def test_creating_user(self):
		response = self.client.post('/api/users', json.dumps({
			"first_name": "abdu",
			"last_name":"bashaa",
			"username": "abdu1",
			"email": "abdelrahman.farag114@gmail.com",
			"phone": "01069225161"}), format="json", content_type="application/json") 

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	# Test creating user
	def test_verify_email(self):
		response = self.client.post('/api/users', json.dumps({
			"first_name": "abdu",
			"last_name":"bashaa",
			"username": "abdu1",
			"email": "abdelrahman.farag114@gmail.com",
			"phone": "01069225161"}), format="json", content_type="application/json") 

		verify_token = json.loads(response.content.decode('utf-8'))['verify_token']

		verify_response = self.client.post('/api/verify_token', json.dumps({
			"verify_token": verify_token,
				"password": "1234bB1$"}), format="json", content_type="application/json") 

		self.assertEqual(verify_response.status_code, status.HTTP_200_OK)	


   # Test login user
	def test_verify_email(self):
		response = self.client.post('/api/users', json.dumps({
			"first_name": "abdu",
			"last_name":"bashaa",
			"username": "abdu1",
			"email": "abdelrahman.farag114@gmail.com",
			"phone": "01069225161"}), format="json", content_type="application/json") 

		verify_token = json.loads(response.content.decode('utf-8'))['verify_token']

		verify_response = self.client.post('/api/verify_token', json.dumps({
			"verify_token": verify_token,
				"password": "1234bB1$"}), format="json", content_type="application/json") 

		self.assertEqual(verify_response.status_code, status.HTTP_200_OK)		



