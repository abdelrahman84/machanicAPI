from django.http.response import JsonResponse
from authentication.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from authentication.models import User


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
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
