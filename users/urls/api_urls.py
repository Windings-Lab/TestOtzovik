from django.urls import path

from users.views.api_views import UserDetailApiView, UserListApiView

urlpatterns = [
    path('users/', UserListApiView.as_view(), name='api_users_detail'),
    path('users/<int:pk>', UserDetailApiView.as_view(), name='api_user_detail')

]
