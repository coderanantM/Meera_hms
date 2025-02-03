from django.urls import path
from . import views

urlpatterns = [
    path('complaint/', views.complaint_form, name='complaint_form'),
    path('submit-complaint/', views.complaint_form, name='submit_complaint'),
    path('complaints/', views.complaints_view, name='complaints_list'),
    path('complaint/success/', views.complaint_success, name='complaint_success'),
    path('complaints/about-hms-team/', views.about_hms_team, name='about_hms_team'),
    
]