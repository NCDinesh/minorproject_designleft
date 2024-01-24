from django.urls import path
from .views import parse_resumes

urlpatterns = [
    path('', parse_resumes, name='parse_resumes'),
]
