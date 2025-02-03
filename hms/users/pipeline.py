from django.shortcuts import redirect
from django.urls import reverse

def set_user_type(strategy, user, response, *args, **kwargs):
    """
    Set the user_type after successful Google login.
    """
    email = user.email.lower()

    # Check if the email domain belongs to BITS Pilani and set user type accordingly
    if email.endswith('@pilani.bits-pilani.ac.in'):
        user.user_type = 'STUDENT'
    else:
        user.user_type = 'SUPERINTENDENT'  # or another type based on your need

    user.save()
    return user
