from django.urls import path
from . import views

urlpatterns = [
    path('', views.node, name='node'),
]
