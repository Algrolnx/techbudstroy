from django.contrib import admin
from .models import (
    Company, Brigade, Employee,
    Client, ConstructionObject, Contract,
    ConstructionStage, Material, MaterialUsage,
    Equipment, Payment, AuditLog
)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'edrpou', 'director')
    search_fields = ('name', 'edrpou')

@admin.register(Brigade)
class BrigadeAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'company')
    list_filter = ('company',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'salary', 'company', 'brigade')
    list_filter = ('company', 'brigade')
    search_fields = ('full_name', 'position')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax', 'address')

@admin.register(ConstructionObject)
class ConstructionObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'client', 'company')
    list_filter = ('client', 'company')
    search_fields = ('title', 'address')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'client', 'total_amount', 'status')
    list_filter = ('status',)

@admin.register(ConstructionStage)
class ConstructionStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress_percent', 'construction_object')
    list_filter = ('construction_object',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'price_per_unit', 'stock_quantity')
    search_fields = ('name',)

@admin.register(MaterialUsage)
class MaterialUsageAdmin(admin.ModelAdmin):
    list_display = ('material', 'construction_object', 'quantity', 'date_used')
    list_filter = ('construction_object', 'date_used')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'serial_number', 'company')
    list_filter = ('type', 'company')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'payment_type', 'amount', 'payment_date')
    list_filter = ('payment_type', 'payment_date')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'employee', 'table_name', 'timestamp')
    list_filter = ('action', 'table_name')
    readonly_fields = ('timestamp',)

