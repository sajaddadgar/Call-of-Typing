from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, blank=True, null=True, default=None)
    text_max_point = models.IntegerField(default=0)
    text_score = models.IntegerField(default=0, null=True, blank=True)
    song_max_point = models.IntegerField(default=0, null=True, blank=True)
    song_score = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

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


class Track(models.Model):
    track_title = models.CharField(max_length=500)
    Artist_name = models.CharField(max_length=500, null=True, blank=True)
    song = models.FileField(upload_to='songs/files/')

    def __str__(self):
        return self.track_title
