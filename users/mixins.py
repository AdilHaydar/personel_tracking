from django.http import HttpResponseForbidden


class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)
    
class EmployeeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)
    
class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden("You are not allowed to access this page.")
        return super().dispatch(request, *args, **kwargs)