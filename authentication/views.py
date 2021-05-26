from django.http.response import JsonResponse
from authentication.serializers import UserSerializer
from rest_framework.decorators import api_view

from authentication.models import User


@api_view(['GET', 'POST', 'DELETE'])
def users_list(request):
    users = User.objects.all()

    users_serializer = UserSerializer(users, many=True)
    return JsonResponse(users_serializer.data, safe=False)
