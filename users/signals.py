from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import AnnualLeave, EmployeeInformation
from .tasks import send_websocket_notify
from datetime import datetime

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:  
        AnnualLeave.objects.create(user=instance)

@receiver(post_save, sender=AnnualLeave)
def notify_annual_leave_signal(sender, instance, created, **kwargs):
    if not created:
        if instance.get_remaining_leave().days < 3 and not instance.notify_sent:
            instance.notify_sent = True
            # post_save.disconnect(notify_annual_leave_signal, sender=AnnualLeave)
            instance.save()
            # post_save.connect(notify_annual_leave_signal, sender=AnnualLeave)
            send_websocket_notify.delay('notify_group', 
                                        {'notify': f'{instance.user.first_name} {instance.user.last_name} remaining leave is less than 3 days.'}) 
            
def update_annual_leave(user, time_difference):
    print("***UPDATE ANNUAL LEAVE***")
    annual_leave = AnnualLeave.objects.get(user=user)
    annual_leave.total_late_minute += time_difference
    annual_leave.save()
    

def login_log(user):
    print("LOGIN LOG")
    current_datetime = timezone.now() + timezone.timedelta(hours=3)
    if current_datetime.weekday() in [5, 6]:
        return
        
    if not EmployeeInformation.objects.filter(user=user, created_at__day=current_datetime.day).exists():
        late_minute = 0
        if user.last_login.day == current_datetime.day:
            manual_time = settings.START_TIME
            if (user.last_login + timezone.timedelta(hours=3)).time() > manual_time:
                manual_datetime = timezone.make_aware(datetime.combine(current_datetime.date(), manual_time))
                time_difference = user.last_login - manual_datetime
                late_minute = time_difference.seconds // 60
                
                update_annual_leave(user, time_difference)
                
                send_websocket_notify.delay('notify_group', 
                                            {'notify': f'{user.first_name} {user.last_name} is late {late_minute} minutes.'})
                
        EmployeeInformation.objects.create(user=user, late_minute=late_minute)
    
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if not user.is_superuser:
        login_log(user)