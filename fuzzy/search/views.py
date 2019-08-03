from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

def index(request, template_name='search.html'):
    return render(request, template_name)
