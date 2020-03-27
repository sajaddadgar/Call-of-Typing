from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from .form import RegisterForm
from django.contrib.auth.models import User
from .models import is_email_unique
from passlib.hash import django_pbkdf2_sha256 as handler
from django.contrib.auth.models import User

# Create your views here.

# Get authenticated user: request.user
# Get profile of user: request.user.profile.max_point


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        password = request.POST['pass'].lower()


        if request.POST['pass'] == request.POST['confpass'] and len(request.POST['pass']) > 7\
                and request.POST['firstname'] != "" and request.POST['lastname'] != "" and request.POST['email'] != ""\
                and request.POST['username'] != "" and password.islower():
            if is_email_unique(request.POST['email']):
                User.objects.create_user(username=request.POST['username'], password=request.POST['pass'],
                                         first_name=request.POST['firstname'], last_name=request.POST['lastname'],
                                         email=request.POST['email'])
            else:
                raise ValidationError("Email already exists")

            return redirect('/')

        else:
            stuff_for_front = {'error': 'Error occurred'}
            return render(request, 'registration/register.html', stuff_for_front)

    return render(request, 'registration/register.html')


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
    return HttpResponseRedirect(reverse('type:home'))

def change_password_page(request):
    return render(request, 'registration/ChangePassword.html')

def edit_password(request):
    user = request.user
    password = str(request.POST['newpass']).lower()

    if handler.verify(request.POST['oldpass'], user.password):
        if request.POST['newpass'] == request.POST['confirmpass'] and len(password) > 7\
                and password.islower():
            user.password = handler.hash(request.POST['newpass'])
            user.save()
            return HttpResponseRedirect(reverse('type:home'))

        else:
            stuff_for_front = {'error': 'Error occurred'}
            return render(request, 'registration/ChangePassword.html', stuff_for_front)

    else:
        stuff_for_front = {'error': 'Error occurred'}
        return render(request, 'registration/ChangePassword.html', stuff_for_front)


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


def test(request):
    email = 'sajad.dadgar98@gmail.com'

    print(RegisterForm.clean_email())



