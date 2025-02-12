from django.urls import path
from .views import EmployeeProfileUpsertView, GetNotificationsView, JobApplicationCreateView, JobApplicationSuccessView, JobListView, JobProfileSelectView, JobSeekerProfileUpsertView, JobDetailView, NotificationDataView, SaveRemoveJobView

app_name = 'jobs'

urlpatterns = [
    # Jobs
    path('', JobListView.as_view(), name='home'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('apply/<int:job_id>/', JobApplicationCreateView.as_view(), name='job_application_create'),
    path('success/<int:pk>/', JobApplicationSuccessView.as_view(), name='job_application_success'),
    
    # Notification
    path('notifications/', GetNotificationsView.as_view(), name='get_notifications'),
    path('notification-data/', NotificationDataView.as_view(), name='notification_data'),
    
    # savejob
    path('save-remove-job/', SaveRemoveJobView.as_view(), name='save_remove_job'),
    
    # JobProfile
    path('select-profile/', JobProfileSelectView.as_view(), name='select_profile'),
    path('create/job-seeker/', JobSeekerProfileUpsertView.as_view(), name='create_job_seeker_profile'),
    path('create/employee/', EmployeeProfileUpsertView.as_view(), name='create_employee_profile'),
]
