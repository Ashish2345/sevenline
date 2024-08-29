from django.shortcuts import render

from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = "sevenline_main/index.html"


class ContactPageView(TemplateView):
    template_name = "sevenline_main/contact_me.html"


class GeneralPageView(TemplateView):
    template_name = "sevenline_main/general/index.html"

class PreviewTipsPageView(TemplateView):
    template_name = "sevenline_main/preview_tip.html"

class GraphTipsPageView(TemplateView):
    template_name = "sevenline_main/graph_tip.html"

class ServicePageView(TemplateView):
    template_name = "sevenline_main/services.html"

class SignupPageView(TemplateView):
    template_name = "sevenline_main/sign_up.html"

class LoginPageView(TemplateView):
    template_name = "sevenline_main/login.html"


class PwResetPageView(TemplateView):
    template_name = "sevenline_main/pw_reset.html"