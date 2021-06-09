from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.template.loader import get_template, render_to_string
from django.core import mail
from django.contrib.auth.hashers import make_password

from authentication.models import User
from authentication.serializers import UserSerializer, VerifyTokenSerializer


@api_view(['GET', 'POST', 'DELETE'])
def users_list(request):
	if request.method == 'GET':
		users = User.objects.all()

		users_serializer = UserSerializer(users, many=True)
		return JsonResponse(users_serializer.data, safe=False)

	if request.method == 'POST':
		user_data = JSONParser().parse(request)
		user_serializer = UserSerializer(data=user_data)
		if user_serializer.is_valid():
			user_serializer.save()

			veirfy_email_template = get_template('verification_email.html').render({'first_name' : user_serializer.data['first_name'], 'token': user_serializer.data['token']})

			subject = 'Email verification'
			plain_message = render_to_string('verification_email.html', {'first_name' : user_serializer.data['first_name'], 'token': user_serializer.data['token']})
			from_email = 'info@machinc.com'
			to = user_serializer.data['email']

			mail.send_mail(
				subject,
				plain_message,
				from_email,
				[to],
				html_message = veirfy_email_template,
				fail_silently=False
			)
			return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_token(request):
	users_data = JSONParser().parse(request)
	token_serializer = VerifyTokenSerializer(data=users_data)

	if token_serializer.is_valid():
		try:
			user = User.objects.get(token=users_data['token'])
			user_serializer = UserSerializer(user)

			user.password = make_password(user_serializer.data['password'])
			user.save()

		except User.DoesNotExist: 
			return JsonResponse({'error': 'user doesn`t exist'}, status=status.HTTP_400_BAD_REQUEST) 
		return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

	return JsonResponse(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

