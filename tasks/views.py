from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django!")

def show_task(request):
    return HttpResponse("<h1>This is show task page</h1>")
