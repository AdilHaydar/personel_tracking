from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import EmployeeInformation, AnnualLeave, TakenAnnualLeave
from ..enums import LoginType
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .serializer_fields import LeaveDurationField
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'first_name', 'last_name', 'last_login')

class EmployeeInformationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = EmployeeInformation
        fields = ('__all__')

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(
        required=True,
        write_only=True,
        validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    username = None

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }
        
class CustomLoginSerializer(LoginSerializer):
    username = None
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError(_("Email or password is incorrect."), code='authorization')
        else:
            raise serializers.ValidationError(_("Email and password fields are required."), code='authorization')

        attrs['user'] = user
        return attrs

    def authenticate(self, **kwargs):
        login_type = self.context['login_type']
        auth_user = authenticate(self.context['request'], **kwargs)
        if auth_user and auth_user.is_superuser and not (login_type == LoginType.ADMIN):
            raise serializers.ValidationError('Admin user cannot login here.')
        if auth_user and not auth_user.is_superuser and not (login_type == LoginType.EMPLOYEE):
            raise serializers.ValidationError('Employee user cannot login here.')
        return auth_user
    
    


    
class TakenAnnualLeaveSerializer(serializers.ModelSerializer):
    annual_leave = serializers.PrimaryKeyRelatedField(read_only=True)
    leave_duration = LeaveDurationField()
    user = UserSerializer(source='annual_leave.user', read_only=True)


    class Meta:
        model = TakenAnnualLeave
        exclude = ('updated_at',)
        
    def validate(self, data):
        if self.context["request"].user.annual_leave.get_remaining_leave() < data['leave_duration']:
            raise serializers.ValidationError('Not enough leave to take.')
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_staff and 'is_approved' in validated_data:
            validated_data.pop('is_approved', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request.user.is_staff and 'is_approved' in validated_data:
            validated_data.pop('is_approved', None)
        return super().update(instance, validated_data)
    
    
class AnnualLeaveSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    remaining_leave = serializers.SerializerMethodField()
    taken_leaves = TakenAnnualLeaveSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnnualLeave
        exclude = ('created_at', 'updated_at')
        
    def get_remaining_leave(self, obj):
        remaining_time = obj.get_remaining_leave()
        
        total_seconds = int(remaining_time.total_seconds())
        days = total_seconds // (24 * 3600)
        total_seconds %= (24 * 3600)
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60

        return {
            "days": days,
            "hours": hours,
            "minutes": minutes
        }
    