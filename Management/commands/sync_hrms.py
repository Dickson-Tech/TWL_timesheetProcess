from django.core.management.base import BaseCommand  # Import BaseCommand for custom management commands
from OrangeHRM.models import Employee, Department  # Import models for database operations
from django.contrib.auth.models import User  # Import User model for user operations
import requests  # Import requests for making HTTP API calls

class Command(BaseCommand):  # Define custom management command
    help = 'Sync employee data from HRMS API'  # Description of command

    def handle(self, *args, **kwargs):  # Main method to execute command
        hrms_api_url = 'https://hrms.example.com/api/employees'  # Define HRMS API endpoint
        response = requests.get(hrms_api_url)  # Make GET request to HRMS API
        employees = response.json()  # Parse JSON response into Python list

        for emp in employees:  # Loop through employee data from API
            department, _ = Department.objects.get_or_create(name=emp['department'])  # Get or create department
            employee, created = Employee.objects.update_or_create(  # Update or create employee
                employee_id=emp['id'],  # Match by employee ID
                defaults={  # Update these fields
                    'user': User.objects.get_or_create(username=emp['email'])[0],  # Get or create user by email
                    'department': department,  # Assign department
                    'hourly_rate': emp['hourly_rate'],  # Set hourly rate
                    'is_active': emp['is_active']  # Set active status
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Synced employee {employee}'))  # Print success message