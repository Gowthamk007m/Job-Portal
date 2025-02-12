from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'admin_panel/index.html'

class LoginView(TemplateView):
    template_name = 'admin_panel/login.html'

class ProfileView(TemplateView):
    template_name = 'admin_panel/pages/profile/profile.html'

class ProfileEditView(TemplateView):
    template_name = 'admin_panel/pages/profile/edit-profile.html'

class UsersListView(TemplateView):
    template_name = 'admin_panel/pages/user/userslist.html'

class UserUpdateView(TemplateView):
    template_name = 'admin_panel/pages/user/edit-user.html'

class UserCreateView(TemplateView):
    template_name = 'admin_panel/pages/user/add-user.html'

class UserDetailView(TemplateView):
    template_name = 'admin_panel/pages/user/user-detail.html'

class CompaniesListView(TemplateView):
    template_name = 'admin_panel/pages/company/companieslist.html'

class CompanyAddView(TemplateView):
    template_name = 'admin_panel/pages/company/add-company.html'

class CompanyUpdateView(TemplateView):
    template_name = 'admin_panel/pages/company/update-company.html'

class CompanyDetailView(TemplateView):
    template_name = 'admin_panel/pages/company/company-detail.html'

class CompanyDetailInterviewListView(TemplateView):
    template_name = 'admin_panel/pages/company/company-detail-interview.html'

class CompanyDetailApplicantListView(TemplateView):
    template_name = 'admin_panel/pages/company/company-detail-applicant-list.html'

class JobListView(TemplateView):
    template_name = 'admin_panel/pages/job/job-list.html'

class JobDetailView(TemplateView):
    template_name = 'admin_panel/pages/job/job-detail.html'

class JobDetailInterviewListView(TemplateView):
    template_name = 'admin_panel/pages/job/job-detail-schedule.html'

class JobCreateView(TemplateView):
    template_name = 'admin_panel/pages/job/add-job.html'

class JobUpdateView(TemplateView):
    template_name = 'admin_panel/pages/job/job-edit.html'