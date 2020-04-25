from django.urls import path
from . import views

app_name = 'type'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
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
    path('type/create/', views.createTextType, name='createTextType'),
    path('type/add_new_text/', views.add_new_text, name='add_new_text'),
    path('type/music/', views.music_upload, name='UploadMusic'),
    path('type/song/search', views.get_links, name='song_search'),
]
