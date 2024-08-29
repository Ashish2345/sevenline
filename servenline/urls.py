from django.urls import path

from .views import (HomePageView, ContactPageView, ServicePageView, GeneralPageView,
                    PreviewTipsPageView, GraphTipsPageView, SignupPageView, LoginPageView,
                    PwResetPageView
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
   

]
