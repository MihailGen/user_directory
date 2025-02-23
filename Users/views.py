import logging
from datetime import time

# ---------------------------
from asgiref.sync import sync_to_async
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
# ---------------------------
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from Users.models import User
from Users.serializers import RegisterSerializer
from .forms import RegistrationForm

#----------------- Prometheus encapsulate --------------------------

app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['users', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['users', 'endpoint'])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        REQUEST_COUNT.labels(app_name='users', endpoint=endpoint).inc()
        with REQUEST_LATENCY.labels(app_name='users', endpoint=endpoint).time():
            response = await call_next(request)
        return response


app.add_middleware(MetricsMiddleware)


@app.get('/metrics')
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.get('/compute')
def compute():
    time.sleep(2)
    return {"message": "Completed a complex computation"}


@app.get('/heavy_compute')
def heavy_compute():
    for t in range(150):
        time.sleep(2)
    return {"message": "Completed a series of computations"}

# --------------- Prometheus End ---------------------------------


logging.config.fileConfig('config.ini')
logger = logging.getLogger(__name__)


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


# Альтернативный эндпоинт для регистрации пользователя
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


def home(request):
    logger.debug("Отладка из функции создания домашней странички")
    logger.info('Вход пользователя ' + request.user.username + ' на домашнюю страничку')
    try:
        people = User.objects.all()  # Получение списка пользователей
        return render(request, 'users/home.html', {'people': people})
    except Exception as e:
        logger.error(f"Произошла ошибка создания домашней страницы {e}")


@require_POST
async def add_person(request):
    logger.debug("Отладка из представления add_person")
    logger.info('Добавление нового пользователя')
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        await sync_to_async(User.objects.create)(username=username, email=email, phone=phone, address=address,
                                                 birthdate=birthdate,
                                                 gender=gender)
        return redirect('home')
    except Exception as e:
        logger.error(f"Произошла ошибка добавления нового пользователя {e}")


@require_POST
def delete_person(request, person_id):
    logger.debug("Отладка из представления add_person")
    logger.info('Удаление пользователя')
    try:
        person = get_object_or_404(User, pk=person_id)
        person.delete()
        return redirect('home')
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении пользователя {e}")
