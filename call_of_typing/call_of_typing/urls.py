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
import type.views as V

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('type.urls')),
    path('accounts/logout/', V.log_out, name='logout'),
    path('accounts/register/', V.register, name='register'),
    path('accounts/profile/', V.user_profile, name='profile'),
    path('accounts/edit/', V.edit_profile, name='edit'),
    path('accounts/authentication/', V.user_auth, name='user_auth'),
    path('accounts/signin/', V.signin, name='signin'),
]
