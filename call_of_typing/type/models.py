from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_point = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    image = models.ImageField(blank=True, null=True)

    @receiver(post_save, sender=User)
    def update_profile(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.create(user=instance)

        instance.profile.save()

    def __str__(self):
        return self.user.username


class OrdinaryText(models.Model):
    content = models.CharField(max_length=1000, null=True)
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content




