from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cctv/admin/', admin.site.urls),
    path('cctv/api/auth/', include('users.urls_auth')),
    path('cctv/api/users/', include('users.urls')),
    path('cctv/api/cameras/', include('cctv.urls')),
    path('cctv/api/tickets/', include('maintenance.urls')),
    path('cctv/api/routes/', include('routes.urls')),
    path('cctv/api/reports/', include('reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

