
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produto.urls')),
    path('perfil/', include('perfil.urls')),
    path('pedido', include('pedido.urls')),

    path("debug/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
