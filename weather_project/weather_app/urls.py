from django.urls import path
from . import views

urlpatterns=[
    path('weather/',views.all_weather,name="weather"),
]