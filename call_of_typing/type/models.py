from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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

    def get_text_rank(self):
        scores = list(Profile.objects.all().values_list('text_score', flat=True))
        scores = sorted(scores, reverse=True)
        # scores = sorted(set(scores), reverse=True)
        return scores.index(self.text_score) + 1

    def get_song_rank(self):
        scores = list(Profile.objects.all().values_list('song_score', flat=True))
        scores = sorted(scores, reverse=True)
        # scores = sorted(set(scores), reverse=True)
        return scores.index(self.song_score) + 1


class GroupMembers(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_text_score = models.IntegerField(default=0)
    user_song_score = models.IntegerField(default=0)

    def is_admin(self):
        ga = GroupAdmin.objects.get(group=self.group.id)
        if ga.admin.id == self.user.id:
            return True
        return False


class GroupAdmin(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    group_text_score = models.IntegerField(default=0)
    group_song_score = models.IntegerField(default=0)


class GroupTextSets(models.Model):
    content = models.CharField(max_length=1000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class OrdinaryText(models.Model):
    content = models.CharField(max_length=1000, null=True,)
    creation_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Track(models.Model):
    track_title = models.CharField(max_length=500)
    Artist_name = models.CharField(max_length=500, null=True, blank=True)
    song = models.FileField(upload_to='songs/files/', null=True)

    def __str__(self):
        return self.track_title


