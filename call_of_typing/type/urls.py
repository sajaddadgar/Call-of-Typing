from django.urls import path
from . import views

app_name = 'type'

urlpatterns = [
    path('register/', views.register, name='register'),


]