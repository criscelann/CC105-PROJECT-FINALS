from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_view, name='prediction_form'),  # Main form page
    path('result/', views.prediction_result_view, name='prediction_result'),  # Result page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page
]
