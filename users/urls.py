from django.urls import path

from .views.authentication_views import (LinkedInCallbackView, home, login,
                                         logout)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('linkedin/callback/', LinkedInCallbackView.as_view(), name='linkedin_callback'),
    path('home/', home, name='home'),

]
