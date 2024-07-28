from django.urls import path
from .views import *

app_name = 'jobs' 

urlpatterns = [
    path('', JobListView.as_view(), name='home'),
    path('JobCreate/', JobCreate.as_view(), name='JobCreate'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('create/job-seeker/', JobSeekerProfileUpsertView.as_view(), name='create_job_seeker_profile'),
    path('create/employee/', EmployeeProfileUpsertView.as_view(), name='create_employee_profile'),
]