from django.urls import path
from .views import CustomTokenObtainPairView, register_user, get_me

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register', register_user, name='register_user'),
    path('me', get_me, name='get_me'),
]
