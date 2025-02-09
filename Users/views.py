from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
#---------------------------
from rest_framework import generics
from Users.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from Users.serializers import RegisterSerializer
#---------------------------

def base(request):
    return render(request, "users/base.html")



# Эндпоинт для регистрации пользователя с использование Django - форм
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


# Альтернативный эндпоинт для регистрации пользователя через сериалайзер
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

