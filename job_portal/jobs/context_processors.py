from django.urls import reverse_lazy

def notification_url_context(request):
    return {
        'notifications_url': reverse_lazy('job:get_notifications'),
    }

