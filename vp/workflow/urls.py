from django.urls import path
from . import views

urlpatterns = [
    path('open', views.open, name='open'),
    path('save', views.save, name='save'),
]
