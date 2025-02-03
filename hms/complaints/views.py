from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import pytz
from .models import Complaint

def complaint_form(request):
    if request.method == 'POST':
        # Process form data
        bhavan = request.POST.get('bhavan')
        room = request.POST.get('room')
        contact_no = request.POST.get('contactNo')
        complaint_group = request.POST.get('complaintGroup')
        area = request.POST.get('area', '')
        requirement = request.POST.get('requirement')
        category = request.POST.get('category', '')
        preferred_time = request.POST.get('preferredTime', '')
        comments = request.POST.get('comments', '')

        # Get current time in UTC and convert to IST
        utc_now = timezone.now()
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

        # Save the complaint to the database
        Complaint.objects.create(
            bhavan=bhavan,
            room=room,
            contact_no=contact_no,
            complaint_group=complaint_group,
            area=area,
            requirement=requirement,
            category=category,
            preferred_time=preferred_time,
            comments=comments,
            user=request.user,  # Store the logged-in user who submitted the complaint
            ist=ist_now  # Set the IST field
        )

        # Use messages framework to display a success message
        messages.success(request, 'Your complaint has been submitted successfully!')

        # Redirect to the complaint success page
        return redirect('complaint_success')  # This should be a URL name for the success page

    # If the request is GET, render the form
    context = {
        'requirement_options': ["electrical", "Mason", "Carpentry", "Painter", "Sweeper", "Worker"],
        'time_options': [
            {"value": "2-3", "label": "2-3 pm"},
            {"value": "3-4", "label": "3-4 pm"},
            {"value": "4-5", "label": "4-5 pm"}
        ],
        'category_options': []  # Dynamically set based on the requirement
    }

    return render(request, 'complaints/Page8.html', context)


def complaint_success(request):
    return render(request, 'complaints/complaint_success.html')

def about_hms_team(request):
    return render(request, 'complaints/Page10.html')

@login_required
def complaints_view(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page9.html', context)