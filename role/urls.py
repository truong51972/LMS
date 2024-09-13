from django.urls import path
from . import views

app_name = 'role'
urlpatterns = [
    path('roles/', views.role_list, name='role_list'),
    
    path('roles/create/', views.role_add, name='role_add'),
    path('roles/edit/<int:pk>/', views.role_edit, name='role_edit'),
    path('roles/delete/<int:pk>/', views.role_delete, name='role_delete'),
]
