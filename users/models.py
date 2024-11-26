from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
# Create your models here.

class EmployeeInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='login_informations')
    logout_at = models.DateTimeField(null=True, blank=True)
    late_minute = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        
        
class AnnualLeave(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='annual_leave')
    total_leave = models.DurationField(default=timedelta(days=15))
    leave_taken = models.DurationField(default=timedelta(days=0))
    total_late_minute = models.DurationField(default=timedelta(days=0, hours=0, minutes=0))
    notify_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        
    def get_remaining_leave(self):
        return self.total_leave - self.leave_taken - self.total_late_minute
    

class TakenAnnualLeave(models.Model):
    annual_leave = models.ForeignKey(AnnualLeave, on_delete=models.CASCADE, related_name='taken_leaves')
    leave_duration = models.DurationField()
    description = models.TextField()
    is_approved = models.BooleanField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
    
    