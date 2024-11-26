from django.urls import path, include
from .views import CustomLoginView, EmployeeInformationGenericView, CustomLogoutView, AnnualLeaveView, AnnualLeaveAdminView, TakenAnnualLeaveView, TakenAnnualLeaveUpdateView, UserViewSet, TakenAnnualLeaveCreateView, CustomRegisterView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'login-logs', EmployeeInformationGenericView, basename='login-logs')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/employee/', CustomRegisterView.as_view(), name='register_employee'),
    path('login/employee/', CustomLoginView.as_view() ,name='login_employee'),
    path('login/admin/', CustomLoginView.as_view() ,name='login_admin'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('annual-leave/', AnnualLeaveView.as_view(), name='annual_leave'),
    path('annual-leave/<int:user_id>/', AnnualLeaveAdminView.as_view(), name='annual_leave_admin'),
    path('taken-annual-leave/', TakenAnnualLeaveView.as_view(), name='taken_annual_leave'),
    path('taken-annual-leave/<int:taken_id>/', TakenAnnualLeaveUpdateView.as_view(), name='taken_annual_leave_update'),
    path('taken-annual-leave-admin/<int:user_id>/', TakenAnnualLeaveCreateView.as_view(), name='taken_annual_leave_user'),
]