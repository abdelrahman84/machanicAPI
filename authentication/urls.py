from django.conf.urls import url
from django.urls.conf import path

# 3rd-pard

from authentication.views import MyTokenObtainPairView
from authentication import views

app_name = 'authentication'

urlpatterns = [
	url(r'^api/users$', views.users_list),
	url(r'^api/verify_token', views.verify_token),
	url(r'^api/all_users', views.getUsers),
	url(r'^api/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
	url(r'^api/updateUser', views.updateUser),
	url(r'^api/getUserData', views.getUserData),

]
