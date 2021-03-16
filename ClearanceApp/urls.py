"""clearance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', views.staffLogin, name = 'login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.staffLogout, name = 'logout'),
    path('add_staff/', views.staffRegister, name='add_staff'),
    path('dashboard/', views.home, name='dashboard'),
    path('add_student/', views.addStudent, name='add_student'),
    path('clearance/', views.clearance, name='clearance'),
    path('clearance/result/', ClearanceListView.as_view(), name='results'),
    path('feedback/', FeedbackListView.as_view(), name='feedback'),
    path('awaiting_clearance/', HODNotClearedListView.as_view(), name='not_cleared'),
    path('school/awaiting_clearance/', SchoolNotClearedListView.as_view(), name='school_not_cleared'),
    path('library/awaiting_clearance/', LibraryNotClearedListView.as_view(), name='library_not_cleared'),
    path('busary/awaiting_clearance/', BusaryNotClearedListView.as_view(), name='busary_not_cleared'),
    path('cleared_students/', HODListView.as_view(), name='cleared_students'),
    path('school/cleared_students/', SchoolOfficerListView.as_view(), name='school_cleared_students'),
    path('library/cleared_students/', LibraryListView.as_view(), name='library_cleared_students'),
    path('awaiting_clearance/<str:slug>/', views.ToSchoolOfficer, name='awaiting_clearance'),
    path('school/awaiting_clearance/<str:slug>/', views.ToLibrary, name='school_awaiting_clearance'),
    path('library/awaiting_clearance/<str:slug>/', views.ToBusary, name='library_awaiting_clearance'),
    path('busary/cleared_students/', BusaryListView.as_view(), name='busary_cleared_students'),
    path('busary/awaiting_clearance/<str:slug>/', views.FinalClearance, name='busary_awaiting_clearance'),
    path('clearance_form/<str:slug>/', ClearanceFormListView.as_view(), name='form_details'),
    path('issues/<str:slug>', views.HodIssues, name='issues'),
    path('school/issues/<str:slug>', views.SchoolIssues, name='school_issues'),
    path('library/issues/<str:slug>', views.LibraryIssues, name='library_issues'),
    path('busary/issues/<str:slug>', views.BusaryIssues, name='busary_issues'),
    path('issues_details/', IssuesListView.as_view(), name='issues_details'),
    path('school/issues_details/', SchoolIssuesListView.as_view(), name='school_issues_details'),
    path('library/issues_details/', LibraryIssuesListView.as_view(), name='library_issues_details'),
    path('busary/issues_details/', BusaryIssuesListView.as_view(), name='busary_issues_details'),
    path('staffs/', StaffListView.as_view(), name='staffs'),
    path('students/', StudentListView.as_view(), name='students'),
]