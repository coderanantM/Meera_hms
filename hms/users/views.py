import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from social_django.utils import psa
from social_core.exceptions import AuthCanceled, AuthAlreadyAssociated
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmailAuthenticationForm, RegisterForm
from users.models import CustomUser
from django.contrib.auth import get_user_model# Import CustomUser explicitly
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import login
from django.contrib.auth import get_backends
import os

User = get_user_model()

@psa('social:complete')
def auth_receiver(request, backend):
    """
    Custom view that handles the Google OAuth2 callback and performs user login.
    """
    # Get the authenticated user after Google login
    user = request.user

    if user.user_type != 'STUDENT':  # You can add more checks here
        messages.error(request, "Unauthorized user type")
        return redirect('login_view')

    # Log the user in
    login(request, user)
    
    # Redirect to the student dashboard after successful login
    return redirect('student_dashboard')



def login_view(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging output
        print(f"Attempting login for email: {email}, password: {password}")

        # Authenticate the user using email and password
        user = authenticate(request, username=email, password=password)

        # Debugging output
        if user is not None:
            print(f"Authentication successful for email: {email}")
            login(request, user)
            return redirect_dashboard(user)
        else:
            print(f"Authentication failed for email: {email}")
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/Page1.html')






def redirect_dashboard(user):
    DASHBOARD_MAP = {
        'WARDEN': 'warden_dashboard',
        'SUPERINTENDENT': 'warden_dashboard',  # Both go to the same dashboard
    }

    print(f"Redirecting {user.email} (User Type: {user.user_type})")  # Debugging statement

    return redirect(reverse(DASHBOARD_MAP.get(user.user_type, 'home')))

def generate_random_username(email):
    """
    Generate a random username using the email prefix and a random string.
    """
    email_prefix = email.split('@')[0]  # Get the email prefix (before @)
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))  # Generate a 6-character random string
    return f"{email_prefix}_{random_string}"

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['user_type']
            username = form.cleaned_data.get('username', email.split('@')[0])

            # Create the user
            user = form.save(commit=False)
            user.username = username
            user.user_type = user_type
            user.save()

            # Log the user creation for debugging purposes
            print(f"User created: {user.email}, Type: {user.user_type}")

            # Log the user out after registration
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login_view')
        else:
            messages.error(request, "Registration failed. Please check your details.")
    else:
        form = RegisterForm()

    return render(request, 'users/signup.html', {'form': form})




    
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect(reverse('login_view'))


def home_view(request):
    return render(request, 'users/Page1.html')


@login_required(login_url='login_view')
def student_dashboard(request):
    return render(request, 'complaints/Page8.html')


@login_required(login_url='login_view')
def warden_dashboard(request):
    if request.user.user_type not in ['WARDEN', 'SUPERINTENDENT']:
        return redirect('home')
    return render(request, 'complaints/Page2.html')


@login_required
def ems_dashboard(request):
    if request.user.user_type != 'EMS':
        return redirect('home')
    return render(request, 'complaints/ems_dashboard.html')


def sign_out(request):
    del request.session['user_data']
    return redirect('users/sign_in.html')