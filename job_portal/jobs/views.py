from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from .forms import EmployeeForm, JobApplicationForm, JobSeekerForm
from .models import Job, JobApplication, JobPortalProfile, Location, NotificationList, SaveJob
from job_portal.mixin import JobPortalProfileRequiredMixin

# Job Profile Select View
class JobProfileSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/select_jobprofile.html'
    
    def dispatch(self, request, *args, **kwargs):
        if JobPortalProfile.objects.filter(user=request.user).exists():
            return redirect('user:profile_view')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        job_type = request.GET.get('type', None)
        if job_type == 'employer':
            return redirect(reverse_lazy('job:create_employee_profile'))
        elif job_type == 'jobseeker':
            return redirect(reverse_lazy('job:create_job_seeker_profile'))
        else:
            return super().get(request, *args, **kwargs)

# Base Profile Upsert View
class ProfileUpsertView(LoginRequiredMixin, View):
    success_url = reverse_lazy('job_profile:job_profile')

    def get(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = self.get_form(instance=profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        profile = self.get_profile(request)
        form = self.get_form(request.POST, instance=profile)
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
        self.customize_profile(profile)
        profile.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

    def get_form(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method")

    def customize_profile(self, profile):
        raise NotImplementedError("Subclasses should implement this method")

# Job Seeker Profile Upsert View
class JobSeekerProfileUpsertView(ProfileUpsertView):
    template_name = 'jobs/job_seeker_create.html'

    def get_form(self, *args, **kwargs):
        return JobSeekerForm(*args, **kwargs)

    def customize_profile(self, profile):
        profile.job_profile = 'Job Seeker'
        profile.company = None
        profile.location = None

# Employee Profile Upsert View
class EmployeeProfileUpsertView(ProfileUpsertView):
    template_name = 'jobs/employee_create.html'

    def get_form(self, *args, **kwargs):
        return EmployeeForm(*args, **kwargs)

    def customize_profile(self, profile):
        profile.job_profile = 'Employee'
        profile.expertise_level = None

# Job List View
class JobListView(LoginRequiredMixin, JobPortalProfileRequiredMixin, View):
    template_name = 'jobs/job.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q', '')
        selected_locations = request.GET.getlist('location')
        items_per_page = int(request.GET.get('items_per_page', 1))
        
        # Base job list filtered by search query or user profile
        if search_query:
            base_job_list = Job.objects.filter(job_title__title__icontains=search_query)
        else:
            base_job_list = Job.objects.filter(
                job_title__title__icontains=request.user.jobportalprofile.title
            ).exclude(
                user=request.user.jobportalprofile
            ).order_by('-created_at')

        total_job_count = base_job_list.count()

        # Aggregate job counts by location
        location_job_counts = base_job_list.values('location__location').annotate(count=Count('id')).order_by('-count')

        # Create a dictionary of location counts
        location_job_count_dict = {loc['location__location']: loc['count'] for loc in location_job_counts}

        # Get locations
        all_locations = Location.objects.filter(job__in=base_job_list).distinct()

        # Merge job counts with all locations
        location_counts = []
        for loc in all_locations:
            loc_name = loc.location
            loc_count = location_job_count_dict.get(loc_name, 0)
            location_counts.append((loc_name, loc_count))
        
        # Sort locations by job count in descending order
        sorted_location_counts = sorted(location_counts, key=lambda x: x[1], reverse=True)

        if selected_locations:
            location_ids = Location.objects.filter(location__in=selected_locations).values_list('id', flat=True)
            job_list = base_job_list.filter(location__id__in=location_ids)
        else:
            job_list = base_job_list

        paginator = Paginator(job_list, items_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        applied_job_ids = JobApplication.objects.filter(applicant=request.user.jobportalprofile).values_list('job_id', flat=True)
        saved_job_ids = SaveJob.objects.filter(user=request.user.jobportalprofile).values_list('job_id', flat=True)

        context = {
            'jobs': page_obj,
            'search_query': search_query,
            'applied_job_ids': applied_job_ids,
            'saved_job_ids': saved_job_ids,
            'locations': sorted_location_counts,
            'selected_locations': selected_locations,
            'items_per_page': items_per_page,
            'total_job_count': total_job_count,
        }
        return render(request, self.template_name, context)


# Job Detail View
class JobDetailView(LoginRequiredMixin, JobPortalProfileRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/job-detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        applicant = self.request.user.jobportalprofile
        context['already_applied'] = JobApplication.objects.filter(job=job, applicant=applicant).exists()
        context['saved_job'] = SaveJob.objects.filter(job=job, user=applicant)
        return context

# Job Application Create View
class JobApplicationCreateView(LoginRequiredMixin, JobPortalProfileRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/job_apply.html'
    
    def get_success_url(self):
        return reverse_lazy('job:job_application_success', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        applicant = request.user.jobportalprofile

        if JobApplication.objects.filter(job=job, applicant=applicant).exists():
            messages.error(request, 'You have already applied for this job.')
            return redirect('job:job-detail', pk=job.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        initial['job'] = job
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        context['job'] = job
        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(Job, id=job_id)
        applicant = self.request.user.jobportalprofile
        form.instance.applicant = applicant
        form.instance.job = job
        return super().form_valid(form)

# Job Application Success View
class JobApplicationSuccessView(LoginRequiredMixin, JobPortalProfileRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'jobs/job_application_success.html'
    context_object_name = 'application'

    def get_object(self):
        try:
            return JobApplication.objects.get(pk=self.kwargs['pk'], applicant=self.request.user.jobportalprofile)
        except self.model.DoesNotExist:
            raise Http404('Job application not found.')

# Save/Remove Job View
class SaveRemoveJobView(View):
    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')
        job_id = request.GET.get('job_id')
        
        if not action or not job_id:
            return JsonResponse({'status': 'error', 'message': 'Missing action or job ID'})
        
        user = request.user.jobportalprofile
        job = get_object_or_404(Job, id=job_id)
        
        if action == 'save':
            saved_job, created = SaveJob.objects.get_or_create(user=user, job=job)
            if created:
                return JsonResponse({'status': 'success', 'message': 'Job saved successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Job already saved'})
        
        elif action == 'remove':
            try:
                saved_job = SaveJob.objects.get(user=user, job=job)
                saved_job.delete()
                return JsonResponse({'status': 'success', 'message': 'Job removed successfully'})
            except SaveJob.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Job not found'})
        
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

# Get Notifications View
class GetNotificationsView(View):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user.jobportalprofile
            notifications = NotificationList.objects.filter(user=user).select_related('notification')

            data = []
            for notification in notifications:
                notification_data = {
                    'id': notification.id,
                    'subject': notification.notification.subject,
                    'content': notification.notification.content,
                    'created': notification.notification.created,
                    'is_read': notification.is_read,
                    'url': self.get_notification_url(notification, request)
                }
                data.append(notification_data)

            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get_notification_url(self, notification, request):
        if notification.notification.job:
            return reverse_lazy('job:job-detail', args=[notification.notification.job.id])
        elif notification.notification.job_application:
            if request.user.jobportalprofile.job_profile == 'Employee':
                return reverse_lazy('job_profile:application-list', args=[notification.notification.job_application.job.id])
            else:
                return reverse_lazy('job_profile:job_applications_for_applicants')
        else:
            return reverse_lazy('core:home')

# Notification Data View
class NotificationDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            user_profile = request.user.jobportalprofile
            unread_count = NotificationList.objects.filter(user=user_profile, is_read=False).count()
            NotificationList.objects.filter(user=user_profile, is_read=False).update(is_read=True)
            return JsonResponse({'unread_count': unread_count})
        except JobPortalProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)