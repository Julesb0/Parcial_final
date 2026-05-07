from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from proyectos_julio_william_diego_mike.views import InicioView

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('admin/', admin.site.urls),

    path(
        'cuentas/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'cuentas/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('proyectos/', include('proyectos_julio_william_diego_mike.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
