from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import EventForm, EventModelForm
from tasks.models import Participant

def home(request):
    return render(request, 'home.html')

def show_task(request):
    return HttpResponse("<h1>This is show task page</h1>")

def events_dashboard(request):
    return render(request, "events.html")

def managerdashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def create_task(request):
    participant= Participant.objects.all()
    form= EventModelForm()

    if request.method == 'POST':
        form= EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse("Event added successfully!")
    context= {
        'form': form
    }

    return render(request, 'dashboard/event-form.html', context)