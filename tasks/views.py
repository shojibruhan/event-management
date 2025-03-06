from django.shortcuts import render, redirect
from tasks.forms import EventModelForm, EventDetailsModelForm
from tasks.models import Event, RSVP
from datetime import date
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin, is_participant
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User= get_user_model()




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
    
    base_query= Event.objects.select_related('details').prefetch_related('participant')
    if type == "upcoming_events":
        events= base_query.filter(status= "U")
    elif type == "past_events":
        events= base_query.filter(status= "P")
    elif type == "all":
        events= base_query.all()

    query= request.GET.get('q', " ")
   
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

class CreateEvents(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required="tasks.add_event"
    login_url= 'sign-in'
    template_name= "dashboard/event-form.html"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['event_form']= kwargs.get('event_form', EventModelForm())
        context['event_details_form']= kwargs.get('event_details_form', EventDetailsModelForm())

        return context

    def get(self, request, *args, **kwargs):
        context= self.get_context_data()
        return render(request, self.template_name, context)



    def post(self, request, *args, **kwargs):
        event_form= EventModelForm(request.POST)
        event_details_form= EventDetailsModelForm(request.POST, request.FILES)
        if event_form.is_valid() and event_details_form.is_valid():
            event= event_form.save()
            event_details= event_details_form.save(commit=False)
            event_details.events= event
            event_details.save()

            
            messages.success(request, "Events Created Successfully !!!")
            context= self.get_context_data(event_form= event_form, event_details_form= event_details_form)

            return render(request, self.template_name, context)

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


class UpdateEvent(UpdateView):
    model= Event
    form_class= EventModelForm
    template_name= 'dashboard/event-form.html'
    pk_url_kwarg='id'
    context_object_name= 'event'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        event= self.get_object()
        context["event_form"]= self.get_form()

        if hasattr(self.object, 'details') and self.object.details:
            context['event_details_form']= EventDetailsModelForm(instance= self.object.details)
        else:
            context['event_details_form']= EventDetailsModelForm()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object= self.get_object()
        event_form= EventModelForm(request.POST, instance= self.object)
        event_details_form= EventDetailsModelForm(request.POST, instance= getattr(self.object, 'details', None))

        if event_form.is_valid() and event_details_form.is_valid():
            event= event_form.save()
            event_details= event_details_form.save(commit=False)
            event_details.event= event
            event_details_form.save()

            
            messages.success(request, "Events Updated Successfully !!!")

            return redirect("update-events", self.object.id)
        return redirect("update-events", self.object.id)



@login_required
@permission_required('tasks.view_participant', login_url='no-permission')
def view_participents(request):
    participents= User.objects.all()
    
    return render(request , "show_participents.html", {"participents": participents})

view_participents_decorator= [login_required, permission_required('tasks.view_participant', login_url='no-permission')]
@method_decorator(view_participents_decorator,name='dispatch')
class ParticipentsList(ListView):
    model= User
    template_name= "show_participents.html"
    context_object_name= "participents"





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

delete_event_decorator=[login_required, permission_required('tasks.delete_event', login_url='no-permission')]
@method_decorator(delete_event_decorator, name='dispatch')
class DeleteEvent(DeleteView):
    model= Event
    pk_url_kwarg= 'id'
    success_url = reverse_lazy("events-list")

    def post(self, request, *args, **kwargs):
        self.object= self.get_object()
        self.object.delete()

        messages.success(request, "Event Deleted Successfully !!!")
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

class EventDetails(DetailView):
    model= Event
    template_name= "event_details.html"
    pk_url_kwarg= "event_id"
    context_object_name= 'event'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['status_choices']= Event.STATUS_CHOICES

        return context
    def post(self, request, *args, **kwargs):
        event= self.get_object()
        selected_status= request.POST.get('event_status')
        event.status= selected_status
        event.save()

        return redirect('event-details', event.id)
    




@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    
    return redirect('no-permission')