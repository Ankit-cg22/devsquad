from django.urls import path
from . import views #importing the views file of this same app 

urlpatterns = [
    path('' , views.home , name = "home" ) ,  # here we declare that whenever anyone hits ""(home url) run the home function
    path('squad/<str:pk>/' , views.squad , name = "squad") , 
]
