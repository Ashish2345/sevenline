from django.shortcuts import render


from .models import LotteryResult

from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = "sevenline_main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_img"] = LotteryResult.objects.order_by("-date").first().result_image
        context["result_list"] = LotteryResult.objects.order_by("-date")[:12]
        return context
    


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


###############################################################
#puketindex
###############################################################


class IndexMPageView(TemplateView):
    template_name = "puketsite/indexm.html"


class HowtoplayPageView(TemplateView):
    template_name = "puketsite/howtoplay.html"

class MywalletplayPageView(TemplateView):
    template_name = "puketsite/mywallet.html"


class ResultPageView(TemplateView):
    template_name = "puketsite/result.html"

class ContactMPageView(TemplateView):
    template_name = "puketsite/help.html"

class Login2PageView(TemplateView):
    template_name = "puketsite/login.html"

class RegisterPageView(TemplateView):
    template_name = "puketsite/signup.html"


class PassRstPageView(TemplateView):
    template_name = "puketsite/pass_rst.html"



###############################################################
#General index
###############################################################




class Result1PageView(TemplateView):
    template_name = "general_pg/result.html"




class StatPageView(TemplateView):
    template_name = "general_pg/stat.html"

class AbsStat1PageView(TemplateView):
    template_name = "general_pg/abs_stat1.html"


class AbsStat2PageView(TemplateView):
    template_name = "general_pg/abs_stat2.html"

class AbsStat2UpPageView(TemplateView):
    template_name = "general_pg/abs_stat2up.html"


class AbsStat3PageView(TemplateView):
    template_name = "general_pg/abs_stat3.html"
