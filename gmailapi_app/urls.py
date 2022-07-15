
from django.urls import path
from . import views
urlpatterns = [
    path('sendMail',views.sendMail,name="sendmail"),
    path('',views.index,name="index")
]
