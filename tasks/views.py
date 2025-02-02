from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import EventModelForm, EventDetailsModelForm, ParticipentModelForm
from tasks.models import Participant, Category, Event, EventDetails
from datetime import date
from django.db.models import Q, Max, Min, Avg, Count
from django.contrib import messages

def home(request):
    events= Event.objects.all()
    return render(request, 'home.html', {"events": events})





def events_dashboard(request):
    return render(request, "events.html")

def managerdashboard(request):
    type= request.GET.get('type', "upcoming_events")
    # print(type)
    base_query= Event.objects.select_related('details').prefetch_related('participant')
    if type == "upcoming_events":
        events= base_query.filter(status= "U")
    elif type == "past_events":
        events= base_query.filter(status= "P")
    elif type == "all":
        events= base_query.all()
    
    counts= Event.objects.aggregate(
        total= Count('id'),
        upcoming_events= Count('id', filter= Q(status= "U")),
        past_events= Count('id', filter= Q(status= "P"))
       
    )
   
    total_participant= Participant.objects.all().count()

    context= {
        "events": events,
        "counts": counts,
        "total_participant": total_participant
    }


    return render(request, 'dashboard/manager-dashboard.html', context)

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def create_events(request):
   
    event_form= EventModelForm()
    event_details_form= EventDetailsModelForm()


    if request.method == 'POST':
        
        event_form= EventModelForm(request.POST)
        event_details_form= EventDetailsModelForm(request.POST)
        if event_form.is_valid() and event_details_form.is_valid():
            event= event_form.save()
            event_details= event_details_form.save(commit=False)
            event_details.events= event
            event_details.save()

            
            messages.success(request, "Events Created Successfully !!!")

            return redirect("create-events")
    context= { 'event_form': event_form, "event_details_form": event_details_form }


    return render(request, 'dashboard/event-form.html', context)

def update_event(request, id):
    
    event= Event.objects.get(id= id)
    event_form= EventModelForm(instance= event)
    if event.details:
        event_details_form= EventDetailsModelForm(instance= event.details)


    if request.method == 'POST':
        
        event_form= EventModelForm(request.POST, instance= event)
        event_details_form= EventDetailsModelForm(request.POST, instance= event.details)

        if event_form.is_valid() and event_details_form.is_valid():
            event_form.save()
            event_details= event_details_form.save(commit=False)
            event_details.event= event
            event_details_form.save()

            
            messages.success(request, "Events Updated Successfully !!!")

            return redirect("update-events", id)
    context= { 'event_form': event_form, "event_details_form": event_details_form }


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
    # events= Category.objects.annotate(tot_part= Count("event"))
    # events= Event.objects.prefetch_related("participant").count()
    participents= Participant.objects.all()
    

    return render(request , "show_event.html", {"participents": participents})

def create_participent(request):

    participant_form= ParticipentModelForm()

    return render(request, "participent-form.html", {"participant_form": participant_form})



    

def delete_event(request, id):
    if request.method == "POST":
        event= Event.objects.get(id= id)
        event.delete()

        messages.success(request, "Event Deleted Successfully !!!")
        return redirect("manager-dashboard")

    else:
        messages.error(request, "Something Went Wrong")
        return redirect("manager-dashboard")