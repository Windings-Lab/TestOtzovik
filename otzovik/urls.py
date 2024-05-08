from django.contrib import admin
from django.urls import include, path

from users.views.authentication_views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('', include('users.urls')),
    path('', include('courses.urls')),
    path('', index)
]
