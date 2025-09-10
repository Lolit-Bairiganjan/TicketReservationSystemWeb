from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def main_page(request):
    if request.method == "POST":
        uname = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = uname, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You've been logged in")
            return redirect('main_page')
        else:
            messages.error(request, "There was an error logging in")
            return redirect('main_page')
    return render(request, 'index.html', {})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('main_page')