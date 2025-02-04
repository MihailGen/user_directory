# Users_Directory/urls.py
from django.contrib import admin
from django.urls import include
from django.urls import path
from Users import views, urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(urls)),
]
