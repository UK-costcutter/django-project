# system_monitor/monitor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('metrics/', views.get_system_metrics, name='get_metrics'),
    path('toggle/', views.toggle_monitoring, name='toggle_monitoring'),
]