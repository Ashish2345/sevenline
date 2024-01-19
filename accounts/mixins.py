from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from django.shortcuts import redirect

User = get_user_model()

class NonLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)
    

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('accounts:login')

    def dispatch(self,request,*args,**kwargs):
        if self.request.user.is_superuser or self.request.user.is_active:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()