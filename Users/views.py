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
from asyncio import sleep
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
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


def home(request):
    people = User.objects.all()  # Получение списка пользователей
    return render(request, 'users/home.html', {'people': people})


@require_POST
async def add_person(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    birthdate = request.POST.get('birthdate')
    gender = request.POST.get('gender')
    await sync_to_async(User.objects.create)(username=username, email=email,phone=phone, address= address, birthdate=birthdate,
                                             gender=gender)
    return redirect('home')


@require_POST
def delete_person(request, person_id):
    person = get_object_or_404(User, pk=person_id)
    person.delete()
    return redirect('home')
