from drf_yasg import openapi

api_info = openapi.Info(
    title="Otzovik API",
    default_version='v1',
    description="Have a nice experience)",
    terms_of_service="https://www.example.com/policies/terms/",
    contact=openapi.Contact(email="contact@example.com"),
    license=openapi.License(name="BSD License"),
)
