# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('node/<str:node_id>', views.get_node, name='get_node'),
    path('node', views.add_node, name='add_node'),
    path('nodes', views.get_all_nodes, name='get_all_nodes'),
    
    path('node/<str:node_id>/update', views.update_node, name='update_node'),
    path('node/<str:node_id>/delete', views.delete_node, name='delete_node'),
    
    path('edge', views.add_edge, name='add_edge'),
    path('edge/delete', views.delete_edge, name='delete_edge'),
    
    path('init-mock/', views.init_mock_data, name='init_mock'),
]