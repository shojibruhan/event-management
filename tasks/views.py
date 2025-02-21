from django.shortcuts import render, redirect
from tasks.forms import EventModelForm, EventDetailsModelForm
from tasks.models import Event, RSVP
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin, is_participant
from django.contrib.auth.models import User



def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()




def home(request):
    events= Event.objects.all()
    return render(request, 'home.html', {"events": events})





def events_dashboard(request):
    return render(request, "events.html")

@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    type= request.GET.get('type', "upcoming_events")
    # print(type)
    
    base_query= Event.objects.select_related('details').prefetch_related('participant')
    if type == "upcoming_events":
        events= base_query.filter(status= "U")
    elif type == "past_events":
        events= base_query.filter(status= "P")
    elif type == "all":
        events= base_query.all()

    query= request.GET.get('q', " ")
    # if query:
    #     search= base_query.filter(name__icontains = query)
    counts= Event.objects.aggregate(
        total= Count('id'),
        upcoming_events= Count('id', filter= Q(status= "U")),
        past_events= Count('id', filter= Q(status= "P"))
       
    )
   
    total_participant= User.objects.all().count()

    context= {
        "events": events,
        "counts": counts,
        "total_participant": total_participant
    }


    return render(request, 'dashboard/dashboard.html', context)


def participent_dashboard(request):
    return render(request, "dashboard/participent_dashboard.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@login_required
@permission_required('tasks.add_event', login_url='no-permission')
def create_events(request):
   
    event_form= EventModelForm()
    event_details_form= EventDetailsModelForm()


    if request.method == 'POST':
        
        event_form= EventModelForm(request.POST)
        event_details_form= EventDetailsModelForm(request.POST, request.FILES)
        if event_form.is_valid() and event_details_form.is_valid():
            event= event_form.save()
            event_details= event_details_form.save(commit=False)
            event_details.events= event
            event_details.save()

            
            messages.success(request, "Events Created Successfully !!!")

            return redirect("create-events")
    context= { 
        'event_form': event_form, 
        "event_details_form": event_details_form 
        }


    return render(request, 'dashboard/event-form.html', context)


@login_required
@permission_required('tasks.change_event', login_url='no-permission')
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
    context= { 
        'event_form': event_form, 
        "event_details_form": event_details_form,
        "event": event}


    return render(request, 'dashboard/event-form.html', context)


@login_required
@permission_required('tasks.view_participant', login_url='no-permission')
def view_participents(request):
    participents= User.objects.all()
    
    return render(request , "show_participents.html", {"participents": participents})







@login_required
@permission_required('tasks.delete_event', login_url='no-permission')
def delete_event(request, id):
    if request.method == "POST":
        event= Event.objects.get(id= id)
        event.delete()

        messages.success(request, "Event Deleted Successfully !!!")
        return redirect("events-list")

    else:
        messages.error(request, "Something Went Wrong")
        return redirect("events-list")
    


def search_event(request):
    if request.method == "POST":
        searched= request.POST['searched']
        
        events= Event.objects.filter(name__icontains= searched)
        
        context= {
            "events": events,
            
        }
        return render(request, "searched-result.html", context)
    else:
        
        return render(request, "searched-result.html", {})
    
 
def test(request):
    participents= User.objects.all()
    

    return render(request , "test.html", {"participents": participents})

@login_required
@permission_required('tasks.view_event', login_url='no-permission')
def event_details(request, event_id):
    event= Event.objects.get(id= event_id)
    status_choices= Event.STATUS_CHOICES

    if request.method == "POST":
        selected_status= request.POST.get('event_status')
        print(selected_status)
        event.status= selected_status
        event.save()

        return redirect("event-details", event.id)

    return render(request, "event_details.html", {"event": event, "status_choices": status_choices})





@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    
    return redirect('no-permission')