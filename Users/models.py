from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, username=None, email=None, password=None, phone=None, address=None, birthdate=None,
                    gender=None, **extra_fields):
        # def create_user(self,  email=None, password=None, phone=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        # user = self.model(username=username, **extra_fields)

        user.username = username
        user.phone = phone
        user.address = address
        user.password = make_password(password)
        user.birthdate = birthdate
        user.gender = gender
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, phone=None, address=None, birthdate=None,
                         gender=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, phone, birthdate, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    # username = None
    username = models.CharField(max_length=120, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField(lank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
