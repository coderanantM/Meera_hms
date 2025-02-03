from django.urls import path, include
from . import views

urlpatterns = [
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),

    # Dashboards
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('warden/', views.warden_dashboard, name='warden_dashboard'),
    path('ems/', views.ems_dashboard, name='ems_dashboard'),
    
    # Home view
    path('', views.home_view, name='home'),
]