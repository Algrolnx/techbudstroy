from django.shortcuts import render, get_object_or_404
from .models import (
    ConstructionObject, Material,
    Employee, Contract
)

def dashboard(request):
    total_objects = ConstructionObject.objects.count()
    active_contracts = Contract.objects.filter(status='Active').count()

    context = {
        'total_objects': total_objects,
        'active_contracts': active_contracts,
    }
    return render(request, 'core/dashboard.html', context)

def object_list(request):
    objects = ConstructionObject.objects.all()
    return render(request, 'core/object_list.html', {'objects': objects})

def object_detail(request, pk):
    obj = get_object_or_404(ConstructionObject, pk=pk)
    return render(request, 'core/object_detail.html', {'object': obj})

def material_list(request):
    materials = Material.objects.all()
    return render(request, 'core/material_list.html', {'materials': materials})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'core/employee_list.html', {'employees': employees})

def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, 'core/contract_list.html', {'contracts': contracts})
    
