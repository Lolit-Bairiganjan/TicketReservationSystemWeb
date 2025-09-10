from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def main_page(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username = username, password = passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "You're successfully logged in.")
            return redirect('main_page')
        else:
            messages.error(request, "Login failed. Try again.")
            return redirect('main_page')

def logout_user(request):
    logout(request)
    messages.warning(request, "User logged out.")
    return redirect('main_page')

def features_page(request):
    return render(request, 'features.html')

def contacts_page(request):
    return render(request, 'contact.html')

def signup_page(request):
    return render(request, 'login_signup.html')