from django.urls import re_path 
from rest_api import views

#set url that receiving http post request
urlpatterns = [
    re_path(r'^dataUpload$',views.dataUpload),
    re_path(r'^output$',views.output),
]