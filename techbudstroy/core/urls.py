from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('objects/', views.object_list, name='objects_list'),
    path('objects/<int:pk>/', views_objects_detail, name='objects_detail')
    path('materials/', views.material_list, name='material_list')
    path('employees/', views.employee_list, name='employee_list')
    path('contracts/', views.contract_list, name='contract_list')
]