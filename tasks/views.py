from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import EventModelForm
from tasks.models import Participant, Category, Event, EventDetails
from datetime import date
from django.db.models import Q, Max, Min, Avg, Count

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

def create_events(request):
   
    form= EventModelForm()

    if request.method == 'POST':
        form= EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            context= {
                'form': form,
                "message": "Event added succussfully"
            }
            

            return render(request, 'dashboard/event-form.html', context)
    context= { 'form': form }


    return render(request, 'dashboard/event-form.html', context)

def view_events(request):
    # events= Event.objects.all()
    # events= Event.objects.filter(status= "U")
    # events= Event.objects.filter(schedule= date.today())
    # events= Event.objects.filter(Q(name__icontains= "in") | Q(status= "P"))

            #  ****** select_related(Foreign key, OnetoOne Field) ************

    # events= Event.objects.select_related("details").all()
    # events= Event.objects.select_related("category").all()
    # events= Category.objects.select_related("event_set").all()

            # ******** prefetch_related(reverse Foreign key, ManyToMany Field) **********

    # events= Category.objects.prefetch_related("event_set").all()
    # events= EventDetails.objects.select_related("events").all()
    # events= EventDetails.objects.prefetch_related("events").all()
    # events= Event.objects.prefetch_related("participant").all()

                # Aggregation
    
    # total_person= Participant.objects.aggregate(tot_part= Count("id"))
    events= Category.objects.annotate(tot_part= Count("event"))
    

    return render(request , "show_event.html", {"events": events})

