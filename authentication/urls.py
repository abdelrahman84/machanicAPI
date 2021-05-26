from django.conf.urls import url
from django.urls.conf import path

from authentication.views import users_list
from authentication import views


urlpatterns = [
    url(r'^api/users$', views.users_list)
]
