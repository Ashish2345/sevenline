from django.urls import path

from .views import (HomePageView, ContactPageView)

app_name= "servenline"

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('contact_me.php', ContactPageView.as_view(), name="contact_page"),
   

]
