from django.conf.urls import url
from django.urls.conf import path
from rest_framework_simplejwt.views import TokenObtainPairView

# 3rd-pard

from authentication.views import users_list
from authentication import views

app_name = 'authentication'

urlpatterns = [
	url(r'^api/users$', views.users_list),
	url(r'^api/verify_token', views.verify_token),
	url(r'^api/all_users', views.getUsers),
	url(r'^api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
