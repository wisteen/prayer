from django.urls import path
from . import views

urlpatterns = [
    path('', views.current_prayer, name='current_prayer'),
]
