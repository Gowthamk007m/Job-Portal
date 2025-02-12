from django.urls import path
from .views import *


app_name = 'admin_panel'

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    # Login
    path("login/", LoginView.as_view(), name="login"),
    # Profile
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    # Users
    path("user/", UsersListView.as_view(), name="userslist"),
    path("user/detail/1", UserDetailView.as_view(), name="userdetail"),
    path("user/update/1", UserUpdateView.as_view(), name="userupdate"),
    path("user/create/", UserCreateView.as_view(), name="useradd"),
    # Company
    path("company/", CompaniesListView.as_view(), name="companylist"),
    path("company/update/1/", CompanyUpdateView.as_view(), name="companyupdate"),
    path("company/create/", CompanyAddView.as_view(), name="companycreate"),
    path("company/detail/1/", CompanyDetailView.as_view(), name="companydetail"),
    path("company/detail/1/applicant/", CompanyDetailApplicantListView.as_view(), name="company-applicant-list"),
    path("company/detail/1/scheduled-interview/", CompanyDetailInterviewListView.as_view(), name="company-interview-list"),
    # Job
    path("job/", JobListView.as_view(), name="job-list"),
    path("job/detail/1", JobDetailView.as_view(), name="job-detail"),
    path("job/detail/1/scheduled-interview/", JobDetailInterviewListView.as_view(), name="job-detail-interview"),
    path("job/update/1/", JobUpdateView.as_view(), name="job-update"),
    path("job/create/", JobCreateView.as_view(), name="job-create"),
]
