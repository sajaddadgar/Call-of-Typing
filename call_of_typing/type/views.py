from django.shortcuts import render
from .form import RegisterForm

# Create your views here.


def home(request):
    pass


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