from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterUserForm

def sign_up(request):
    form= RegisterUserForm()
    if request.method == "POST":
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print("Invalid")

   
    return render(request, "registration/register.html", {"form":form})


def sign_in(request):
    if request.method == 'POST':
       username= request.POST.get('username')
       password= request.POST.get('password')

       user= authenticate(request, username= username, password= password)

       if user:
           login(request, user)
           return redirect('home')
    return render(request, "registration/login.html")

def sign_out(request):

    if request.method == "POST":
        logout(request)
        return render(request, "registration/login.html")