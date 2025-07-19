"""
URL configuration for ecommerce_clothes project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Custom admin site
    path('django-admin/', admin.site.urls),  # Default Django admin
    path('', include('store.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 