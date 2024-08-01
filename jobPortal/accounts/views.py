from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from.mixin import *
from .models import *
from .forms import CustomUserCreationForm, LoginForm,ActivitiesForm,QualificationsForm,DetailsForm
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,TemplateView
from django.views import View
from django.contrib.auth import logout 

class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'auth/register.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse('accounts:create_details', kwargs={'id': user.id}))


class LoginView(View):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('jobs:home')
            else:
                form.add_error(None, "Invalid email or password.")
                return render(request, self.template_name, {'form': form})


class ForgotPasswordView(TemplateView):
    template_name = 'auth/forgot_password.html'



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class DetailsCreateView(LoginRequiredMixin, UpdateView):
    model=CustomUser
    form_class = DetailsForm
    template_name = 'users/complete_profile.html'
    success_url = reverse_lazy('accounts:create_activities')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return CustomUser.objects.filter(username=self.request.user.username)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ActivitiesCreateView(LoginRequiredMixin, CreateView):
    form_class = ActivitiesForm
    template_name = 'users/user_activities.html'
    success_url = reverse_lazy('accounts:create_qualifications')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class QualificationsCreateView(LoginRequiredMixin, CreateView):
    form_class = QualificationsForm
    template_name = 'users/user_qualifications.html'
    success_url = reverse_lazy('accounts:role')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

# class UserHobbyUpdateView(UpdateView):
#     model = UserHobby
#     form_class = UserHobbyForm
#     template_name = 'user_hobby_form.html'
#     context_object_name = 'user_hobby'

#     def get_object(self):
#         user_id = self.kwargs.get('user_id')
#         user_hobby, created = UserHobby.objects.get_or_create(user_id=user_id)
#         return user_hobby

#     def get_success_url(self):
#         return reverse_lazy('some_view_name')

class Role(LoginRequiredMixin, TemplateView):
    template_name = 'users/role.html'
