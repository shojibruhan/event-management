from django.shortcuts import render
from tasks.models import Event
# Create your views here.

def home(request):
    events= Event.objects.all()
    return render(request, 'home.html', {"events": events})

def no_permission(request):
    return render(request, "no_permission.html")