from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

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

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        passwd = request.POST['password']

        # Basic Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup_page")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup_page")
        
        # Create the user (Django hashes the password automatically)
        user = User.objects.create_user(username=username, email=email, password=passwd)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login_page")