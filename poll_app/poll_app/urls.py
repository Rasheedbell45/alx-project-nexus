from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView

# Swagger / ReDoc schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Polling API",
        default_version="v1",
        description="API documentation for the Polling system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/polls/", include("polls.urls")),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/schema.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("api/schema.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
]
