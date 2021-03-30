from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('webmaster_admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('', include('home.urls', namespace='home')),
    path('staff/', include('staff.urls', namespace='staff')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    #url(r'^webmaster_admin/', admin.site.urls),
    #url(r'^account/', include('account.urls', namespace='account')),
    #url('^', include('home.urls', namespace='home')),
    #url(r'^staff/', include('staff.urls', namespace='staff')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
