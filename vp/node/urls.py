from django.urls import path
from . import views

urlpatterns = [
    path('', views.node, name='node'),
    path('<str:node_id>', views.handle_node, name='handle node'),
    path('edge/<str:node_from_id>/<str:node_to_id>', views.edge, name='add edge')
]
