from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('well/<int:pk>/', views.well_detail, name='well_detail'),
]
