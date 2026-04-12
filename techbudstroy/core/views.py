from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.http import HttpResponse
import csv
from .models import (
    ConstructionObject, Material,
    Employee, Contract, Payment, Brigade, MaterialUsage
)

@login_required
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

@login_required
@permission_required('core.view_constructionobject', raise_exception=True)
def object_list(request):
    objects = ConstructionObject.objects.select_related('client').all()
    return render(request, 'core/object_list.html', {'objects': objects})

@login_required
@permission_required('core.view_constructionobject', raise_exception=True)
def object_detail(request, pk):
    queryset = ConstructionObject.objects.prefetch_related(
        'constructionstage_set', 
        'materialusage_set__material',
        'contract_set'
    )
    obj = get_object_or_404(queryset, pk=pk)
    return render(request, 'core/object_detail.html', {'object': obj})

@login_required
@permission_required('core.view_material', raise_exception=True)
def material_list(request):
    materials = Material.objects.all()
    return render(request, 'core/material_list.html', {'materials': materials})

@login_required
@permission_required('core.view_employee', raise_exception=True)
def employee_list(request):
    brigade_id = request.GET.get('brigade')
    if brigade_id:
        employees = Employee.objects.select_related('brigade').filter(brigade_id=brigade_id)
        current_brigade = Brigade.objects.get(id=brigade_id)
    else:
        employees = Employee.objects.select_related('brigade').all()
        current_brigade = None
        
    brigades = Brigade.objects.all()
    
    context = {
        'employees': employees,
        'brigades': brigades,
        'current_brigade': current_brigade
    }
    return render(request, 'core/employee_list.html', context)

@login_required
@permission_required('core.view_contract', raise_exception=True)
def contract_list(request):
    contracts = Contract.objects.select_related('client', 'construction_object').all()
    return render(request, 'core/contract_list.html', {'contracts': contracts})

@login_required
@permission_required('core.view_materialusage', raise_exception=True)
def reports(request):
    material_report = (
        MaterialUsage.objects
        .values(name=F('material__name'), unit=F('material__unit'))
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:10]
    )
    salary_report = (
        Employee.objects
        .values(brigade_name=F('brigade__name'))
        .annotate(total_salary=Sum('salary'))
        .order_by('-total_salary')
    )
    
    return render(request, 'core/reports.html', {
        'material_report': material_report,
        'salary_report': salary_report,
    })

@login_required
@permission_required('core.view_materialusage', raise_exception=True)
def export_reports_excel(request):
    import openpyxl

    wb = openpyxl.Workbook()

    # Аркуш 1: Матеріали
    ws1 = wb.active
    ws1.title = 'Матеріали'
    ws1.append(['Матеріал', 'Одиниця', 'Кількість'])
    material_report = (
        MaterialUsage.objects
        .values(name=F('material__name'), unit=F('material__unit'))
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:10]
    )
    for row in material_report:
        ws1.append([row['name'], row['unit'], float(row['total_qty'])])

    # Аркуш 2: Зарплати по бригадах
    ws2 = wb.create_sheet('Зарплати по бригадах')
    ws2.append(['Бригада', 'Сума зарплат (грн)'])
    salary_report = (
        Employee.objects
        .values(brigade_name=F('brigade__name'))
        .annotate(total_salary=Sum('salary'))
        .order_by('-total_salary')
    )
    for row in salary_report:
        ws2.append([row['brigade_name'], float(row['total_salary'])])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="techbudstroy_reports.xlsx"'
    wb.save(response)
    return response