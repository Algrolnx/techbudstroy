from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from .models import (
    ConstructionObject, Material,
    Employee, Contract, Payment
)

def dashboard(request):
    total_objects = ConstructionObject.objects.count()
    active_contracts = Contract.objects.filter(status='Active').count()
    
    period = request.GET.get('period', 'month')
    
    if period == 'week':
        trunc_func = TruncWeek('payment_date')
        date_format = '%Y-%U' 
    elif period == 'day':
        trunc_func = TruncDay('payment_date')
        date_format = '%d %b'
    else: 
        trunc_func = TruncMonth('payment_date')
        date_format = '%b %Y' 

    payments = Payment.objects.annotate(period=trunc_func).values('period', 'payment_type').annotate(total=Sum('amount')).order_by('period')
    
    labels = []
    income_data = []
    expense_data = []
    
    data_map = {} 

    for p in payments:
        date_label = p['period'].strftime(date_format)
        if date_label not in data_map:
            data_map[date_label] = {'IN': 0, 'OUT': 0}
        
        if p['payment_type'] == 'IN':
            data_map[date_label]['IN'] += float(p['total'])
        else:
            data_map[date_label]['OUT'] += float(p['total'])

    for label, values in data_map.items():
        labels.append(label)
        income_data.append(values['IN'])
        expense_data.append(values['OUT'])

    latest_payments = Contract.objects.order_by('-id')[:5]

    context = {
        'total_objects': total_objects,
        'active_contracts': active_contracts,
        'chart_labels': labels,
        'income_data': income_data,
        'expense_data': expense_data,
        'latest_payments': latest_payments,
        'current_period': period
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
    
