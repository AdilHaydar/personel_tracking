from django.urls import path
from . import views
urlpatterns = [
    path('main/admin/', views.AdminMainTemplateView.as_view(), name='admin_main'),
    path('login/admin/', views.AdminLoginTemplateView.as_view(), name='admin_login'),
    path('main/employee/', views.EmployeeMainTemplateView.as_view(), name='employee_main'),
    path('login/employee/', views.EmployeeLoginTemplateView.as_view(), name='employee_login'),
    path('taken_annual_leave/', views.TakenAnnualLeaveTemplateView.as_view(), name='taken_annual_leave'),
    path('taken_annual_leave/admin/', views.AdminTakenAnnualLeaveTemplateView.as_view(), name='admin_taken_annual_leave'),
    path('assign_annual_leave/', views.AdminAssignAnnualLeaveTemplateView.as_view(), name='admin_assign_annual_leave'),
]