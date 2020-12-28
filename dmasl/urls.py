from django.contrib import admin
# from django.urls import path, include
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^webmaster_admin/', admin.site.urls),

    url(r'^account/', include('account.urls', namespace='account')),
    url('^', include('home.urls', namespace='home')),
    url(r'^staff/', include('staff.urls', namespace='staff')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
