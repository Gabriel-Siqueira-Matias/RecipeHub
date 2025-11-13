from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from receitas.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('receitas/', include('receitas.urls')),
    path('usuarios/', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)