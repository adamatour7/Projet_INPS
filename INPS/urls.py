# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # L'URL pour l'administration de Django
    path('api/', include('mobile.urls')),  # Inclure les URLs de l'application INPS
]
