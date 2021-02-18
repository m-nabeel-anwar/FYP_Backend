from django.conf.urls import url
from myapi.views import *
from django.urls import path
urlpatterns = [
    path('getallperson',getAllPersons),
]