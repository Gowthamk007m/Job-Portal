from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView,TemplateView
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
class JobCreate(LoginRequiredMixin, CreateView):
    form_class = JobCreationForm
    template_name = 'jobs/create_job.html'
    success_url = reverse_lazy('users:jobs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class JobProfileSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'roles.html'
    
    def dispatch(self, request, *args, **kwargs):
        if JobPortalProfile.objects.filter(user=request.user).exists():
            return redirect('user:profile_view')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        job_type = self.request.GET.get('type', None)
        
        if job_type == 'employer':
            return redirect(reverse_lazy('jobs:create_employee_profile'))
        elif job_type == 'jobseeker':
            return redirect(reverse_lazy('jobs:create_job_seeker_profile'))
        else:
            return super().get(request, *args, **kwargs)


class EmployeeProfileUpsertView(LoginRequiredMixin, View):
    template_name = "add-employee.html"
    success_url = reverse_lazy('users:jobs')

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = EmployeeForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = EmployeeForm(request.POST, instance=profile)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_profile(self, request):
        try:
            return JobPortalProfile.objects.get(user=request.user)
        except JobPortalProfile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Employee'
        profile.expertise_level = None
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class JobSeekerProfileUpsertView(LoginRequiredMixin, View):
    template_name = "add-seeker.html"
    success_url = reverse_lazy('users:jobs')

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = JobSeekerForm(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = JobSeekerForm(request.POST, instance=profile)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_profile(self, request):
        try:
            return JobPortalProfile.objects.get(user=request.user)
        except JobPortalProfile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.job_profile = 'Job Seeker'
        profile.company = None
        profile.location = None
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})



class JobCreateView(LoginRequiredMixin, CreateView):
    form_class = JobForm
    template_name = 'job_create.html'
    success_url = reverse_lazy('users:jobs')
    
    def form_valid(self, form):
        form.instance.user = self.request.user.jobportalprofile
        response = super().form_valid(form)
        # messages.success(self.request, f'Job created successfully.')
        return response
    
    def form_invalid(self, form):
        # messages.error(self.request, 'Job creation failed.')
        return super().form_invalid(form)




from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.core.paginator import Paginator
from django.template.loader import render_to_string

class JobListView(LoginRequiredMixin, View):
    template_name = 'users/index.html'
    paginate_by = 10
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        page_number = request.GET.get('page', 1)
        user_profile = request.user.jobportalprofile

        if user_profile.job_profile == 'Employee':
            job_list = Job.objects.filter(user=user_profile).order_by('-created_date')
        else:
            if search_query:
                job_list = Job.objects.filter(job_title__title__icontains=search_query).exclude(user=user_profile).order_by('-created_date')
            else:
                job_list = Job.objects.filter(job_title__title__icontains=user_profile.title).exclude(user=user_profile).order_by('-created_date')

        paginator = Paginator(job_list, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        applied_job_ids = JobApplication.objects.filter(applicant=user_profile).values_list('job_id', flat=True)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            jobs_html = render_to_string('users/job_list_partial.html', {'jobs': page_obj})
            return JsonResponse({'jobs_html': jobs_html, 'has_next': page_obj.has_next()})

        context = {'jobs': page_obj, 'search_query': search_query, 'applied_job_ids': applied_job_ids}
        return render(request, self.template_name, context)




# from django.views.generic import ListView
# from .models import Job

# class JobListView(TemplateView):
#     template_name = 'users/index.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         user_profile = get_object_or_404(JobPortalProfile, user=self.request.user)
        
#         # Fetch all jobs excluding those posted by the current user's profile
#         job_list = Job.objects.exclude(user=user_profile).order_by('-created_date')
        
#         # Assuming you need job application information
#         applied_job_ids = JobApplication.objects.filter(applicant=user_profile).values_list('job_id', flat=True)

#         context.update({
#             'jobs': job_list,
#             'applied_job_ids': applied_job_ids,
#         })
#         return context