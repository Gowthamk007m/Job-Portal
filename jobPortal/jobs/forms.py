from django.forms import ModelForm
from django import forms
from .models import *
from tinymce.widgets import TinyMCE


class JobSeekerForm(ModelForm):
    
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'expertise_level',
        ]
        
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control','required':True}),
            'expertise_level': forms.Select(attrs={'class': 'form-control','required':True})
        }


# Employee Form
class EmployeeForm(ModelForm):
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'company',
            'location',
            ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'col-12'})
        self.fields['company'].widget.attrs.update({'class': 'col-8'})
        self.fields['location'].widget.attrs.update({'class': 'col-8'})


class JobSeekerForm(forms.ModelForm):
    
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'expertise_level',
        ]
        
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control','required':True}),
            'expertise_level': forms.Select(attrs={'class': 'form-control','required':True})
        }


class JobCreationForm(ModelForm):
    class Meta:
        model = Job
        exclude = ['user']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'job_description', 'salary_from', 'salary_to', 'location', 'expected_joining_date']
        
        widgets = {
            'job_title': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter job title', 'required':True}),
            'job_description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'location': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter job location', 'required':True}),
            'expected_joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter expected joining date', 'required':True}),
            'salary_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter job salary', 'required':True}),
            'salary_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter job salary', 'required':False})
        }
        