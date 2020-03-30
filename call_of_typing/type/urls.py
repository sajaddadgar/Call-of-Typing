from django.urls import path
from . import views

app_name = 'type'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('accounts/logout/', views.log_out, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.user_profile, name='profile'),
    path('accounts/edit/', views.edit_profile, name='edit'),
    path('accounts/editpassword/', views.edit_password, name='edit_password'),
    path('accounts/changepassword/', views.change_password_page, name='change_password'),
    path('accounts/authentication/', views.user_auth, name='user_auth'),
    path('accounts/signin/', views.signin, name='signin'),

    path('change_image/', views.change_image, name='change_image'),

]
