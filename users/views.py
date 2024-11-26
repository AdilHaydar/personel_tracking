from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SuperuserRequiredMixin, AnonymousRequiredMixin, EmployeeRequiredMixin


class AdminMainTemplateView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "admin/main.html"
    login_url = '/u/login/admin/'


class AdminLoginTemplateView(AnonymousRequiredMixin, TemplateView):
    template_name = "admin/login.html"


class EmployeeMainTemplateView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = "employee/main.html"
    login_url = '/u/login/employee/'


class EmployeeLoginTemplateView(AnonymousRequiredMixin, TemplateView):
    template_name = "employee/login.html"
    

class TakenAnnualLeaveTemplateView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    template_name = "employee/taken_annual_leave.html"
    login_url = '/u/login/employee/'


class AdminTakenAnnualLeaveTemplateView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "admin/taken_annual_leave.html"
    login_url = '/u/login/admin/'


class AdminAssignAnnualLeaveTemplateView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = "admin/assign_annual_leave.html"
    login_url = '/u/login/admin/'
    
    
class EmployeeRegisterTemplateView(AnonymousRequiredMixin, TemplateView):
    template_name = "employee/register.html"