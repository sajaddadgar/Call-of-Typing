from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from .form import RegisterForm
from django.contrib.auth.models import User
from passlib.hash import pbkdf2_sha256


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
    user.password = request.POST['password']
    user.password = pbkdf2_sha256.encrypt('user.password',rounds = 12000, salt_size = 32)
    user.save()
    return HttpResponseRedirect(reverse('type:home'))


def user_auth(request):
    return render(request, 'registration/login.html')


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        stuff_for_front = {'error': 'Error occurred'}
        return render(request, 'registration/login.html', stuff_for_front)

    login(request, user)
    return HttpResponseRedirect(reverse('type:home'))
