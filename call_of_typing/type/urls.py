from django.urls import path
from . import views

app_name = 'type'

urlpatterns = [
    path('', views.home, name='home'),
    path('ranking/', views.ranking, name='ranking'),

    path('accounts/logout/', views.log_out, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.user_profile, name='profile'),
    path('accounts/edit/', views.edit_profile, name='edit'),
    path('accounts/editpassword/', views.edit_password, name='edit_password'),
    path('accounts/changepassword/', views.change_password_page, name='change_password'),
    path('accounts/authentication/', views.user_auth, name='user_auth'),
    path('accounts/signin/', views.signin, name='signin'),
    path('accounts/change_image/', views.change_image, name='change_image'),

    path('type/change_max_point', views.change_max_point, name='change_max_point'),
    path('type/change_song_score', views.change_song_score, name='change_song_score'),
    path('type/normal/', views.ord_type, name='ord_type'),
    path('type/normal_result', views.normal_result, name='normal_result'),

    path('type/song/mode', views.song_type_mode, name='song_type_mode'),
    path('type/song/random', views.song_type_random, name='song_type_random'),
    path('type/song', views.song_type, name='song_type'),
    path('type/song_result', views.song_result, name='song_result'),
    path('type/create/', views.createTextType, name='createTextType'),
    path('type/add_new_text/', views.add_new_text, name='add_new_text'),
    path('type/music/', views.music_upload, name='UploadMusic'),
    path('type/song/search', views.get_links, name='song_search'),
    path('type/song/soundcloud', views.go_to_soundcloud_search, name='soundcloudSearch'),
    path('type/song/soundcloud/result', views.get_soundcloud_links, name='soundcloudLinks'),

    path('type/group/Mygroups', views.my_groups, name='my_groups'),
    path('type/group/<int:group_id>/', views.group_page, name='GroupPage'),
    path('type/group/create', views.creating_group, name='CreateGroup'),
    path('type/group/join', views.join_group, name='JoinGroup'),
    path('type/group/add_member', views.group_member_adding, name='AddMember'),
    path('type/group/group_normal_type/<int:group_id>/', views.group_normal_type, name='group_normal_type'),
    path('type/group/group_normal_result/<int:group_id>', views.group_normal_result, name='group_normal_result'),
    path('type/group/group_change_normal_type_score/<int:group_id>', views.group_change_normal_type_score, name='group_change_normal_type_score'),
    path('type/group/song/mode/<int:group_id>', views.group_song_mode, name='group_song_mode'),
    path('type/group/song/soundcloud/<int:group_id>', views.group_song_soundcloud, name='group_song_soundcloud'),
    path('type/group/song/soundcloud/result/<int:group_id>', views.group_get_soundcloud_links, name='group_get_soundcloud_links'),
    path('type/group/song/type/<int:group_id>/', views.group_song_type, name='group_song_type'),
    path('type/group/song/change_score/<int:group_id>', views.group_change_song_score, name='group_change_song_score'),
    path('type/group/song/result/<int:group_id>', views.group_song_result, name='group_song_result'),
    path('type/group/leave', views.leave_group, name='LeaveGroup'),

]
