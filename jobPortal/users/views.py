from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class UserProfileForm(LoginRequiredMixin,TemplateView):
    template_name = 'users/complete_profile.html'
    
class UserHome(LoginRequiredMixin,TemplateView):
    template_name = 'users/index.html'
    
class JobDetails(TemplateView):
    template_name = 'users/job_detail.html'
