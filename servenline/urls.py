from django.urls import path

from .views import (HomePageView, ContactPageView, ServicePageView, GeneralPageView,
                    PreviewTipsPageView, GraphTipsPageView, SignupPageView, LoginPageView,
                    PwResetPageView,
                    IndexMPageView, HowtoplayPageView, MywalletplayPageView, ResultPageView,
                    ContactMPageView, Login2PageView, RegisterPageView, PassRstPageView,
                    AbsStat1PageView, AbsStat2PageView, AbsStat2UpPageView, AbsStat3PageView,
                    Result1PageView, StatPageView, VipPaymentPageView
                    )

app_name= "servenline"

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('contact_me.php', ContactPageView.as_view(), name="contact_page"),
    
    path('general', GeneralPageView.as_view(), name="general"),
    path('preview_tip.php', PreviewTipsPageView.as_view(), name="preview_tip"),
    path('graph_tip.php', GraphTipsPageView.as_view(), name="graph_tip"),
    path('services.php', ServicePageView.as_view(), name="services"),

    path('sign_up.php', SignupPageView.as_view(), name="signup"),
    path('login.php', LoginPageView.as_view(), name="login"),
    path('pw_reset.php', PwResetPageView.as_view(), name="pw_reset"),

    #puketindex
    path('index_m.php', IndexMPageView.as_view(), name="index_m"),
    path('howtoplay.php', HowtoplayPageView.as_view(), name="howtoplay"),
    path('deposit_member_btc.php', MywalletplayPageView.as_view(), name="mywalletaddress"),
    path('result_m.php', ResultPageView.as_view(), name="result_m"),
    path('contact_m.php', ContactMPageView.as_view(), name="contact_m"),
    path('login2_m.php', Login2PageView.as_view(), name="login2_m"),
    path('regist_m.php', RegisterPageView.as_view(), name="regist_m"),
    path('reset_pw_m.php', PassRstPageView.as_view(), name="reset_pw_m"),

    #general
    path('result.php', Result1PageView.as_view(), name="result1"),
    path('stat.php', StatPageView.as_view(), name="stat"),
    path('abs_stat1.php', AbsStat1PageView.as_view(), name="abs_stat1"),
    path('abs_stat2.php', AbsStat2PageView.as_view(), name="abs_stat2"),
    path('abs_stat2up.php', AbsStat2UpPageView.as_view(), name="abs_stat2up"),
    path('abs_stat3.php', AbsStat3PageView.as_view(), name="abs_stat3"),

    # Extra
    path('vip_payment.php', VipPaymentPageView.as_view(), name="vip_payment"),




]
