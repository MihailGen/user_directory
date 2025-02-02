# Users_Directory/urls.py
from django.contrib import admin
from django.urls import path, include

from Users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base),
    path('api-auth/', include('rest_framework.urls')),
]
