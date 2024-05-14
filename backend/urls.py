from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userauth.urls')),
    path('api/main/', include('main.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
