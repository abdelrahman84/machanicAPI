from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from cars.serializers import CarSerializer

@api_view(['POST'])
def createCar(request):

    car_data = JSONParser().parse(request)
    car_serializer = CarSerializer(data=car_data)

    if car_serializer.is_valid():
        car_serializer.user = request.user.name;
        car_serializer.save();

        return JsonResponse(car_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


