from django import forms
from .models import Job, JobApplication, JobPortalProfile
from django_select2.forms import Select2Widget


class JobSeekerForm(forms.ModelForm):
    
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'expertise_level',
        ]
        
        widgets = {
            'title': Select2Widget(attrs={'class': 'form-control','required':True}),
            'expertise_level': forms.Select(attrs={'class': 'form-control','required':True})
        }

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.job_profile = 'Job Seeker'
    #     instance.company = None
    #     instance.location = None
    #     if commit:
    #         instance.save()
    #     return instance


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = JobPortalProfile
        fields = [
            'title',
            'company',
            'location',
            ]
        widgets = {
            'title': Select2Widget(attrs={'class': 'form-control', 'required':True}),
            'company': forms.Select(attrs={'class': 'form-control','required':True}),
            'location': forms.Select(attrs={'class': 'form-control', 'required':True}),
        }


    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.job_profile = 'Employee'
    #     if commit:
    #         instance.save()
    #     return instance
    

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['job', 'applicant','status']
        
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'company'
            }),
            'designation':forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'designation'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'autocomplete':'salary'
            }),
            'last_working_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'quit_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 150px;'
            }),
        }