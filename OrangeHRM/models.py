from django.db import models

# Create your models here.
from django.db import models  # Import Django's models module to define database models
from django.contrib.auth.models import User  # Import User model for authentication and relationships

class Department(models.Model):  # Define Department model to store department information
    name = models.CharField(max_length=100)  # Store department name with max length of 100 characters
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_departments')  # Link to User as department manager, set to NULL if user is deleted

    def __str__(self):  # Define string representation of Department
        return self.name  # Return department name as string

class Employee(models.Model):  # Define Employee model to store employee details
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model, delete employee if user is deleted
    employee_id = models.CharField(max_length=10, unique=True)  # Store unique employee ID with max length of 10 characters
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  # Link to Department, set to NULL if department is deleted
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Store hourly rate with 10 digits, 2 decimal places
    is_active = models.BooleanField(default=True)  # Indicate if employee is active, default to True

    def __str__(self):  # Define string representation of Employee
        return f"{self.user.get_full_name()} ({self.employee_id})"  # Return employee's full name and ID as string

class Timesheet(models.Model):  # Define Timesheet model to store timesheet entries
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Link to Employee, delete timesheet if employee is deleted
    date = models.DateField()  # Store the date of the timesheet entry
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)  # Store regular hours worked with 5 digits, 2 decimal places
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Store overtime hours with 5 digits, 2 decimal places, default to 0
    status = models.CharField(max_length=20, choices=[  # Store timesheet status with predefined choices
        ('PENDING', 'Pending'),  # Status option: Pending
        ('APPROVED', 'Approved'),  # Status option: Approved
        ('REJECTED', 'Rejected')  # Status option: Rejected
    ], default='PENDING')  # Set default status to Pending
    submitted_at = models.DateTimeField(auto_now_add=True)  # Store submission timestamp, auto-set on creation
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_timesheets')  # Link to User who approved, set to NULL if user is deleted

    def __str__(self):  # Define string representation of Timesheet
        return f"{self.employee} - {self.date} - {self.hours_worked} hours"  # Return employee, date, and hours as string