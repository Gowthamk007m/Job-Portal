# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect, render
# from django.urls import reverse, reverse_lazy
# from django.views.generic import TemplateView
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import authenticate, login
# from.mixin import *
# from .models import *
# from .forms import CustomUserCreationForm, LoginForm,ActivitiesForm,QualificationsForm,DetailsForm
# from django.contrib import messages
# from django.views.generic import CreateView,UpdateView,ListView,TemplateView
# from django.views import View
# from django.contrib.auth import logout 

# #####API Imports########################
# from rest_framework import routers, serializers, viewsets
# from . serializers import *

# class RegisterView(SuccessMessageMixin, CreateView):
#     template_name = 'auth/register.html'
#     form_class = CustomUserCreationForm

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return HttpResponseRedirect(reverse('accounts:create_details', kwargs={'id': user.id}))


# class LoginView(View):
#     form_class = LoginForm
#     template_name = 'auth/login.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {'form': self.form_class()})

#     def post(self, request):
#         form = self.form_class(data=request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('jobs:home')
#             else:
#                 form.add_error(None, "Invalid email or password.")
#                 return render(request, self.template_name, {'form': form})


# class ForgotPasswordView(TemplateView):
#     template_name = 'auth/forgot_password.html'



# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('accounts:login')


# class DetailsCreateView(LoginRequiredMixin, UpdateView):
#     model=CustomUser
#     form_class = DetailsForm
#     template_name = 'users/complete_profile.html'
#     success_url = reverse_lazy('accounts:create_activities')
#     pk_url_kwarg = 'id'

#     def get_queryset(self):
#         return CustomUser.objects.filter(username=self.request.user.username)
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class ActivitiesCreateView(LoginRequiredMixin, CreateView):
#     form_class = ActivitiesForm
#     template_name = 'users/user_activities.html'
#     success_url = reverse_lazy('accounts:create_qualifications')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
# class QualificationsCreateView(LoginRequiredMixin, CreateView):
#     form_class = QualificationsForm
#     template_name = 'users/user_qualifications.html'
#     success_url = reverse_lazy('accounts:role')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    

# # class UserHobbyUpdateView(UpdateView):
# #     model = UserHobby
# #     form_class = UserHobbyForm
# #     template_name = 'user_hobby_form.html'
# #     context_object_name = 'user_hobby'

# #     def get_object(self):
# #         user_id = self.kwargs.get('user_id')
# #         user_hobby, created = UserHobby.objects.get_or_create(user_id=user_id)
# #         return user_hobby

# #     def get_success_url(self):
# #         return reverse_lazy('some_view_name')

# class Role(LoginRequiredMixin, TemplateView):
#     template_name = 'users/role.html'

# #///////////////////////////////////API VIEWS//////////////////////////#

# # class LoginAPIView(viewsets.ModelViewSet):
# #     queryset=CustomUser.objects.all()

# # class RegisterAPIView(APIView):
# #     permission_classes = [AllowAny]
# #     def post(self, request, *args, **kwargs):
# #         serializer = CustomUserSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save()
# #             refresh = RefreshToken.for_user(user)
# #             return Response({
# #                 "user_id": user.id,
# #                 "email": user.email,
# #                 "access_token": str(refresh.access_token),
# #                 "refresh_token": str(refresh)
# #             }, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# # class LoginAPIView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request, *args, **kwargs):
# #         email = request.data.get('email')
# #         password = request.data.get('password')

# #         # Authenticate the user
# #         user = authenticate(request, username=email, password=password)

# #         if user is not None:
# #             # If authentication is successful, generate tokens
# #             refresh = RefreshToken.for_user(user)
# #             return Response({
# #                 "user_id": user.id,
# #                 "email": user.email,
# #                 "access_token": str(refresh.access_token),
# #                 "refresh_token": str(refresh)
# #             }, status=status.HTTP_200_OK)
# #         else:
# #             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.utils import timezone
import datetime
import json
from social_django.models import UserSocialAuth
from django.conf import settings

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            # Verify the token using Google API
            id_info = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)

            # Get user info from token
            email = id_info.get('email')
            name = id_info.get('name')

            # Use the custom user model
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email, defaults={'username': email, 'first_name': name})

            social_user, social_created = UserSocialAuth.objects.get_or_create(
                user=user,
                provider='google-oauth2',
                uid=id_info['sub'],  # Use the 'sub' field from the ID token as UID
                defaults={'extra_data': id_info}
        )

            # Generate tokens using Django OAuth Toolkit
            application = Application.objects.get(name='JobPortal')  # Use your application name

            # Create access token
            expires = timezone.now() + datetime.timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            access_token = AccessToken.objects.create(
                user=user,
                application=application,
                token=generate_token(),
                expires=expires,
                scope='read write'
            )

            # Create refresh token
            refresh_token = RefreshToken.objects.create(
                user=user,
                token=generate_token(),
                application=application,
                access_token=access_token
            )

            # Return user info and tokens
            return JsonResponse({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email,
                'access_token': access_token.token,
                'refresh_token': refresh_token.token
            })
        except ValueError as e:
            # Invalid token
            return JsonResponse({'error': 'Invalid token'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
