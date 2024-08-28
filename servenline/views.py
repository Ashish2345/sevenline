from django.shortcuts import render

from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = "sevenline_main/index.html"


class ContactPageView(TemplateView):
    template_name = "sevenline_main/contact_me.html"

    