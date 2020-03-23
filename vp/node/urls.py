from django.urls import path
from . import views

urlpatterns = [
    path('', views.node, name='node'),
    path('<int:node_id>', views.handle_node, name='handle node')
]
