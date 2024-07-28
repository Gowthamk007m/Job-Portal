from django.urls import path
from .views import *
from jobs.views import JobProfileSelectView
app_name = 'accounts' 

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('details/create/<id>', DetailsCreateView.as_view(), name='create_details'),    
    path('activities/create/', ActivitiesCreateView.as_view(), name='create_activities'),    
    path('qualifications/create/', QualificationsCreateView.as_view(), name='create_qualifications'),   
    path('role/', JobProfileSelectView.as_view(), name='role'),    
]