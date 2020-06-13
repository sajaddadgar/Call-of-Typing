from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..form import SongForm
from ..models import OrdinaryText, Track, GroupAdmin
from django.contrib.auth.models import User
from random import randint
import re
from ..song import Song

duration_ms = 0
lyrics = ""
word_per_min = 0
error_count = 0
word_count = 0
text_score = 0
song_score = 0


def ranking(request):
    all_users = User.objects.filter(is_superuser=0)
    all_groups = GroupAdmin.objects.all()
    text_rank_array = sorted(all_users, key=lambda x: x.profile.text_score, reverse=True)[0:10]
    song_rank_array = sorted(all_users, key=lambda x: x.profile.song_score, reverse=True)[0:10]
    group_text_rank_array = sorted(all_groups, key=lambda x: x.get_group_text_score(), reverse=True)[0:10]
    group_song_rank_array = sorted(all_groups, key=lambda x: x.get_group_song_score(), reverse=True)[0:10]

    if text_rank_array[len(text_rank_array) - 1].profile.text_score == 0:
        for i in range(len(text_rank_array)):
            if text_rank_array[i].profile.text_score == 0:
                text_rank_array = text_rank_array[0:i]
                break
    if song_rank_array[len(song_rank_array) - 1].profile.song_score == 0:
        for i in range(len(song_rank_array)):
            if song_rank_array[i].profile.song_score == 0:
                song_rank_array = song_rank_array[0:i]
                break

    stuff_for_front = {
        'text_rank_array': text_rank_array,
        'song_rank_array': song_rank_array,
        'group_text_rank_array': group_text_rank_array,
        'group_song_rank_array': group_song_rank_array
    }
    return render(request, 'ranking.html', stuff_for_front)


def ord_type(request):
    IDs = OrdinaryText.objects.all().values_list('id', flat=True)
    text_obj = OrdinaryText.objects.get(id=IDs[randint(0, len(IDs) - 1)])
    stuff_for_front = {
        'text': text_obj.content
    }
    return render(request, 'type/normal.html', stuff_for_front)


def song_type_mode(request):
    global lyrics, duration_ms
    if request.method == 'POST':
        mode = request.POST['mode']
        if mode == 'random_song':
            IDs = Track.objects.all().values_list('id', flat=True)
            track_obj = Track.objects.get(id=IDs[randint(0, len(IDs) - 1)])
            song_obj = Song()
            data = song_obj.get_data(track_obj.Artist_name, track_obj.track_title)
            lyrics, duration_ms = data[4], data[5]
            lyrics = pre_process_lyrics(lyrics)
            stuff_for_front = {
                'Artist_name': track_obj.Artist_name,
                'track_title': track_obj.track_title,
                'spotify': data[0],
                'soundcloud': data[1]
            }
            return render(request, 'type/songTypeMode.html', stuff_for_front)

        elif mode == 'favorite_song':
            return render(request, 'type/favoriteSongType.html')

    return render(request, 'type/songTypeMode.html')


def pre_process_lyrics(S):
    pattern = r'\[.*\]'
    S = re.sub(pattern, '', S)
    S = re.sub(r'(\s)+', ' ', S)
    S = S[1:]
    return S


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
        current_user.profile.save_song_score(song_score)

    return HttpResponse('success')


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


def calculate_text_score(user):
    global word_per_min
    global word_count
    global text_score
    text_score = word_per_min * word_count
    if user.is_authenticated:
        user.profile.save_text_score(text_score)


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
    pattern = r'^[آ-ی]([آ-ی]| )+$'
    if re.search(pattern, text):
        return True
    return False


def get_soundcloud_links(request):
    global lyrics
    singer_name = request.POST.get('singer')
    song_title = request.POST.get('song')
    song_obj = Song()
    data = song_obj.get_data(singer_name, song_title)
    url, image_url = data[2], data[3]
    lyrics = data[4]
    lyrics = pre_process_lyrics(lyrics)
    stuff_for_front = {
        'song_url': url,
        'song_image': image_url
    }
    return render(request, 'type/soundcloudSearch.html', stuff_for_front)


def go_to_soundcloud_search(request):
    return render(request, 'type/soundcloudSearch.html')

