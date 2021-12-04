from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.template.loader import get_template, render_to_string
from django.core import mail
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


# 3rd part

from authentication.models import User
from authentication.serializers import MyTokenObtainPairSerializer, UpdateNameSerializer, UserSerializer, VerifyTokenSerializer


@api_view(['POST', 'DELETE'])
@permission_classes([AllowAny])
def users_list(request):

    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()

            veirfy_email_template = get_template('verification_email.html').render(
                {'name': user_serializer.data['name'], 'verify_token': user_serializer.data['verify_token']})

            subject = 'Email verification'
            plain_message = render_to_string('verification_email.html', {
                                             'name': user_serializer.data['name'], 'verify_token': user_serializer.data['verify_token']})
            from_email = 'info@machinc.com'
            to = user_serializer.data['email']

            mail.send_mail(
                subject,
                plain_message,
                from_email,
                [to],
                html_message=veirfy_email_template,
                fail_silently=False
            )
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    user_data = JSONParser().parse(request)
    token_serializer = VerifyTokenSerializer(data=user_data)

    if token_serializer.is_valid():
        try:
            user = User.objects.get(verify_token=user_data['verify_token'])
            user_serializer = UserSerializer(user)

            user.password = make_password(user_data['password'])
            user.email_verified = True
            user.save()

        except User.DoesNotExist:
            return JsonResponse({'error': 'user doesn`t exist'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)

    return JsonResponse(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getUsers(request):
    if request.user.is_staff:
        users = User.objects.all()

        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

    return JsonResponse({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def updateUser(request):
    user =request.user
    user_name = JSONParser().parse(request)
    user_name_serailizer = UpdateNameSerializer(data=user_name)

    if user_name_serailizer.is_valid():
        try:
            user.name = user_name['name']
            user.save()
        except User.DoesNotExist:
            return JsonResponse({'error': 'user doesn`t exist'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'updated_name': user.name}, status=status.HTTP_200_OK)

    return JsonResponse(user_name_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)
