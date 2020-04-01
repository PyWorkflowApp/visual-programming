from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_workflow, name='new workflow'),
    path('open', views.open_workflow, name='open workflow'),
    path('save', views.save_workflow, name='save'),
    path('execute', views.execute_workflow, name='execute workflow'),
    path('execute/<str:node_id>/successors', views.get_successors, name='get node successors'),
    path('retrieve_csv/<str:node_id>', views.retrieve_csv, name='retrieve csv')
]
