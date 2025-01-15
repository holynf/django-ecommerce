from django.contrib.auth.models import AbstractBaseUser 
from django.db import models

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username