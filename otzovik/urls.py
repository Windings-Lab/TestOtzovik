from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from users.views.authentication_views import index

from .api_info import api_info

schema_view = get_schema_view(
    api_info,
    url='https://testotzovik.onrender.com/swagger/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls.urls')),
    path('', include('courses.urls.urls')),
    path('api/v1/', include('users.urls.api_urls')),
    path('api/v1/', include('courses.urls.api_urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', index)
]


if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
