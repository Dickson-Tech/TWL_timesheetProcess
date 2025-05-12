from django import forms  # Import Django forms module for creating form classes
from .models import Timesheet  # Import Timesheet model for form

class TimesheetForm(forms.ModelForm):  # Define form class for Timesheet model
    class Meta:  # Meta class to configure form
        model = Timesheet  # Specify Timesheet model for form
        fields = ['date', 'hours_worked', 'overtime_hours']  # Include only these fields in form
        widgets = {  # Customize form field widgets
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date input for date field
            'hours_worked': forms.NumberInput(attrs={'step': '0.01'}),  # Use number input with 0.01 step for hours
            'overtime_hours': forms.NumberInput(attrs={'step': '0.01'}),  # Use number input with 0.01 step for overtime
        }