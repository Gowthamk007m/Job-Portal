from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView, TemplateView, View, ListView, CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from .token import custom_token_generator
from .forms import ImageForm, UserDetailAddForm, UserHobbyAddForm, UserHobbyForm, UserImageForm, UserInterestAddForm, UserInterestForm, UserRegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, ProfileUpdateForm, ChangePasswordForm, AddressCreateForm, ExperienceUpsertForm, EducationUpsertForm, UserSkillUpsertForm
from .models import CustomUser, Address, Experience, Education, UserHobby, UserImages, UserInterest, UserSkill
from job_portal.mixin import RedirectAuthenticatedUserMixin


# Create your views here.

# Register 1st step
class CustomRegisterView(RedirectAuthenticatedUserMixin, FormView):
    template_name = "accounts/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile_add")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        
        # Perform Login Function
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            messages.success(
                self.request,
                f"Account created successfully for {user.first_name} {user.last_name}! You are now logged in.",
            )
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Failed to log in after registration. Please try logging in manually.")
            return redirect("user:login")
        

# Register 2nd step
class RegisterCompleteView(LoginRequiredMixin, FormView):
    template_name = 'accounts/registrationcomplete.html'
    success_url = reverse_lazy("job:select_profile")
    form_class = UserDetailAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hobby_form'] = UserHobbyForm()
        context['interest_form'] = UserInterestForm()
        context['image_form'] = UserImageForm()
        return context
    
    def form_valid(self, form):
        # Initialize forms with POST data
        hobby_form = UserHobbyForm(self.request.POST)
        interest_form = UserInterestForm(self.request.POST)
        image_form = UserImageForm(self.request.POST, self.request.FILES)
        
        # Validate all forms
        if hobby_form.is_valid() and interest_form.is_valid() and image_form.is_valid() and form.is_valid():
            hobbies = hobby_form.cleaned_data['hobbies']
            for hobby in hobbies:
                UserHobby.objects.get_or_create(user=self.request.user, hobby=hobby)
            
            interests = interest_form.cleaned_data['interests']
            for interest in interests:
                UserInterest.objects.get_or_create(user=self.request.user, interest=interest)
                
            images = self.request.FILES.getlist('image')
            for image in images:
                UserImages.objects.create(user=self.request.user, image=image)
            
            user = self.request.user
            user.profile_photo = form.cleaned_data['profile_photo']
            user.dob = form.cleaned_data['dob']
            user.qualification = form.cleaned_data['qualification']
            user.smoking_habit = form.cleaned_data['smoking_habit']
            user.drinking_habit = form.cleaned_data['drinking_habit']
            user.short_reel = form.cleaned_data['short_reel']
            
            user.save()
            
            return super().form_valid(form)
        
        return self.form_invalid(form, hobby_form=hobby_form, interest_form=interest_form, image_form=image_form)

    def form_invalid(self, form, hobby_form=None, interest_form=None, image_form=None):
        context = self.get_context_data(
            form=form,
            hobby_form=hobby_form or UserHobbyForm(),
            interest_form=interest_form or UserInterestForm(),
            image_form=image_form or UserImageForm(),
        )
        return self.render_to_response(context)
    
    
# Login
class CustomLoginView(RedirectAuthenticatedUserMixin, View):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name} {user.last_name}! You have successfully logged in.')
                next_url = request.GET.get('next', self.success_url)
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        return render(request, self.template_name, {'form': form})


# Logout
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect(reverse('user:login'))
    
    
# Forgot Password
class ForgotPasswordView(RedirectAuthenticatedUserMixin, View):
    template_name = 'accounts/forgot_password.html'
    success_template_name = 'accounts/emailsentforgotpassword.html'
    form_class = ForgotPasswordForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            
            if user is not None:
                current_site = get_current_site(request)
                mail_subject = 'Reset Your Password'
                message = render_to_string('accounts/reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': custom_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.content_subtype = 'html'
                send_email.send()
                
                context = {
                    'email': email,
                }
                return render(request, self.success_template_name, context)
            else:
                messages.error(request, 'Account does not exist.')
                return redirect('user:forgot-password')
        else:
            return render(request, self.template_name, {'form': form})
        

# Reset Password   
class ResetPasswordView(RedirectAuthenticatedUserMixin, View):
    template_name = "accounts/reset_password.html"
    form_class = ResetPasswordForm
    
    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return None
    
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and custom_token_generator.check_token(user, token):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')
    
    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        
        if user is not None and custom_token_generator.check_token(user, token):
            form = self.form_class(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful. Please login with your new password.')
                    return redirect('user:login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'This link has expired or is invalid.')
            return redirect('user:login')

       
# Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user = request.user
            user_image.save()
            messages.success(request, 'Image updated successfully.')
            return redirect(reverse_lazy('user:profile_view'))
        else:
            context = self.get_context_data()
            context['image_form'] = form
            context['form_errors'] = True
            return self.render_to_response(context)


# Profile Update
class ProfileUpdateView(LoginRequiredMixin, FormView):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('user:profile_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


# Change Password
class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('user:profile_view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# Address
class AddressListVew(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = sorted(queryset, key=lambda address: not address.is_default)
        return queryset


class AddressCreateView(LoginRequiredMixin, CreateView):
    form_class = AddressCreateForm
    template_name = 'accounts/address_upsert.html'
    success_url = reverse_lazy('user:address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Address "{form.instance.name}" created successfully.')
            return response
        except IntegrityError:
            messages.error(self.request, f'Address with the name "{form.instance.name}" already exists.')
            return self.form_invalid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AddressCreateForm
    model = Address
    template_name = 'accounts/address_upsert.html'
    success_url = reverse_lazy('user:address_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'Address "{form.instance.name}" updated successfully.')
            return response
        except IntegrityError:
            messages.error(self.request, f'Address with the name "{form.instance.name}" already exists.')
            return self.form_invalid(form)


class AddressDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        address = get_object_or_404(Address, id=id, user=request.user)
        address.delete()
        return redirect('user:address_list')
    
    
class SetDefaultAddressView(View):
    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.is_default = True
        address.save()
        messages.success(request, f'Address {address.name} set as default successfully.')
        return redirect('user:address_list')
    
    
#Experience
class ExperienceListVew(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'accounts/experience_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = sorted(queryset, key=lambda experience: experience.start_date, reverse=True)
        return queryset
    

class ExperienceCreateView(LoginRequiredMixin, CreateView):
    form_class = ExperienceUpsertForm
    template_name = 'accounts/experience_upsert.html'
    success_url = reverse_lazy('user:experience_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{form.instance.title}" Added successfully.')
        return response
    
    
class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ExperienceUpsertForm
    model = Experience
    template_name = 'accounts/experience_upsert.html'
    success_url = reverse_lazy('user:experience_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'"{form.instance.title}" Added successfully.')
        return response


class ExperienceDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        experience = get_object_or_404(Experience, id=id, user=request.user)
        experience.delete()
        messages.success(self.request, f'"{experience.title}" deleted successfully.')
        return redirect('user:experience_list')
    
    
#Education
class EducationListVew(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'accounts/education_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        queryset = sorted(queryset, key=lambda education: education.start_date, reverse=True)
        return queryset
    

class EducationCreateView(LoginRequiredMixin, CreateView):
    form_class = EducationUpsertForm
    template_name = 'accounts/education_upsert.html'
    success_url = reverse_lazy('user:education_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Education Added successfully.')
        return response
    
    
class EducationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EducationUpsertForm
    model = Education
    template_name = 'accounts/education_upsert.html'
    success_url = reverse_lazy('user:education_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Education Added successfully.')
        return response


class EducationDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        education = get_object_or_404(Education, id=id, user=request.user)
        education.delete()
        messages.success(self.request, f'Education deleted successfully.')
        return redirect('user:education_list')
    
    
# UserSkill
class UserSkillListVew(LoginRequiredMixin, ListView):
    model = UserSkill
    template_name = 'accounts/skill_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    

class UserSkillCreateView(LoginRequiredMixin, CreateView):
    form_class = UserSkillUpsertForm
    template_name = 'accounts/skill_upsert.html'
    success_url = reverse_lazy('user:skill_list')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            response = super().form_valid(form)
            messages.success(self.request, f'"{form.instance.skill}" created successfully.')
            return response
        except IntegrityError:
            messages.error(self.request, f'"{form.instance.skill}" already exists.')
            return self.form_invalid(form)



class UserSkillDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        education = get_object_or_404(UserSkill, id=id, user=request.user)
        education.delete()
        messages.success(self.request, f'{education.skill} deleted successfully.')
        return redirect('user:skill_list')


class DeleteImageView(LoginRequiredMixin, View):
    def get(self, request, pk):
        image = get_object_or_404(UserImages, pk=pk)
        
        if image.user == request.user:
            image.delete()
            messages.success(request, 'Image deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this image.')
        
        return redirect(reverse_lazy('user:profile_view'))
    

# Add Hobby To User
class AddHobbyView(LoginRequiredMixin, CreateView):
    model = UserHobby
    form_class = UserHobbyAddForm
    template_name = 'accounts/hobby-add.html'
    success_url = reverse_lazy('user:profile_view')
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Hobby already exists in your profile.')
            return self.form_invalid(form)
        

# Delete Hobby of user
class DeleteHobbyView(LoginRequiredMixin, View):
    model = UserHobby
    success_url = reverse_lazy('user:profile_view')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        hobby_id = kwargs.get('id')
        hobby = get_object_or_404(UserHobby, id=hobby_id, user=self.request.user)
        hobby.delete()
        messages.success(request, 'Hobby deleted successfully.')
        return redirect('user:profile_view')
    

# Add Interest to User
class AddInterestView(LoginRequiredMixin, CreateView):
    model = UserInterest
    form_class = UserInterestAddForm
    template_name = 'accounts/interest-add.html'
    success_url = reverse_lazy('user:profile_view')
    
    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Interest already exists in your profile.')
            return self.form_invalid(form)


# Delete Interst from User
class DeleteInterestView(LoginRequiredMixin, View):
    model = UserInterest
    success_url = reverse_lazy('user:profile_view')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        interest_id = kwargs.get('id')
        interest = get_object_or_404(UserInterest, id=interest_id, user=self.request.user)
        interest.delete()
        messages.success(request, 'Interest deleted successfully.')
        return redirect('user:profile_view')