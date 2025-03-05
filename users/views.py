from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from users.forms import RegisterUserForm, LogInForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from tasks.models import Event, RSVP
from django.db.models import Q, Count
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from users.models import CustomUser
from django.contrib.auth import get_user_model

User= get_user_model()

def is_admin(user):
    return user.groups.filter(name="Admin").exists()
    

def sign_up(request):
    form= RegisterUserForm()
    if request.method == "POST":
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            user= form.save(commit= False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active= False
            print(form.cleaned_data)
            user.save()
            messages.success(request, "Pleace activation your account. A mail is sent to your inbox.")
            return redirect('sign-in')
        else:
            print("Invalid")

   
    return render(request, "registration/register.html", {"form":form})


def sign_in(request):
    form= LogInForm()
    if request.method == 'POST':
       form= LogInForm(data= request.POST)
       
       if form.is_valid():
           user= form.get_user()
           login(request, user)
           return redirect('home')
       
    return render(request, "registration/login.html", {"form": form})
class CustomLogIn(LoginView):
    form_class= LogInForm
    
    
    def get_success_url(self):
        next_url= self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

@login_required
def sign_out(request):

    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    
def activate_user(request, user_id, token):
    try:
        user= User.objects.get(id= user_id)
        if default_token_generator.check_token(user, token):
            user.is_active= True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid Token")
    except User.DoesNotExist:
        return HttpResponse("User Not Found")

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users= User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name= user.all_groups[0].name
        else:
            user.group_name= "No Group Assigned"
    return render(request, "admin/admin_dashboard.html", {"users":users})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user= User.objects.get(id= user_id)
    form= AssignRoleForm()

    if request.method == "POST":
        form= AssignRoleForm(request.POST)

        if form.is_valid():
            role= form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username} is assigned to {role.name} role.")
            return redirect('admin-dashboard')
    return render(request, "admin/assign_role.html", {"form":form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form= CreateGroupForm()

    if request.method == 'POST':
        form= CreateGroupForm(request.POST)

        if form.is_valid():
            group= form.save()
            messages.success(request, f"Group \"{group.name}\" is created successfully.")
            
            return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups= Group.objects.prefetch_related('permissions').all()

    return render(request, "admin/group_list.html", {"groups": groups})

def events_list(request):
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

    return render(request, "events_list.html", context)

@login_required(login_url='sign-in')
def rspv_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if RSVP.objects.filter(user= request.user, event= event).exists():
        messages.warning(request, f"You already booked this event")
        return redirect('my-events')
        
    
    RSVP.objects.create(user= request.user, event= event)
    messages.success(request, "A confirmation mail sent to your inbox!")
    return redirect('my-events')

@login_required
def my_events(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event')

    return render(request, "my_events.html", {"rsvps": rsvps})

def is_participant(user):
    return user.groups.filter(name="Participant").exists() 


@user_passes_test(is_participant, login_url='no-permission')
def participant_dashboard(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event')
    
    return render(request, "participant_dashboard.html", {"rsvps": rsvps})

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name= 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        user= self.request.user
        context['username']= user.username
        context['email']= user.email
        context['bio']= user.bio
        context['profile_image']= user.profile_image
        context['mobile']= user.mobile
        context['name']= user.get_full_name()
        context['member_since']= user.date_joined
        context['last_login']= user.last_login

        return context
    
class ChangePassword(PasswordChangeView):
    template_name= 'accounts/password_change.html'
    form_class= CustomPasswordChangeForm

class CustomPasswordResetView(PasswordResetView):
    form_class= CustomPasswordResetForm
    template_name= 'registration/password_reset.html'
    success_url= reverse_lazy('sign-in')
    html_email_template_name= 'registration/reset_email.html'

    def form_valid(self, form):
        messages.success(self.request, "Password reset form is sent to your mail.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['protocol']= 'https' if self.request.is_secure() else 'http'
        context['domain']= self.request.get_host()

        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class= CustomSetPasswordForm
    template_name= 'registration/password_reset.html'
    success_url= reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request, "Password reset Successfully.")
        return super().form_valid(form)
"""
class EditProfileView(UpdateView):
    model= User
    form_class= EditProfileForm
    template_name= 'accounts/update_profile.html'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs['userprofile']= UserProfile.objects.get(user= self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_profile= UserProfile.objects.get(user=self.request.user)
        context['form']= self.form_class(instance= self.request.user, userprofile= user_profile)

        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
        
"""     

class EditProfileView(UpdateView):
    model= User
    form_class= EditProfileForm
    template_name= 'accounts/update_profile.html'

    def get_object(self):
        return self.request.user
    
    
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')