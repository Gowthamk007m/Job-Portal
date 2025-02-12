from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job, JobApplication, Notification, NotificationList, JobPortalProfile

def create_notification(subject, content, job=None, job_application=None):
    notification, created = Notification.objects.get_or_create(
        job=job,
        job_application=job_application,
        defaults={
            'subject': subject,
            'content': content
        }
    )
    return notification, created

@receiver(post_save, sender=Job)
def create_job_notifications(sender, instance, created, **kwargs):
    if created:
        subject = f"New Job Opportunity: {instance.job_title.title}"
        content = f"A new job for {instance.job_title.title} in {instance.location} is now available."
        notification, _ = create_notification(subject, content, job=instance)
        
        jobseekers = JobPortalProfile.objects.filter(title=instance.job_title, job_profile='Job Seeker').exclude(user=instance.user)
        for jobseeker in jobseekers:
            NotificationList.objects.get_or_create(
                user=jobseeker,
                notification=notification
            )

@receiver(post_save, sender=JobApplication)
def create_application_notifications(sender, instance, created, **kwargs):
    if created:
        subject = f"New Application: {instance.job.job_title}"
        content = f"A new application for {instance.job.job_title} in {instance.job.location} has been received."
        notification, _ = create_notification(subject, content, job_application=instance)
        
        employee = instance.job.user
        NotificationList.objects.get_or_create(
            user=employee,
            notification=notification
        )

@receiver(post_save, sender=JobApplication)
def update_application_status_notifications(sender, instance, created, **kwargs):
    if not created and instance.status in ['Selected', 'Rejected']:
        subject = f"Application Status Update: {instance.job.job_title}"
        content = f"Your application status for {instance.job.job_title} in {instance.job.location} has been updated to {instance.status}."
        
        notification = Notification.objects.create(
            job=None,
            job_application=instance,
            subject=subject,
            content=content
        )
        
        job_seeker = instance.applicant
        NotificationList.objects.create(
            user=job_seeker,
            notification=notification
        )
