# core/urls.py
from django.contrib import admin
from django.urls import include, path
from django.urls import reverse_lazy

from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# def custom_404_view(*args):
#     return redirect(reverse_lazy('home'))

# handler404 = 'core.urls.custom_404_view'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.controller.urls')),
    path('auth/', include('authapp.urls')),  # Include authentication app URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
