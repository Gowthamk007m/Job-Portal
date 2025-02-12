from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import default_storage

from job_portal.mixin import JobPortalProfileRequiredMixin
from jobs.models import Job, JobApplication, JobPortalProfile, SaveJob, JobTitle
from user.forms import JobForm

# Create your views here.
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES['file']
        file_path = default_storage.save(f'images/{image.name}', image)
        file_url = default_storage.url(file_path)
        return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_job_titles(request):
    job_titles = JobTitle.objects.all().values('id', 'title')
    return JsonResponse(list(job_titles), safe=False)


# job profile
class JobProfileView(LoginRequiredMixin, JobPortalProfileRequiredMixin, TemplateView):
    template_name = 'job_profile/job_profile.html'


# Job List
class JobListView(LoginRequiredMixin, JobPortalProfileRequiredMixin, ListView):
    model = Job
    template_name = 'job_profile/job_list.html'
    context_object_name = 'data'
    
    def get_queryset(self):
        return Job.objects.filter(user=self.request.user.jobportalprofile)


# Job Create
class JobCreateView(LoginRequiredMixin, JobPortalProfileRequiredMixin, CreateView):
    form_class = JobForm
    template_name = 'job_profile/job_upsert.html'
    success_url = reverse_lazy('job_profile:job-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user.jobportalprofile
        response = super().form_valid(form)
        messages.success(self.request, f'Job created successfully.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Job creation failed.')
        return super().form_invalid(form)

# add job title ajax
@method_decorator(csrf_protect, name='dispatch')
class AddJobTitleView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        if not title:
            return JsonResponse({'success': False, 'message': 'Title cannot be empty.'})
        
        job_title, created = JobTitle.objects.get_or_create(title=title)
        if created:
            return JsonResponse({'success': True, 'id': job_title.id, 'title': job_title.title})
        else:
            return JsonResponse({'success': False, 'message': 'Job title already exists.'})

# Job Update
class JobUpdateView(LoginRequiredMixin, JobPortalProfileRequiredMixin, UpdateView):
    form_class = JobForm
    model = Job
    template_name = 'job_profile/job_upsert.html'
    success_url = reverse_lazy('job_profile:job-list')
    pk_url_kwarg = 'id'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.jobportalprofile)
    
    def form_valid(self, form):
        form.instance.user = self.request.user.jobportalprofile
        response = super().form_valid(form)
        messages.success(self.request, f'Job updated successfully.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Job update failed.')
        return super().form_invalid(form)
    

# Job Delete
class JobDeleteView(LoginRequiredMixin, JobPortalProfileRequiredMixin, View):
    model = Job
    template_name = 'job_profile/job_delete.html'
    success_url = reverse_lazy('user:job-list')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.jobportalprofile)
    
    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('id')
        job = get_object_or_404(Job, id=job_id, user=self.request.user.jobportalprofile)
        job.delete()
        messages.success(self.request, f'Job deleted successfully.')
        return redirect('user:job-list')
    

# Job Detail
class JobDetailView(LoginRequiredMixin, JobPortalProfileRequiredMixin, DetailView):
    model = Job
    template_name = 'job_profile/job-detail.html'
    context_object_name = 'job'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        try:
            jobportal_profile = self.request.user.jobportalprofile
        except JobPortalProfile.DoesNotExist:
            raise Http404("You must have a JobPortalProfile to view job details.")

        if obj.user != jobportal_profile:
            raise Http404("You are not authorized to view this job.")

        return obj


# Job Application List View with status change for job creator
class JobApplicationListView(LoginRequiredMixin, JobPortalProfileRequiredMixin, View):
    template_name = 'job_profile/job_applications.html'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.user != request.user.jobportalprofile:
            messages.error(request, "You do not have permission to view this job's applications.")
            return redirect('job_profile:job-list')

        status_filter = request.GET.get('status', '')
        applications = JobApplication.objects.filter(job=job)

        if status_filter:
            applications = applications.filter(status=status_filter)

        # Pagination
        paginator = Paginator(applications, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'applications': page_obj,
            'job': job,
            'selected_status': status_filter,
            'STATUS_CHOICES': JobApplication.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        job_id = kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)

        if job.user != request.user.jobportalprofile:
            messages.error(request, "You do not have permission to modify this job's applications.")
            return redirect('job_profile:job-list')

        action = request.POST.get('action')
        application_id = request.POST.get('application_id')
        application = get_object_or_404(JobApplication, id=application_id, job=job)

        if action == 'select':
            application.status = 'Selected'
        elif action == 'reject':
            application.status = 'Rejected'
        elif action == 'undo':
            application.status = 'Applied'

        application.save()       
        page_number = request.GET.get('page', 1)
        status_filter = request.GET.get('status', '')

        # Redirect to the same page with the same status filter
        redirect_url = f"{request.path}?page={page_number}&status={status_filter}"
        return redirect(redirect_url)


# Job Application List View for Applicants
class JobApplicationListForApplicantsView(LoginRequiredMixin, JobPortalProfileRequiredMixin, View):
    template_name = 'job_profile/job_applications_for_applicants.html'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        return self.render_list(request)

    def post(self, request, *args, **kwargs):
        application_id = request.POST.get('application_id')
        application = get_object_or_404(JobApplication, pk=application_id, applicant=request.user.jobportalprofile)
        
        if application:
            application.delete()
            messages.success(request, "Job application deleted successfully.")
        else:
            messages.error(request, "Job application not found.")
        
        return self.render_list(request)

    def render_list(self, request):
        applicant = request.user.jobportalprofile
        status_filter = request.GET.get('status', '')
        
        # Get all applications for the current user (applicant)
        applications = JobApplication.objects.filter(applicant=applicant)
        
        # Filter by status if provided
        if status_filter:
            applications = applications.filter(status=status_filter)
        
        # Pagination of applications
        paginator = Paginator(applications, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'applications': page_obj,
            'selected_status': status_filter,
            'STATUS_CHOICES': JobApplication.STATUS,
        }
        return render(request, self.template_name, context)
    

# Saved Jobs
class SavedJobListView(LoginRequiredMixin, ListView):
    model = SaveJob
    template_name = 'job_profile/saved_job.html'
    context_object_name = 'saved_jobs'

    def get_queryset(self):
        return SaveJob.objects.filter(user=self.request.user.jobportalprofile).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        job_id = request.POST.get('job_id')
        action = request.POST.get('action')

        if action == 'delete':
            job = get_object_or_404(SaveJob, id=job_id, user=request.user.jobportalprofile)
            try:
                saved_job = job
                saved_job.delete()
                messages.success(request, "Job removed from saved jobs.")
            except SaveJob.DoesNotExist:
                messages.error(request, "Job not found in saved jobs.")

        return redirect('job_profile:saved_jobs')