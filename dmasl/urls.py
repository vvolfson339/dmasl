from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^account/', include('account.urls', namespace='account')),
    url('^', include('home.urls', namespace='home')),
    url(r'^staff/', include('staff.urls', namespace='staff')),
]
