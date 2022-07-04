from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('squads/', views.getSquads),
    path('squad/<str:pk>/', views.getSquad),
]
