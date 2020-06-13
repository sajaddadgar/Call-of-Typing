from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models import Sum


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
        return scores.index(self.text_score) + 1

    def get_song_rank(self):
        scores = list(Profile.objects.all().values_list('song_score', flat=True))
        scores = sorted(scores, reverse=True)
        return scores.index(self.song_score) + 1

    def save_text_score(self, text_score):
        self.text_score += text_score
        if self.text_max_point < text_score:
            self.text_max_point = text_score
        self.save()

    def save_song_score(self, song_score):
        self.song_score += song_score
        if self.song_max_point < song_score:
            self.song_max_point = song_score
        self.save()


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

    def member_save_text_score(self, text_score):
        self.user_text_score += text_score
        self.save()

    def member_save_song_score(self, song_score):
        self.user_song_score += song_score
        self.save()

    def get_member_text_rank(self):
        text_scores = list(GroupMembers.objects.filter(group=self.group).values_list('user_text_score', flat=True))
        text_scores = sorted(text_scores, reverse=True)
        return text_scores.index(self.user_text_score) + 1

    def get_member_song_rank(self):
        song_scores = list(GroupMembers.objects.filter(group=self.group).values_list('user_song_score', flat=True))
        song_scores = sorted(song_scores, reverse=True)
        return song_scores.index(self.user_song_score) + 1


class GroupAdmin(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_group_text_rank(self):
        all_groups = list(GroupAdmin.objects.all())
        current_group_score = self.get_group_text_score()
        scores = sorted([x.get_group_text_score() for x in all_groups], reverse=True)
        return scores.index(current_group_score) + 1

    def get_group_text_score(self):
        return GroupMembers.objects.filter(group=self.group).aggregate(Sum('user_text_score'))['user_text_score__sum']

    def get_group_song_rank(self):
        all_groups = list(GroupAdmin.objects.all())
        current_group_score = self.get_group_song_score()
        scores = sorted([x.get_group_song_score() for x in all_groups], reverse=True)
        return scores.index(current_group_score) + 1

    def get_group_song_score(self):
        return GroupMembers.objects.filter(group=self.group).aggregate(Sum('user_song_score'))['user_song_score__sum']


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


