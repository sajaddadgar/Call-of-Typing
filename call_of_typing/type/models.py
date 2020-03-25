from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_point = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def update_profile(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        instance.profile.save()

    def __str__(self):
        return self.user.username


class OrdinaryText(models.Model):
    pass
