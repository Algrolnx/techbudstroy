import os
import glob
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand
from decouple import config


def find_pg_dump():
    import shutil
    found = shutil.which('pg_dump')
    if found:
        return found

    pattern = r'C:\Program Files\PostgreSQL\*\bin\pg_dump.exe'
    matches = glob.glob(pattern)
    if matches:
        return matches[-1] 

    return None


class Command(BaseCommand):
    help = 'Робить резервну копію бази даних'

    def handle(self, *args, **kwargs):
        pg_dump = find_pg_dump()

        self.stdout.write(f'Використовується: {pg_dump}')

        db_name = config('DB_NAME')
        db_user = config('DB_USER')
        db_password = config('DB_PASSWORD')
        db_host = config('DB_HOST', default='localhost')
        db_port = config('DB_PORT', default='5432')

        backup_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..', '..', 'backups'
        )
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'backup_{db_name}_{timestamp}.sql'
        filepath = os.path.normpath(os.path.join(backup_dir, filename))

        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        command = [pg_dump, '-h', db_host, '-p', db_port,
                   '-U', db_user, '-F', 'p', '-f', filepath, db_name]

        self.stdout.write(f'Створення бекапу: {filename}...')
        result = subprocess.run(command, env=env, capture_output=True, text=True)

        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS(f'Бекап збережено: {filepath}'))
        else:
            self.stdout.write(self.style.ERROR(f'Помилка: {result.stderr}'))
