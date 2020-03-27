"""call_of_typing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import type.views as V

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('type.urls')),
    path('accounts/logout/', V.log_out, name='logout'),
    path('accounts/register/', V.register, name='register'),
    path('accounts/profile/', V.user_profile, name='profile'),
    path('accounts/edit/', V.edit_profile, name='edit'),
    path('accounts/editpassword/', V.edit_password, name='edit_password'),
    path('accounts/changepassword/', V.change_password_page, name='change_password'),
    path('accounts/authentication/', V.user_auth, name='user_auth'),
    path('accounts/signin/', V.signin, name='signin'),
    path('about/', V.about, name='about'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_complete"),

]
