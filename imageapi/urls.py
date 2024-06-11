from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('api/', include('imageapp.urls')),
    path('admin/', admin.site.urls),
]
