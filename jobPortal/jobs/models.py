from django.db import models

from accounts.models import LEVEL_CHOICES, CustomUser

class Location(models.Model):
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.location


class JobTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
    
class Industry(models.Model):
    industry = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.industry


class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class JobPortalProfile(models.Model):
    JOBPROFILE_CHOICES = (
        ('Job Seeker', 'Job Seeker'),
        ('Employee', 'Employee'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, null=True, blank=True)
    
    # Job Seeker
    expertise_level = models.CharField(max_length=12, choices=LEVEL_CHOICES, null=True, blank=True)
    
    # Employer
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    
    job_profile = models.CharField(max_length=12, choices=JOBPROFILE_CHOICES, default='Job Seeker')
    
    def is_jobseeker(self):
        return self.job_profile == 'Job Seeker'
    
    def is_employee(self):
        return self.job_profile == 'Employee'
    
    def __str__(self):
        return f"{self.user}'s Profile"
    

class Job(models.Model):    
    user = models.ForeignKey(JobPortalProfile, on_delete=models.CASCADE) 
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    job_description = models.TextField(null=True, blank=True)
    salary_from = models.PositiveIntegerField(null=True, blank=True)
    salary_to = models.PositiveIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    expected_joining_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job_title}"


class JobApplication(models.Model):
    STATUS = [
        ('Applied', 'Applied'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobPortalProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    last_working_date = models.DateField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    quit_reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default='Applied')
    
    def __str__(self):
        return f"{self.applicant} applied for {self.job.job_title}"