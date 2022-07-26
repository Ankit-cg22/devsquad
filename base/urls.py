from django.urls import path
from . import views  # importing the views file of this same app

urlpatterns = [
    # here we declare that whenever anyone hits ""(home url) run the home function
    path('', views.home, name="home"),
    path('squad/<str:pk>/', views.squad, name="squad"),
    path('create-squad/', views.createSquad, name="create-squad"),
    path('update-squad/<str:pk>/', views.updateSquad, name="update-squad"),
    path('delete-squad/<str:pk>/', views.deleteSquad, name="delete-squad"),
    path('login/', views.loginController, name="login"),
    path('logout/', views.logoutController, name="logout"),
    path('register/', views.registerController, name="register"),
    path('delete-chat/<str:pk>/', views.deleteChat, name="delete-chat"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('update-profile/', views.updateProfile, name="update-profile"),
]
