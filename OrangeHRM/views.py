from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect  # Import render for templates and redirect for URL redirection
from django.contrib.auth.decorators import login_required  # Import decorator to restrict views to logged-in users
from django.http import HttpResponse  # Import HttpResponse for returning raw responses like CSV
from .models import Timesheet, Employee, Department  # Import models for database operations
from .forms import TimesheetForm  # Import form for timesheet submission
import csv  # Import CSV module for generating CSV files
from datetime import datetime  # Import datetime for timestamp in CSV filename
from django.db.models import Sum  # Import Sum for aggregating database fields

@login_required  # Restrict view to logged-in users
def submit_timesheet(request):  # View for submitting a new timesheet
    if request.method == 'POST':  # Check if request is a POST (form submission)
        form = TimesheetForm(request.POST)  # Create form instance with submitted data
        if form.is_valid():  # Validate form data
            timesheet = form.save(commit=False)  # Create timesheet object without saving to database
            timesheet.employee = request.user.employee  # Assign logged-in user's employee to timesheet
            timesheet.save()  # Save timesheet to database
            return redirect('timesheet_list')  # Redirect to timesheet list view
    else:  # If not POST (e.g., GET request)
        form = TimesheetForm()  # Create empty form for rendering
    return render(request, 'timesheet/submit_timesheet.html', {'form': form})  # Render form template

@login_required  # Restrict view to logged-in users
def approve_timesheet(request, timesheet_id):  # View for approving/rejecting a timesheet
    timesheet = Timesheet.objects.get(id=timesheet_id)  # Retrieve timesheet by ID
    if request.user == timesheet.employee.department.manager:  # Check if user is the department manager
        if request.method == 'POST':  # Check if request is a POST (form submission)
            action = request.POST.get('action')  # Get action (approve/reject) from form
            timesheet.status = 'APPROVED' if action == 'approve' else 'REJECTED'  # Set status based on action
            timesheet.approved_by = request.user  # Assign logged-in user as approver
            timesheet.save()  # Save updated timesheet
            return redirect('timesheet_list')  # Redirect to timesheet list view
    return render(request, 'timesheet/approve_timesheet.html', {'timesheet': timesheet})  # Render approval template

@login_required  # Restrict view to logged-in users
def timesheet_list(request):  # View for listing timesheets
    timesheets = Timesheet.objects.filter(employee=request.user.employee)  # Get timesheets for logged-in user's employee
    if request.user.employee.department.manager == request.user:  # Check if user is a department manager
        timesheets = Timesheet.objects.filter(employee__department__manager=request.user)  # Get timesheets for manager's department
    return render(request, 'timesheet/timesheet_list.html', {'timesheets': timesheets})  # Render timesheet list template

@login_required  # Restrict view to logged-in users
def export_timesheet_summary(request):  # View for exporting timesheet summary as CSV
    response = HttpResponse(content_type='text/csv')  # Create HTTP response with CSV content type
    response['Content-Disposition'] = f'attachment; filename="timesheet_summary_{datetime.now().strftime("%Y%m%d")}.csv"'  # Set filename with current date
    writer = csv.writer(response)  # Create CSV writer for response
    writer.writerow(['Employee ID', 'Employee Name', 'Department', 'Total Hours', 'Overtime Hours', 'Total Pay'])  # Write CSV header row
    summary = Timesheet.objects.filter(status='APPROVED').values(  # Query approved timesheets and group by employee
        'employee__employee_id',  # Select employee ID
        'employee__user__first_name',  # Select employee's first name
        'employee__user__last_name',  # Select employee's last name
        'employee__department__name',  # Select department name
        'employee__hourly_rate'  # Select hourly rate
    ).annotate(  # Aggregate hours
        total_hours=Sum('hours_worked'),  # Sum regular hours
        total_overtime=Sum('overtime_hours')  # Sum overtime hours
    )
    for entry in summary:  # Loop through summary data
        total_hours = entry['total_hours'] or 0  # Get total hours, default to 0 if None
        overtime_hours = entry['total_overtime'] or 0  # Get overtime hours, default to 0 if None
        total_pay = (total_hours * entry['employee__hourly_rate']) + (overtime_hours * entry['employee__hourly_rate'] * 1.5)  # Calculate pay (regular + 1.5x overtime)
        writer.writerow([  # Write row to CSV
            entry['employee__employee_id'],  # Employee ID
            f"{entry['employee__user__first_name']} {entry['employee__user__last_name']}",  # Full name
            entry['employee__department__name'],  # Department
            total_hours,  # Total hours
            overtime_hours,  # Overtime hours
            total_pay  # Total pay
        ])
    return response  # Return CSV response