# Location: timesheet/payroll_api.py (App directory)
from django.http import JsonResponse  # Import JsonResponse for returning JSON responses
from .models import Timesheet  # Import Timesheet model for database operations
from django.db.models import Sum  # Import Sum for aggregating database fields
import requests  # Import requests for making HTTP API calls

def send_to_payroll(request):  # View for sending timesheet data to payroll API
    summary = Timesheet.objects.filter(status='APPROVED').values(  # Query approved timesheets
        'employee__employee_id',  # Select employee ID
        'employee__hourly_rate'  # Select hourly rate
    ).annotate(  # Aggregate hours
        total_hours=Sum('hours_worked'),  # Sum regular hours
        total_overtime=Sum('overtime_hours')  # Sum overtime hours
    )
    payroll_data = []  # Initialize list for payroll data
    for entry in summary:  # Loop through summary data
        total_hours = entry['total_hours'] or 0  # Get total hours, default to 0 if None
        overtime_hours = entry['total_overtime'] or 0  # Get overtime hours, default to 0 if None
        total_pay = (total_hours * entry['employee__hourly_rate']) + (overtime_hours * entry['employee__hourly_rate'] * 1.5)  # Calculate pay
        payroll_data.append({  # Add entry to payroll data
            'employee_id': entry['employee__employee_id'],  # Employee ID
            'total_hours': total_hours,  # Total hours
            'overtime_hours': overtime_hours,  # Overtime hours
            'total_pay': total_pay  # Total pay
        })
    payroll_api_url = 'https://payroll.example.com/api/import'  # Define payroll API endpoint
    response = requests.post(payroll_api_url, json=payroll_data)  # Send POST request with payroll data
    return JsonResponse({'status': 'success' if response.status_code == 200 else 'failed'})  # Return JSON response