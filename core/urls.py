# core/urls.py
from django.contrib import admin
from django.urls import include, path, reverse_lazy

from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# def custom_404_view(*args):
#     return redirect(reverse_lazy('home'))

# handler404 = 'core.urls.custom_404_view'



schema_view = get_schema_view(
    openapi.Info(
        title="whatsApp API's",
        default_version='v1',
        description="whatsApp API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mallamsiddiq@gmail.com"),
        license=openapi.License(name="Nutfa's licence"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ...
    # Include DRF-Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('', include('chat.controller.urls')),
    path('auth/', include('authapp.urls')),  # Include authentication app URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
