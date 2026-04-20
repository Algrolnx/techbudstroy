import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    Company, Brigade, Employee, Client,
    ConstructionObject, Contract, ConstructionStage,
    Material, MaterialUsage, Equipment, Payment
)

class Command(BaseCommand):
    help = 'Наповнення БД тестовими вибірковими даними'

    def handle(self, *args, **kwargs):
        self.stdout.write('Видалення старих даних...')
        Payment.objects.all().delete()
        MaterialUsage.objects.all().delete()
        Equipment.objects.all().delete()
        Material.objects.all().delete()
        ConstructionStage.objects.all().delete()
        Contract.objects.all().delete()
        ConstructionObject.objects.all().delete()
        Client.objects.all().delete()
        Employee.objects.all().delete()
        Brigade.objects.all().delete()
        Company.objects.all().delete()

        self.stdout.write('Створення Компаній (30+)...')
        companies = []
        for i in range(1, 40):
            c = Company.objects.create(
                name=f"БудМоноліт {i}",
                edrpou=f"1000{i:04d}",
                address=f"м. Київ, вул. Будівельна, {i}",
                director=f"Іванов І.І.{i}"
            )
            companies.append(c)

        self.stdout.write('Створення Клієнтів (30+)...')
        clients = []
        for i in range(1, 40):
            c = Client.objects.create(
                name=f"Інвест-Груп {i}",
                tax=f"200000{i:04d}",
                address=f"м. Львів, вул. Франка, {i}"
            )
            clients.append(c)

        self.stdout.write('Створення Бригад (30+)...')
        brigades = []
        for i in range(1, 40):
            b = Brigade.objects.create(
                name=f"Бригада №{i}",
                specialization=random.choice(["Бетонні роботи", "Мурування", "Оздоблення", "Електрика", "Сантехніка"]),
                company=random.choice(companies)
            )
            brigades.append(b)

        self.stdout.write('Створення Працівників (150+)...')
        for i in range(1, 150):
            Employee.objects.create(
                full_name=f"Працівник {i}",
                position=random.choice(["Бригадир", "Бетоняр", "Муляр", "Маляр", "Різноробочий"]),
                salary=round(random.uniform(15000, 45000), 2),
                company=random.choice(companies),
                brigade=random.choice(brigades)
            )

        self.stdout.write("Створення Об'єктів будівництва (30+)...")
        objects = []
        for i in range(1, 40):
            obj = ConstructionObject.objects.create(
                title=f"ЖК Щасливий {i}",
                address=f"Київ, ділянка {i}",
                area=round(random.uniform(500, 10000), 2),
                client=random.choice(clients),
                company=random.choice(companies)
            )
            objects.append(obj)

        self.stdout.write("Створення Контрактів (30+)...")
        contracts = []
        for i in range(1, 40):
            contract = Contract.objects.create(
                contract_number=f"CNTR-{i}-2024",
                total_amount=round(random.uniform(1000000, 50000000), 2),
                status=random.choice(['Active', 'Completed', 'Paused']),
                client=random.choice(clients),
                construction_object=random.choice(objects)
            )
            contracts.append(contract)

        self.stdout.write("Створення Стадій будівництва (90+)...")
        for obj in objects:
            ConstructionStage.objects.create(name="Підготовка", progress_percent=100, construction_object=obj)
            ConstructionStage.objects.create(name="Фундамент", progress_percent=random.randint(0, 100), construction_object=obj)
            ConstructionStage.objects.create(name="Зведення стін", progress_percent=random.randint(0, 50), construction_object=obj)

        self.stdout.write("Створення Матеріалів (30+)...")
        materials = []
        for i in range(1, 40):
            m = Material.objects.create(
                name=f"Матеріал Будівельний {i}",
                unit=random.choice(['кг', 'т', 'шт', 'куб.м']),
                price_per_unit=round(random.uniform(10, 5000), 2),
                stock_quantity=round(random.uniform(100, 10000), 2)
            )
            materials.append(m)

        self.stdout.write("Створення Використання Матеріалів (100+)...")
        for i in range(1, 100):
            MaterialUsage.objects.create(
                construction_object=random.choice(objects),
                material=random.choice(materials),
                quantity=round(random.uniform(1, 100), 2)
            )

        self.stdout.write("Створення Обладнання (30+)...")
        for i in range(1, 40):
            Equipment.objects.create(
                name=f"Екскаватор {i}",
                type=random.choice(['Вантажівка', 'Екскаватор', 'Кран', 'Бетономішалка']),
                serial_number=f"SN-{i}-{random.randint(1000,9999)}",
                company=random.choice(companies)
            )

        self.stdout.write("Створення Оплат (60+)...")
        for i in range(1, 60):
            Payment.objects.create(
                payment_type=random.choice(['IN', 'OUT']),
                amount=round(random.uniform(10000, 500000), 2),
                payment_date=timezone.now().date() - timezone.timedelta(days=random.randint(1, 365)),
                contract=random.choice(contracts)
            )

        self.stdout.write(self.style.SUCCESS('База даних успішно наповнена випадковими даними (мінімум 30 записів на таблицю)!'))
