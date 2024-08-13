from django.views.generic import TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser

# Create your views here.
class UserProfileForm(LoginRequiredMixin,TemplateView):
    template_name = 'users/complete_profile.html'
    
class UserHome(LoginRequiredMixin,TemplateView):
    template_name = 'users/index.html'
    
class JobDetails(TemplateView):
    template_name = 'users/job_detail.html'

class UserProfileView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'user-profile.html'
    pk_url_kwarg = 'id'
    context_object_name = 'user'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Use select_related for one-to-one and many-to-one relationships
        queryset = queryset.select_related('jobportalprofile')
        # Use prefetch_related for many-to-many and reverse FK relationships
        queryset = queryset.prefetch_related(
            'user_activities__hobbies',
            'user_activities__Interest'
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if needed
        return context