from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .type import calculate_text_score, get_links_2, LCS, text_in_persian
from ..models import Track, GroupAdmin, GroupMembers, GroupTextSets
from django.contrib.auth.models import User
from random import randint
from django.contrib.auth.models import Group

duration_ms = 0
lyrics = ""
word_per_min = 0
error_count = 0
word_count = 0
text_score = 0
song_score = 0


def my_groups(request):
    user = request.user
    groups = GroupMembers.objects.filter(user=user)
    stuff_for_front = {
        'groups': groups
    }
    return render(request, 'type/my_groups.html', stuff_for_front)


def group_page(request, group_id):
    current_group = Group.objects.get(id=group_id)
    user = request.user
    member = GroupMembers.objects.get(group=group_id, user=user.id)
    stuff_for_front = {
        'current_group': current_group,
        'member': member
    }
    return render(request, 'type/GroupPage.html', stuff_for_front)


def group_normal_type(request, group_id):
    IDs = GroupTextSets.objects.filter(group=group_id).values_list('id', flat=True)
    text_obj = GroupTextSets.objects.get(id=IDs[randint(0, len(IDs) - 1)])
    stuff_for_stuff = {
        'group': Group.objects.get(id=group_id),
        'text': text_obj.content
    }
    return render(request, 'type/group_type/group_normal_type.html', stuff_for_stuff)


def group_add_text(request, group_id):
    content = request.POST['content']
    if text_in_persian(content):
        group = Group.objects.get(id=group_id)
        GroupTextSets.objects.create(group=group, content=content)
        return HttpResponseRedirect(reverse('type:GroupPage', args=(group_id,)))
    stuff_for_front = {
        'Group_id': group_id,
        'language_error': 'error'
    }
    return render(request, 'type/group_type/group_add_text.html', stuff_for_front)


def group_new_text(request, group_id):
    stuff_for_front = {
        'Group_id': group_id
    }
    return render(request, 'type/group_type/group_add_text.html', stuff_for_front)


def group_change_normal_type_score(request, group_id):
    global word_per_min
    global error_count
    global word_count
    word_per_min = int(request.POST['word_per_min'])
    error_count = int(request.POST['error_count'])
    word_count = int(request.POST['word_count'])
    calculate_text_score(request.user, group_id)
    return HttpResponse('success')


def group_normal_result(request, group_id):
    stuff_for_front = {
        'Group_id': group_id,
        'error_count': error_count,
        'word_per_min': word_per_min,
        'text_score': text_score,
    }

    return render(request, 'type/normal_result.html', stuff_for_front)


def group_song_mode(request, group_id):
    stuff_for_front = {
        'Group_id': group_id
    }
    if request.method == 'POST':
        mode = request.POST['mode']
        if mode == 'random_song':
            IDs = Track.objects.all().values_list('id', flat=True)
            track_obj = Track.objects.get(id=IDs[randint(0, len(IDs) - 1)])
            links = get_links_2(track_obj.Artist_name, track_obj.track_title)
            stuff_for_front = {
                'Group_id': group_id,
                'Artist_name': track_obj.Artist_name,
                'track_title': track_obj.track_title,
                'spotify': links[0],
                'soundcloud': links[1]
            }
            return render(request, 'type/songTypeMode.html', stuff_for_front)

        elif mode == 'favorite_song':
            return render(request, 'type/favoriteSongType.html', stuff_for_front)

    return render(request, 'type/songTypeMode.html', stuff_for_front)


def group_song_type(request, group_id):
    global lyrics
    stuff_for_front = {
        'Group_id': group_id,
        'lyrics_length': len(lyrics)
    }
    return render(request, 'type/group_type/group_songType.html', stuff_for_front)


def group_song_soundcloud(request, group_id):
    stuff_for_front = {
        'Group_id': group_id
    }
    return render(request, 'type/soundcloudSearch.html', stuff_for_front)


def group_get_soundcloud_links(request, group_id):
    singer_name = request.POST.get('singer')
    song_title = request.POST.get('song')
    data = get_links_2(singer_name, song_title)
    url, image_url = data[2], data[3]
    stuff_for_front = {
        'Group_id': group_id,
        'song_url': url,
        'song_image': image_url
    }
    return render(request, 'type/soundcloudSearch.html', stuff_for_front)


def group_change_song_score(request, group_id):
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
        g = GroupMembers.objects.get(group=group_id, user=current_user)
        ga = GroupAdmin.objects.get(group=group_id)
        g.user_song_score += song_score
        ga.group_song_score += song_score
        g.save()
        ga.save()
    return HttpResponse('success')


def group_song_result(request, group_id):
    global song_score
    user = request.user

    stuff_for_front = {
        'song_score': song_score,
        'Group_id': group_id
    }
    return render(request, 'type/song_result.html', stuff_for_front)


def creating_group(request):
    if request.method == 'POST':
        admin = request.user
        new_group = Group.objects.create(name=request.POST['name'])
        new_group.user_set.add(admin)
        GroupAdmin.objects.create(group=new_group, admin=admin)
        GroupMembers.objects.create(group=new_group, user=admin)
        return HttpResponseRedirect(reverse('type:my_groups'))

    return render(request, 'type/GroupCreation.html')


def join_group(request):
    user = request.user
    try:
        group = Group.objects.filter(name=request.POST['id'])[0]
        user_groups = GroupMembers.objects.filter(user=user)
        user_groups_name = [g.group.name for g in user_groups]
        if group.name in user_groups_name:
            stuff_for_front = {
                'join_error': 'error'
            }
            return render(request, 'type/GroupCreation.html', stuff_for_front)

        g = GroupAdmin.objects.get(group=group)
        if user == g.admin:
            stuff_for_front = {
                'admin_error': 'error'
            }
            return render(request, 'type/GroupCreation.html', stuff_for_front)

        group.user_set.add(user)
        GroupMembers.objects.create(group=group, user=user)

    except (AttributeError, IndexError):
        stuff_for_front = {
            'group_name_is_not_exists': 'error'
        }
        return render(request, 'type/GroupCreation.html', stuff_for_front)
    return HttpResponseRedirect(reverse('type:home'))


def group_member_adding(request, group_id):
    user = User.objects.get(username=request.POST['member'])
    current_group = Group.objects.get(id=group_id)
    if user.id in GroupMembers.objects.all().values_list('user', flat=True):
        stuff_for_front = {
            'Group_id': group_id
        }
        return render(request, 'type/add_member_error.html', stuff_for_front)

    GroupMembers.objects.create(group=current_group, user=user)
    '''
    for user in all_users:
        if request.POST['member'] == user.username:
            member = user
            break

    for user in all_members:
        if admin == user.user:
            group = user.group

    group.user_set.add(member)
    '''
    return HttpResponseRedirect(reverse('type:GroupPage', args=(group_id,)))


def leave_group(request, group_id):
    user = request.user
    GroupMembers.objects.filter(group=group_id, user=user.id).delete()
    # group.user_set.remove(user)
    return HttpResponseRedirect(reverse('type:my_groups'))


def delete_group(request, group_id):
    Group.objects.filter(id=group_id).delete()
    GroupMembers.objects.filter(group=group_id).delete()
    GroupAdmin.objects.filter(group=group_id).delete()
    GroupTextSets.objects.filter(group=group_id).delete()
    return render(request, 'type/my_groups.html')
