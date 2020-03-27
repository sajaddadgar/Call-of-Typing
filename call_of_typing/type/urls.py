from django.urls import path
from . import views

app_name = 'type'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
]
