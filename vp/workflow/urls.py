from django.urls import path
from . import views

urlpatterns = [
    path('open', views.open_workflow, name='open workflow'),
    path('save', views.save_workflow, name='save'),
]
