from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from .form import ProfileForm
from .models import Profile,OrdinaryText
from passlib.hash import django_pbkdf2_sha256 as handler
from django.contrib.auth.models import User

# Get authenticated user: request.user
# Get profile of user: request.user.profile.max_point


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        password1 = request.POST.get('pass')
        password2 = request.POST.get('confpass')
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        if register_validation(first_name, last_name, username, password1, password2, email):
            User.objects.create_user(username=username,
                                     password=password1,
                                     first_name=first_name,
                                     last_name=last_name,
                                     email=email)
        else:
            raise ValidationError("something wrong: email must be unique, username and name are empty, etc.")

        return HttpResponseRedirect(reverse('type:home'))


def signup(request):
    return render(request, 'registration/register.html')


def log_out(request):
    current_user = request.user
    if current_user.is_authenticated:
        logout(request)
    return redirect('/')


def user_profile(request):
    stuff_for_front = {
        'user': request.user,
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
    db_password = user.password
    old_pass = request.POST['oldpass']
    new_pass = request.POST['newpass']
    confirm_pass = request.POST['confirmpass']
    stuff_for_front = {'error': 'Error occurred'}
    if handler.verify(old_pass, db_password):
        if new_pass == confirm_pass:
            user.password = handler.hash(new_pass)
            user.save()
            return HttpResponseRedirect(reverse('type:home'))
        else:
            return render(request, 'registration/ChangePassword.html', stuff_for_front)
    else:
        return render(request, 'registration/ChangePassword.html', stuff_for_front)


def user_auth(request):
    return render(request, 'registration/login.html')


def signin(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is None:
        stuff_for_front = {'error': 'Error occurred'}
        return render(request, 'registration/login.html', stuff_for_front)
    login(request, user)
    return HttpResponseRedirect(reverse('type:home'))


def is_email_unique(email):
    email = email.lower()
    for person in Profile.objects.all():
        if person.user.email == email:
            return False
    return True


def register_validation(first_name, last_name, username, pass1, pass2, email):
    if first_name == '' and last_name == '' and email == '' and username == '':
        return False
    else:
        if pass1 != pass2:
            return False
        else:
            if is_email_unique(email):
                return True
            else:
                return False


def change_image(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    print(form.fields)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    stuff_for_front = {
        'form': form
    }
    return render(request, 'registration/changeImage.html', stuff_for_front)


def ord_type(request):
    return render(request, 'type/normal.html')


def change_max_point(request):
    current_user = request.user
    word_per_min = int(request.POST['word_per_min'])
    error_count = int(request.POST['error_count'])
    curr_point = word_per_min - error_count
    current_user.profile.score += curr_point
    if curr_point > current_user.profile.max_point:
        current_user.profile.max_point = curr_point

    current_user.save()
    return redirect('/')


def LCS(S1, S2):
    L1 = len(S1)
    L2 = len(S2)

    C = [[None for j in range(L2 + 1)] for i in range(L1 + 1)]

    for i in range(L1 + 1):
        for j in range(L2 + 1):
            if i == 0 or j == 0:
                C[i][j] = 0
            elif S2[j - 1] == S1[i - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i - 1][j], C[i][j - 1])

    return C[L1][L2]


def createTextType(request):
    return render(request, 'type/create.html')


def add_new_text(request):
    if request.method == 'POST':
        OrdinaryText.objects.create(content=request.POST['content'], user=request.user)
        return redirect('type:createTextType')

