from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from jobs.models import JobPortalProfile
from accounts.models import UserActivity,CustomUser

class JobPortalProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user=self.request.user

        if not CustomUser.objects.filter(email=user.email).exists():
            return HttpResponseRedirect(reverse('accounts:create_details', kwargs={'id': user.id}))

        elif not UserActivity.objects.filter(user=request.user).exists():
            return HttpResponseRedirect(reverse('accounts:create_details', kwargs={'id': user.id}))
        
        elif not JobPortalProfile.objects.filter(user=request.user).exists():
            return redirect('accounts:role')
        return super().dispatch(request, *args, **kwargs)

