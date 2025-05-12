# Location: timesheet/urls.py (App directory)
from .payroll_api import send_to_payroll  # Import send_to_payroll view from payroll_api module
from . import views  # Import views module from current app
from django.urls import path
from .views import *  # Import all views from current app

urlpatterns = [  # List of URL patterns
    path('submit/', views.submit_timesheet, name='submit_timesheet'),  # Map /submit/ to submit_timesheet view
    path('approve/<int:timesheet_id>/', views.approve_timesheet, name='approve_timesheet'),  # Map /approve/<id>/ to approve_timesheet view
    path('list/', views.timesheet_list, name='timesheet_list'),  # Map /list/ to timesheet_list view
    path('export/', views.export_timesheet_summary, name='export_timesheet_summary'),  # Map /export/ to export_timesheet_summary view
    path('payroll/', send_to_payroll, name='send_to_payroll'),  # Map /payroll/ to send_to_payroll view
]