from django.shortcuts import render
from datetime import datetime
import random

from .models import (LotteryResult, XcrossPictureUpload, VIPPictureUpload, 
                    PictureUpload1, PictureUpload2, PictureUpload3)

from django.views.generic import TemplateView


def generate_random_5_digit_number():
    return ''.join(str(random.randint(1, 9)) for _ in range(5))

class HomePageView(TemplateView):
    template_name = "sevenline_main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_img"] = LotteryResult.objects.order_by("-date").first().result_image if LotteryResult.objects.order_by("-date") else ""
        context["result_list"] = LotteryResult.objects.order_by("-date")[:12]
            
        context["latest_x_cross"] = XcrossPictureUpload.objects.first().picture if XcrossPictureUpload.objects.first() else ""
        context["latest_sasima"] = VIPPictureUpload.objects.first() if VIPPictureUpload.objects.first() else ""
        return context
    


class ContactPageView(TemplateView):
    template_name = "sevenline_main/contact_me.html"

    


class GeneralPageView(TemplateView):
    template_name = "sevenline_main/general/index.html"

class PreviewTipsPageView(TemplateView):
    template_name = "sevenline_main/preview_tip.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["picture_1"] = PictureUpload1.objects.first().picture if PictureUpload1.objects.first() else ""
        context["picture_2"] = PictureUpload2.objects.first().picture if PictureUpload2.objects.first() else ""
        context["picture_3"] = PictureUpload3.objects.first().picture if PictureUpload3.objects.first() else ""
            
       
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_result_count"] = LotteryResult.objects.order_by("-date").first().next_drawn_duration
        return context


class HowtoplayPageView(TemplateView):
    template_name = "puketsite/howtoplay.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_result"] = LotteryResult.objects.order_by("-date").first()
        return context

class MywalletplayPageView(TemplateView):
    template_name = "puketsite/mywallet.html"


class ResultPageView(TemplateView):
    template_name = "puketsite/result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_img"] = LotteryResult.objects.order_by("-date").first().result_image
        return context

class ContactMPageView(TemplateView):
    template_name = "puketsite/help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_img"] = LotteryResult.objects.order_by("-date").first().result_image
        context["result_list"] = LotteryResult.objects.order_by("-date")[:12]
        return context

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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["result_img"] = LotteryResult.objects.order_by("-date").first().result_image if LotteryResult.objects.order_by("-date") else ""
        context["result_list"] = LotteryResult.objects.order_by("-date")[:12]
            
        return context


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


class VipPaymentPageView(TemplateView):
    template_name = "sevenline_main/vip_payment.html"

