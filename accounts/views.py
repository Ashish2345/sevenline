import subprocess

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse_lazy
from django.contrib import messages


from .mixins import NonLoginRequiredMixin

from .forms import (LoginForm, PasswordChangeForm, ProfileForm, SignupForm,
            NewPasswordform,)

from .models import Otp, User

from .email_send import _sendOtp

from .utils import store_audit, rate_limit

# from axes.decorators import axes_dispatch
from django.utils.decorators import method_decorator

from .encryption import _encrypt
from .utils import OTPEncryptionDec, TokenEncodeDecode


from braces.views import LoginRequiredMixin




# @method_decorator(axes_dispatch, name='dispatch')
class LoginView(NonLoginRequiredMixin, View):
    template_name = "authentication/login.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": LoginForm()})
    
    def post(self, request, *args, **kwargs):
        post_dict = self.request.POST.dict()
        form = LoginForm(data={**post_dict})
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_verified_email == True:
                    login(request, user)
                    store_audit(instance=user, action='Logged in Successfully')
                    if not request.POST.get('remember_me'):
                        request.session.set_expiry(0)
                    return redirect("accounts:dashboard")
                else:
                    request.session['email'] = user.email
                    return redirect("accounts:verify-email")
            else:
                return render(request, self.template_name, {'form': LoginForm(), 'msg_error': 'Invalid Email and/or Password'})
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


def resend_otp_code(request):

    rate_limit(request)
    if request.session.get('new_email', None):
        user_email = request.session.get('new_email', None)
    else:
        user_email = request.session['email']
    otp_enc = OTPEncryptionDec()
    user_email = User.objects.filter(is_active=True, email=user_email).exists()
    if user_email:
        entry = Otp.objects.filter(email=user_email).order_by('created_date').last()
        if not entry or (entry and entry.is_otp_valid is False):
    
            otp_dict = otp_enc._encrypt_otp()
            entry = Otp.objects.create(email=user_email.email, otp=otp_dict["encrypted_otp"])

        _sendOtp(to=entry.email, context={'name':'User', 'otp':otp_dict["otp"], "title": 'Recover Your Password', "desc":'Your Password Reset Code is'},  template='mail/password-reset.html', purpose='Recover Password')
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def send_otp_code(request, mail_info):

    otp_enc = OTPEncryptionDec()
    if request.session.get('new_email', None):
        user_email = request.session.get('new_email', None)
    else:
        user_email = request.session['email']
    user_email = User.objects.filter(is_active=True, email=user_email).first()
    if user_email:
        entry = Otp.objects.filter(email=user_email).order_by('created_date').last()
        if not entry or (entry and entry.is_otp_valid is False):
            otp_dict = otp_enc._encrypt_otp()
            entry = Otp.objects.create(email=user_email.email, otp=otp_dict["encrypted_otp"])

        _sendOtp(to=entry.email, context={'name':'User', 'otp':otp_dict["otp"], "title": mail_info['title'], "desc":mail_info['description']},  template='mail/password-reset.html', purpose=mail_info['purpose'])
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


class SignUpView(NonLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "authentication/signup.html"
        self.args = {
            "form": SignupForm()
        }
        if self.request.method == "POST":
            self.args['form'] = SignupForm(self.request.POST)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.args)

    @transaction.atomic
    def post(self ,request, *args, **kwargs):
        rate_limit(request)
        form = self.args['form']
        if form.is_valid():
            m = form.save(commit=False)
            m.set_password(form.cleaned_data.get('password1'))
            m.save()
            request.session['email'] = m.email
            return redirect("accounts:verify-email")
        else:
            return render(request, self.template_name, {'form': form})


class EmailVerifyView(View):

    def dispatch(self, request, *args, **kwargs):
        self.template_name = "authentication/email-verify.html"
        self.user_email = request.session.get('email', None)
        self.new_email = request.session.get('new_email', None)
        self.user_obj = User.objects.filter(email=self.user_email, is_active=True).first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        if self.user_email or self.new_email:
            if self.new_email:
                user_email = self.new_email
            else:
                user_email = self.user_email
           
            if self.user_obj:
                send_otp_code(request, {"title": "Verify your email", "description":"Your Email Verification Code is", "purpose":"Email Verify"})
            self.args = {
                "email":user_email
            }
            return render(request, self.template_name, self.args)
        else:
            return redirect("accounts:login")

    def post(self, request, *args, **kwargs):
        user_code = request.POST.get("otp")
        otp_dec_validate = OTPEncryptionDec()

        
        if self.new_email:
            otp_qs = Otp.objects.filter(email=self.new_email).order_by('created_date').last()
        else:
            otp_qs = Otp.objects.filter(email=self.user_obj.email).order_by('created_date').last()

        get_otp_value = otp_dec_validate._decrypt_otp(otp_qs.otp)
        if not otp_qs or (otp_qs and (otp_qs.is_otp_valid is False or get_otp_value != str(user_code))):
            return JsonResponse({"success": False, "message": "Invalid OTP!!"})
        else:
            Otp.objects.filter(email=self.new_email).delete()
            if self.new_email:
                self.user_obj.email = self.new_email
                self.user_obj.is_verified_email = True
                self.user_obj.save()
                del request.session['email'] 
                del request.session['new_email'] 
                store_audit(request= self.request, instance=self.user_obj, action=f'Email Verified Successfully!!')
            else:
                self.user_obj.is_verified_email = True
                self.user_obj.save()
                del request.session['email'] 
            return JsonResponse({"success": True, "message": "Your email is successfully verified. Now you can login to your accounts. "})


class RecoverPasswordView(NonLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "authentication/recover_password.html"
        self.args = {
        }
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):	
        return render(request, self.template_name, self.args)

    def post(self, request, *args, **kwargs):
        rate_limit(request)
        request.session['email'] = request.POST.get("email")
        exists_user = User.objects.filter(email=request.session['email']).exists()
        if exists_user:
            send_otp_code(request, {"title": "Recover Your Password", "description":"Your Password Reset Code is", "purpose":"Recover Password"})
        return redirect("accounts:recover-pass-verify")


class RecoverPasswordVerifyView(NonLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "authentication/email-verify.html"
        self.user_email = request.session['email']
        self.user_obj = User.objects.filter(is_active=True, email=self.user_email).first()
        # get_object_or_404(User.objects.filter(is_active=True), email=self.user_email)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.args = {
            "email":request.session['email'],
            "recover_pass": True
        }
        return render(request, self.template_name, self.args)

    def post(self, request, *args, **kwargs):
        rate_limit(request)
        user_code = request.POST.get("otp")
        if self.user_obj:
            
            otp_qs = Otp.objects.filter(email=self.user_obj.email).order_by('created_date').last()
            otp_dec_validate = OTPEncryptionDec()
            get_otp_value = otp_dec_validate._decrypt_otp(otp_qs.otp)
            if not otp_qs or (otp_qs and (otp_qs.is_otp_valid is False or get_otp_value != str(user_code))):
                return JsonResponse({"success": False, "message": "Invalid OTP!!"})
            else:
                Otp.objects.filter(email=self.user_obj.email).delete()
                user = self.user_obj
                primarykey = user.id
                uid = urlsafe_base64_encode(force_bytes(primarykey))
                response={
                    'success_url': reverse_lazy('accounts:pass-reset', kwargs={'uidb64': uid})
                }
                return JsonResponse({"success": True, "message": "Success OTP!!","success_url":response})
        else:
                return JsonResponse({"success": False, "message": "OTP Invalid"})



class RecoverResetView(NonLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "authentication/password_reset.html"
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        form = NewPasswordform()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            return render(request, self.template_name)
        else:
            return render(request, 'authentication/recover-pass.html')

    def post(self, request, *args, **kwargs):
        rate_limit(request)
        uidb64 = kwargs.get("uidb64")
        data_dict = request.POST.dict()
        form = NewPasswordform(data={**data_dict})
        if form.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            pass1 = form.cleaned_data['password']
            user.set_password(pass1)
            user.save()
            return render(request, self.template_name, {"recovered":True})
        else:
            return render(request, self.template_name, {"form":form})


# class ProfileView(LoginRequiredMixin, View):
# 	def dispatch(self, request, *args, **kwargs):
# 		self.template_name = "authentication/profile.html"
# 		id = self.kwargs.get("pk")
        
# 		user_obj= get_object_or_404(User,id = id)
# 		profile_obj =  user_obj.user_profile
# 		self.check_permission(user_obj, user_obj)
# 		form = ProfileForm(instance=profile_obj)
# 		signup_form = UserProfileSignupForm(instance = user_obj)
# 		email_change_form = EmailChangeForm()
# 		contact_no = profile_obj.contact_no
# 		self.args = {
# 			"user_id": id,
# 			"form": form,
# 			"profile_obj": profile_obj,
# 			"user_obj": user_obj,
# 			"signup_form": signup_form,
# 			'contact_no': contact_no,
# 			"breadscumb":self.getbreadscumb(currentname= "Profile"), 
# 			"email_change_form":email_change_form
# 		}
# 		return super().dispatch(request, *args, **kwargs)
    
# 	def get(self, request, *args, **kwargs):
# 		return render(request, self.template_name, self.args)

# 	def post(self, request, *args, **kwargs):
# 		profile = self.args['profile_obj']
# 		user = self.args['user_obj']
# 		form = ProfileForm(request.POST, instance = profile)
# 		form2 = UserProfileSignupForm(request.POST, instance = user)
# 		previous_number = profile.contact_no
# 		if form.is_valid() and form2.is_valid():
            
# 			if previous_number != form.cleaned_data['contact_no']:
# 				exists_number = Profile.objects.filter(contact_no=form.cleaned_data['contact_no']).exists()
# 				if exists_number:
# 					messages.error(request, "Number already taken")
# 					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# 				profile.is_verified_contact = False
# 			user.save()
# 			profile.save()
# 			store_audit(request= self.request, instance=profile, action=f'Profile Updated Successfully')
# 			messages.success(request, "Profile Updated Successfully")
            
# 		else:
# 			messages.error(request, "Error Updating Profile")
# 		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PasswordChangeView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "change_password.html"
        id = kwargs.get("pk")
        form = PasswordChangeForm()
        self.args = {
            "form": form,
            "user_id": id,	
        }
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.args)
    
    def post(self, request, *args, **kwargs):
        rate_limit(request)
        form= PasswordChangeForm(request.POST)
        form.set_user(request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get("password1")
            user = request.user
            user.set_password(new_password)
            user.save()
            context = {
                "title": "Password",
                "message": 'Password Changed Successfully'
            }
            store_audit(request= self.request, instance=user, action=context['title'])
            messages.success(request, "Password changed successfully!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            self.args = {
                'form':form,
                "user_id": self.args["user_id"],
            }
            return render(request, self.template_name, self.args)

from .models import AuditTrail
from django.views.generic import ListView

class AuditTrailListView(LoginRequiredMixin, ListView):
    model = AuditTrail
    template_name = "auditrials.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user").filter(user=self.request.user).order_by('-created_at')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DashboardView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        self.template_name = "base/index.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class LogoutView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect('accounts:login')