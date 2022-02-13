from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .manager import *
# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=14,unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
