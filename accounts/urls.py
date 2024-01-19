from django.urls import path

from .views import (LoginView, resend_otp_code, LogoutView, SignUpView, send_otp_code, EmailVerifyView,RecoverPasswordView,
                    RecoverPasswordVerifyView,AuditTrailListView,  RecoverResetView, PasswordChangeView,
                    DashboardView
                    )

app_name= "accounts"

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('resend/otp/', resend_otp_code, name="resend-otp"),
    path('verify-email/', EmailVerifyView.as_view(), name="verify-email"),
    path('recover/password/', RecoverPasswordView.as_view(), name="recover-pass"),
    path('recover/password/verify/', RecoverPasswordVerifyView.as_view(), name="recover-pass-verify"),
    path('recover/reset/<str:uidb64>/', RecoverResetView.as_view(), name="pass-reset"),
    path('change/password/<int:pk>/', PasswordChangeView.as_view(), name="change-password"),
    path('audits/', AuditTrailListView.as_view(), name='audittrail-list'),

    #Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
