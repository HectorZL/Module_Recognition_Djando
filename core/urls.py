from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from accounts.views import home_view

urlpatterns = [
    # Páginas principales
    path('', home_view, name='home'),
    
    # URLs de autenticación y cuentas
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth views
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    
    # URLs de pacientes (si es necesario)
    path('patients/', include('patients.urls')),
    
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # Redirección de favicon.ico para evitar errores
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
