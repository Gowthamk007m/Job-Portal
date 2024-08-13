from django.urls import path
from .views import *

app_name = 'users' 

urlpatterns = [
    path('complete-profile/', UserProfileForm.as_view(), name='complete-profile'),
    path('jobs/', UserHome.as_view(), name='jobs'),
    path('job-details/', JobDetails.as_view(), name='job-details'),
    path('user-profile/<id>', UserProfileView.as_view(), name='user-profile'),
]