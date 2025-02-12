from django.urls import path
from .views import *


app_name = "job_profile"

urlpatterns = [
    
    # Profile
    path('', JobProfileView.as_view(), name='job_profile'),
    
    # Job
    path('job/', JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('job/update/<id>', JobUpdateView.as_view(), name='job-update'),
    path('job/delete/<id>/', JobDeleteView.as_view(), name='job-delete'),
    path('saved-job/', SavedJobListView.as_view(), name='saved-job'),
    path('add-job-title/', AddJobTitleView.as_view(), name='add_job_title'),
    path('upload_image/', upload_image, name='upload_image'),
    path('job-titles/', get_job_titles, name='get_job_titles'),
    
    # Job Application
    path('<int:job_id>/applications/', JobApplicationListView.as_view(), name='application-list'),
    path('applications/', JobApplicationListForApplicantsView.as_view(), name='job_applications_for_applicants'),
    
]