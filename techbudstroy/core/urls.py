from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('objects/', views.object_list, name='object_list'),
    path('objects/<int:pk>/', views.object_detail, name='object_detail'),
    path('materials/', views.material_list, name='material_list'),
    path('employees/', views.employee_list, name='employee_list'),
    path('contracts/', views.contract_list, name='contract_list'),
]