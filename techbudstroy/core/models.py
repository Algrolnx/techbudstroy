from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):
    name = models.CharField(max_length=150)
    edrpou = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=225, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Brigade(models.Model):
    name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    brigade = models.ForeignKey(Brigade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name

class Client(models.Model):
    name = models.CharField(max_length=150)
    tax = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=225)

    def __str__(self):
        return self.name

class ConstructionObject(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=225)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class Contract(models.Model):
    contract_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, default='Active')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    construction_object = models.ForeignKey(ConstructionObject, on_delete=models.CASCADE)

    def __str__(self):
        return self.contract_number

class ConstructionStage(models.Model):
    name = models.CharField(max_length=100)
    progress_percent = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    construction_object = models.ForeignKey(ConstructionObject, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} ({self.progress_percent}%)'

class Material(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class MaterialUsage(models.Model):
    construction_object = models.ForeignKey(ConstructionObject, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_used = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.material.name} - {self.construction_object.title}'

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_TYPES = [('IN', 'Надходження'), ('OUT', 'Видаток')]
    payment_type = models.CharField(max_length=3, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE )

    def __str__(self):
        return f'{self.get_payment_type_display()} - {self.amount}'

class AuditLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    table_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.action} @ {self.timestamp}'


    


