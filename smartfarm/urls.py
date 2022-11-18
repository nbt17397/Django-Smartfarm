from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('hatchery.urls')),
    path('admin/', admin.site.urls),
]


handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
