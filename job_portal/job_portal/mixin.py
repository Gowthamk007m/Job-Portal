from django.shortcuts import redirect
from jobs.models import JobPortalProfile

# authenticated user dont have access
class RedirectAuthenticatedUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)


# required jobprofile
class JobPortalProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not JobPortalProfile.objects.filter(user=request.user).exists():
            return redirect("job:select_profile")
        return super().dispatch(request, *args, **kwargs)