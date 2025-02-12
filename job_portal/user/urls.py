from django.urls import path
from .views import *


app_name = "user"

urlpatterns = [
    
    # Auth
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path('complete-registration/', RegisterCompleteView.as_view(), name='profile_add'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    
    # Profile
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('add_hobby/', AddHobbyView.as_view(), name='add_hobby'),
    path('delete_hobby/<id>/', DeleteHobbyView.as_view(), name='delete_hobby'),
    path('add_interest/', AddInterestView.as_view(), name='add_interest'),
    path('delete_interest/<id>/', DeleteInterestView.as_view(), name='delete_interest'),
    path('delete_image/<int:pk>/', DeleteImageView.as_view(), name='delete_image'),
    
    # Address
    path('address/', AddressListVew.as_view(), name='address_list'),
    path('address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/update/<id>/', AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<id>/', AddressDeleteView.as_view(), name='address_delete'),
    path('address/set-default/<int:pk>/', SetDefaultAddressView.as_view(), name='set_default_address'),
    
    # Experience
    path('experience/', ExperienceListVew.as_view(), name='experience_list'),
    path('experience/create/', ExperienceCreateView.as_view(), name='experience_create'),
    path('experience/update/<id>/', ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience/delete/<id>/', ExperienceDeleteView.as_view(), name='experience_delete'),
    
    # Education
    path('education/', EducationListVew.as_view(), name='education_list'),
    path('education/create/', EducationCreateView.as_view(), name='education_create'),
    path('education/update/<id>/', EducationUpdateView.as_view(), name='education_edit'),
    path('education/delete/<id>/', EducationDeleteView.as_view(), name='education_delete'),
    
    # Skill
    path('skill/', UserSkillListVew.as_view(), name='skill_list'),
    path('skill/create/', UserSkillCreateView.as_view(), name='skill_create'),
    path('skill/delete/<id>/', UserSkillDeleteView.as_view(), name='skill_delete'),
    
    # Reset Password
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/validate/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset_password_validate"),
]