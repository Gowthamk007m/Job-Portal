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

#####API Imports########################
from rest_framework import routers, serializers, viewsets
from . serializers import *

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

#///////////////////////////////////API VIEWS//////////////////////////#

# class LoginAPIView(viewsets.ModelViewSet):
#     queryset=CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "email": user.email,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # If authentication is successful, generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "email": user.email,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'No token provided'}, status=400)

    user = authenticate(request, token=token)
    if user:
        # Generate JWT or perform any other necessary steps
        return Response({'token': 'YOUR_JWT_TOKEN'})
    return Response({'error': 'Authentication failed'}, status=401)

def authenticate(request, token):
    try:
        backend = 'social_core.backends.google.GoogleOAuth2'
        user = psa(backend)(request)
        return user
    except Exception as e:
        return None