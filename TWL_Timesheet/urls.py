"""
URL configuration for TWL_Timesheet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# Location: TWL_Timesheet/TWL_Timesheet/urls.py (Project directory)
from django.contrib import admin  # Import admin for Django admin site
from django.urls import path, include  # Import path and include for URL routing
#from django.views.generic import RedirectView  # Import RedirectView for root URL redirection

urlpatterns = [  # List of URL patterns
    path('admin/', admin.site.urls),  # Map /admin/ to Django admin site
    path('OrangeHRM/', include('OrangeHRM.urls')),  # Include timesheet app URLs under /timesheet/
    #path('', RedirectView.as_view(url='/OrangeHRM/approve/'), name='root'),  # Redirect root URL (empty path) to timesheet list
]