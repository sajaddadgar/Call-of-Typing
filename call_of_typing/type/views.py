from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from .form import RegisterForm
from django.contrib.auth.models import User
# Create your views here.

# Get authenticated user: request.user
# Get profile of user: request.user.profile.max_point


def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('/')
    else:
        form = RegisterForm()
    stuff_for_front = {
        'form': form
    }
    return render(request, 'registration/register.html', stuff_for_front)


def log_out(request):
    current_user = request.user
    if current_user.is_authenticated:
        logout(request)

    return redirect('/')


def user_profile(request):
    stuff_for_front = {
        'user': request.user
    }
    return render(request, 'registration/profile.html', stuff_for_front)


def edit_profile(request):
    user = request.user
    user.first_name = request.POST['firstName']
    user.last_name = request.POST['lastName']
    user.save()
    return redirect('profile')


def user_auth(request):
    return render(request, 'registration/newLogin.html')


def signin(request):
    username = request.POST['username']
    passw = request.POST['passw']
    user = authenticate(username=username, password=passw)
    login(request, user)
    return HttpResponseRedirect(reverse('type:home'))

