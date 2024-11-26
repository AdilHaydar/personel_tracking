from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from ..models import EmployeeInformation, AnnualLeave, TakenAnnualLeave
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import ListModelMixin
from .serializers import (EmployeeInformationSerializer, CustomLoginSerializer,
                        AnnualLeaveSerializer, TakenAnnualLeaveSerializer, UserSerializer, CustomRegisterSerializer)
from .paginations import DataTablePagination
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from ..enums import LoginType
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime
from django.conf import settings
from ..tasks import send_websocket_notify
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class UserViewSet(ViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

class EmployeeInformationGenericView(ListModelMixin, GenericViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = EmployeeInformationSerializer
    queryset = EmployeeInformation.objects.select_related('user').filter(user__last_login__day=(timezone.now() + timezone.timedelta(hours=3)).day, late_minute__gt=0)
    pagination_class = DataTablePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['id', 'user__first_name', 'user__last_login', 'late_hour']

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        path = self.request.path
        endpoint = path.split('/')[-2]
        context['login_type'] = LoginType.EMPLOYEE if endpoint == 'employee' else LoginType.ADMIN
        return context

    # def post(self, request, *args, **kwargs):
    #     context = self.get_serializer_context()
    #     result = super(CustomLoginView, self).post(request, *args, **kwargs)
    #     if context["login_type"] == LoginType.EMPLOYEE:
    #         self.login_log(request.user)
    #     return result
    
class CustomLogoutView(LogoutView):
    
    def post(self, request, *args, **kwargs):
        user = request.user
        super_return = super(CustomLogoutView, self).post(request, *args, **kwargs)
        current_datetime = timezone.now() + timezone.timedelta(hours=3)
        if not user.is_superuser:
            EmployeeInformation.objects.filter(user=user, user__last_login__day=current_datetime.day).update(logout_at=timezone.now())
        return super_return
            
class AnnualLeaveAdminView(RetrieveUpdateAPIView):
    serializer_class = AnnualLeaveSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        return AnnualLeave.objects.get(user=user)
    

class AnnualLeaveView(RetrieveAPIView):
    serializer_class = AnnualLeaveSerializer
    
    def get_object(self):
        user = self.request.user
        return AnnualLeave.objects.get(user=user)


class TakenAnnualLeaveView(ListCreateAPIView):
    serializer_class = TakenAnnualLeaveSerializer
    pagination_class = DataTablePagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return TakenAnnualLeave.objects.filter(is_approved=None)
        return TakenAnnualLeave.objects.filter(annual_leave__user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        annual_leave = AnnualLeave.objects.get(user=user)
        serializer.save(annual_leave=annual_leave)


class TakenAnnualLeaveCreateView(CreateAPIView):
    serializer_class = TakenAnnualLeaveSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        annual_leave = AnnualLeave.objects.get(user=user)
        instance = serializer.save(annual_leave=annual_leave)
        if instance.is_approved:
            annual_leave.leave_taken += instance.leave_duration
            annual_leave.save()

class TakenAnnualLeaveUpdateView(UpdateAPIView):
    serializer_class = TakenAnnualLeaveSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        pk = self.kwargs.get('taken_id')
        return TakenAnnualLeave.objects.get(id=pk)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_approved:
            annual_leave = instance.annual_leave
            annual_leave.leave_taken += instance.leave_duration
            annual_leave.save()
