from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django!")

def show_task(request):
    return HttpResponse("<h1>This is show task page</h1>")

def events_dashboard(request):
    return render(request, "events.html")

def managerdashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def dashboard(request):
    context= {
        "name": ['spiderman', 'superman', 'batman']
    }
    return render(request, "dashboard.html", context)