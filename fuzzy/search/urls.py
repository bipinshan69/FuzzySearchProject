from django.contrib import admin
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.index,name="index"),
    path('upload_csv/',views.upload_csv,name="upload_csv"),
    path('autocomplete/',views.autocomplete,name="autocomplete"),

]