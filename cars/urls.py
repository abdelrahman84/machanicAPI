from django.conf.urls import url

from cars import views

app_name = 'cars'

urlpatterns = [
    url(r'^api/car/create_car', views.createCar),
]