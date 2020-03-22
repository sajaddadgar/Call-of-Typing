from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    max_point =models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class OrdinaryText(models.Model):
    pass

