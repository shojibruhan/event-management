from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from users.forms import RegisterUserForm, LogInForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

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

def sign_out(request):

    if request.method == "POST":
        logout(request)
        return render(request, "registration/login.html")
    
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
