from django.urls import path
from .views import registration_view, RegisterView, home, add_person, delete_person
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', registration_view, name='register'),
    #path('register/', RegisterView.as_view(), name='register'), # альтернативный метод регистрации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', home, name='home'),
    path('add/', add_person, name='add_person'),
    path('delete/<int:person_id>/', delete_person, name='delete_person')
]