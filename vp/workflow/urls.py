from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_workflow, name='new workflow'),
    path('open', views.open_workflow, name='open workflow'),
    path('save', views.save_workflow, name='save'),
]
