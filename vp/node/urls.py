from django.urls import path
from . import views

urlpatterns = [
    path('', views.node, name='node'),
    path('<str:node_id>', views.handle_node, name='handle node'),
    path('global/<str:node_id>', views.handle_node, name='handle node'),
    path('<str:node_id>/execute', views.execute_node, name='execute node'),
    path('<str:node_id>/retrieve_data', views.retrieve_data, name='retrieve data'),
    path('edge/<str:node_from_id>/<str:node_to_id>', views.handle_edge, name='handle edge')
]
