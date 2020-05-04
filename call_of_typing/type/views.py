from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from .form import ProfileForm
from .form import SongForm
from .models import Profile, OrdinaryText, Track, GroupAdmin, GroupMembers
from passlib.hash import django_pbkdf2_sha256 as handler
from django.contrib.auth.models import User
from django.db import IntegrityError
from random import randint
from django.contrib.auth.models import Group
import re
from .song import *

# import soundcloud


# Get authenticated user: request.user
# Get profile of user: request.user.profile.max_point

# global variables
duration_ms = 0
lyrics = ""

word_per_min = 0
error_count = 0
word_count = 0
text_score = 0

song_score = 0


# # #


def home(request):
    return render(request, 'index.html')


def ranking(request):
    all_users = User.objects.filter(is_superuser=0)
    text_rank_array = sorted(all_users, key=lambda x: x.profile.text_score, reverse=True)[0:10]
    song_rank_array = sorted(all_users, key=lambda x: x.profile.song_score, reverse=True)[0:10]

    if text_rank_array[len(text_rank_array)-1].profile.text_score == 0:
        for i in range(len(text_rank_array)):
            if text_rank_array[i].profile.text_score == 0:
                text_rank_array = text_rank_array[0:i]
                break
    if song_rank_array[len(text_rank_array) - 1].profile.song_score == 0:
        for i in range(len(song_rank_array)):
            if song_rank_array[i].profile.song_score == 0:
                song_rank_array = song_rank_array[0:i]
                break

    stuff_for_front = {
        'text_rank_array': text_rank_array,
        'song_rank_array': song_rank_array
    }
    return render(request, 'ranking.html', stuff_for_front)


def register(request):
    if request.method == 'POST':
        password1 = request.POST.get('pass')
        password2 = request.POST.get('confpass')
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        if register_validation(first_name, last_name, username, password1, password2, email):
            try:
                User.objects.create_user(username=username,
                                         password=password1,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email)
            except IntegrityError:
                stuff_for_front = {'integrity_error': 'duplicate key'}
                return render(request, 'registration/register.html', stuff_for_front)
        else:
            stuff_for_front = {'error': 'sth is wrong'}
            return render(request, 'registration/register.html', stuff_for_front)

        return HttpResponseRedirect(reverse('type:home'))


def signup(request):
    return render(request, 'registration/register.html')


def log_out(request):
    current_user = request.user
    if current_user.is_authenticated:
        logout(request)
    return redirect('/')


def user_profile(request):
    stuff_for_front = {
        'user': request.user,
    }
    return render(request, 'registration/profile.html', stuff_for_front)


def edit_profile(request):
    user = request.user
    user.first_name = request.POST['firstName']
    user.last_name = request.POST['lastName']
    user.save()
    return HttpResponseRedirect(reverse('type:home'))


def change_password_page(request):
    return render(request, 'registration/changePassword.html')


def edit_password(request):
    user = request.user
    db_password = user.password
    old_pass = request.POST['oldpass']
    new_pass = request.POST['newpass']
    confirm_pass = request.POST['confirmpass']
    stuff_for_front = {'error': 'Error occurred'}
    if handler.verify(old_pass, db_password):
        if new_pass == confirm_pass:
            user.password = handler.hash(new_pass)
            user.save()
            return HttpResponseRedirect(reverse('type:home'))
        else:
            return render(request, 'registration/changePassword.html', stuff_for_front)
    else:
        return render(request, 'registration/changePassword.html', stuff_for_front)


def user_auth(request):
    return render(request, 'registration/login.html')


def signin(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
        stuff_for_front = {'error': 'Error occurred'}
        return render(request, 'registration/login.html', stuff_for_front)
    login(request, user)
    return HttpResponseRedirect(reverse('type:home'))


def is_email_unique(email):
    email = email.lower()
    for person in Profile.objects.all():
        if person.user.email == email:
            return False
    return True


def register_validation(first_name, last_name, username, pass1, pass2, email):
    if first_name == '' or last_name == '' or email == '' or username == '':
        return False
    else:
        if pass1 != pass2:
            return False
        else:
            if is_email_unique(email):
                return True
            else:
                return False


def change_image(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    stuff_for_front = {
        'form': form
    }
    return render(request, 'registration/changeImage.html', stuff_for_front)


def ord_type(request):
    IDs = OrdinaryText.objects.all().values_list('id', flat=True)
    text_obj = OrdinaryText.objects.get(id=IDs[randint(0, len(IDs) - 1)])
    stuff_for_front = {
        'text': text_obj.content
    }
    return render(request, 'type/normal.html', stuff_for_front)


def song_type_mode(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        if mode == 'random_song':
            IDs = Track.objects.all().values_list('id', flat=True)
            track_obj = Track.objects.get(id=IDs[randint(0, len(IDs) - 1)])
            links = get_links_2(track_obj.Artist_name, track_obj.track_title)
            stuff_for_front = {
                'Artist_name': track_obj.Artist_name,
                'track_title': track_obj.track_title,
                'spotify': links[0],
                'soundcloud': links[1]
            }
            return render(request, 'type/songTypeMode.html', stuff_for_front)

        elif mode == 'favorite_song':
            return render(request, 'type/searchSong.html')

    return render(request, 'type/songTypeMode.html')


def song_type(request):
    global lyrics
    stuff_for_front = {
        'lyrics_length': len(lyrics)
    }
    return render(request, 'type/songType.html', stuff_for_front)


def song_type_random(request):
    stuff_for_front = {
        'duration_ms': duration_ms
    }
    return render(request, 'type/songTypeRandom.html', stuff_for_front)


def change_song_score(request):
    global lyrics
    global song_score
    current_user = request.user
    string = request.POST['user_typed_string']
    song_score = LCS(lyrics, string)
    if current_user.is_authenticated:
        if song_score > current_user.profile.song_max_point:
            current_user.profile.song_max_point = song_score
        current_user.profile.song_score += song_score
        current_user.save()
    return HttpResponse('success')


def song_result(request):
    global song_score
    user = request.user

    stuff_for_front = {
        'song_score': song_score,
        'user': user
    }
    return render(request, 'type/song_result.html', stuff_for_front)


def music_upload(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = SongForm()
    stuff_for_front = {
        'form': form
    }
    return render(request, 'type/musicUpload.html', stuff_for_front)


def change_max_point(request):
    global error_count
    global word_count
    global word_per_min

    word_per_min = int(request.POST['word_per_min'])
    error_count = int(request.POST['error_count'])
    word_count = int(request.POST['word_count'])
    current_user = request.user

    calculate_text_score(current_user)

    return HttpResponse('success')


def normal_result(request):
    global error_count
    global word_per_min
    global text_score

    all_users = User.objects.filter(is_superuser=0)

    # all_sorted_user = sorted(all_users, key=lambda x: x.profile.text_score, reverse=True)

    rank_array = []
    current_user = request.user

    if current_user.is_authenticated:
        rank_array = sorted(all_users, key=lambda x: x.profile.text_score, reverse=True)[0:10]

    stuff_for_front = {

        'error_count': error_count,
        'word_per_min': word_per_min,
        'text_score': text_score,
        'rank_array': rank_array,
    }
    return render(request, 'type/normal_result.html', stuff_for_front)


def calculate_text_score(user):
    global word_per_min
    global word_count
    global text_score
    text_score = word_per_min * word_count
    if user.is_authenticated:
        user.profile.text_score += text_score
        if text_score > user.profile.text_max_point:
            user.profile.text_max_point = text_score
        user.save()


def createTextType(request):
    return render(request, 'type/create.html')


def add_new_text(request):
    if request.method == 'POST':
        new_text = request.POST['content']
        if text_in_persian(new_text):
            OrdinaryText.objects.create(content=new_text, user=request.user)
        else:
            stuff_for_front = {
                'language_error': 'error'
            }
            return render(request, 'type/create.html', stuff_for_front)

        return redirect('type:createTextType')


def text_in_persian(text):
    pattern = r'^[آ-ی]([آ-ی]|\s)+$'
    if re.search(pattern, text):
        return True
    return False


def group_page(request):
    user = request.user
    stuff_for_front = {
        'user': user
    }
    return render(request, 'type/GroupPage.html', stuff_for_front)


def creating_group(request):
    user = request.user
    new_group = Group.objects.create(name=request.POST['name'])
    new_group.user_set.add(user)
    GroupAdmin.group = new_group
    GroupAdmin.admin = user
    user.save()
    return HttpResponseRedirect(reverse('type:home'))


def LCS(S1, S2):
    L1 = len(S1)
    L2 = len(S2)

    C = [[0 for j in range(L2 + 1)] for i in range(L1 + 1)]

    for i in range(1, L1 + 1):
        for j in range(1, L2 + 1):
            if i == 0 or j == 0:
                C[i][j] = 0
            elif S2[j - 1] == S1[i - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i - 1][j], C[i][j - 1])

    return C[L1][L2]


def get_links(request):
    singer_name = request.POST.get('singer')
    song_title = request.POST.get('song')

    if singer_name is not None and song_title is not None:
        links = get_links_2(singer_name, song_title)
        stuff_for_front = {
            'spotify': links[0],
            'soundcloud': links[1]
        }
        return render(request, 'type/searchSong.html', stuff_for_front)
    else:
        return render(request, 'type/searchSong.html')

def get_soundcloud_links(request):
    singer_name = request.POST.get('singer')
    song_title = request.POST.get('song')
    soundcloud = SoundCloud(singer_name, song_title)
    songs = soundcloud.get_songs_list()
    url = songs.get('url')
    image_url = soundcloud.get_song_image(url)
    stuff_for_front = {
        'song_url': url,
        'song_image': image_url
    }
    return render(request, 'type/soundcloudSearch.html', stuff_for_front)



def get_links_2(singer_name, song_title):
    spotify = Spotify(singer_name, song_title)
    global duration_ms
    duration_ms = spotify.get_duration_ms()
    soundcloud = SoundCloud(singer_name, song_title)
    spotify_link = spotify.get_song_url()
    soundcloud_link = soundcloud.get_songs_list()
    genius_obj = Genius(singer_name, song_title)
    global lyrics
    lyrics = genius_obj.get_lyrics()
    links = [spotify_link, soundcloud_link]
    return links


def go_to_favorite_song(request):
    return render(request, 'type/favoriteSongType.html')

def go_to_soundcloud_search(request):
    return render(request, 'type/soundcloudSearch.html')
