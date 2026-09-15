import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = 'Crea un respaldo de la base de datos SQLite o PostgreSQL.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            default=str(settings.BASE_DIR / 'backups'),
            help='Directorio de destino del respaldo.',
        )

    def handle(self, *args, **options):
        connection = connections['default']
        output_dir = Path(options['output_dir']).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        vendor = connection.vendor

        if vendor == 'sqlite':
            source = Path(connection.settings_dict['NAME'])
            if not source.exists():
                raise CommandError(f'No existe la base SQLite: {source}')
            target = output_dir / f'erp_sqlite_{stamp}.sqlite3'
            shutil.copy2(source, target)
        elif vendor == 'postgresql':
            target = output_dir / f'erp_postgresql_{stamp}.dump'
            config = connection.settings_dict
            env = os.environ.copy()
            if config.get('PASSWORD'):
                env['PGPASSWORD'] = config['PASSWORD']
            command = [
                'pg_dump',
                '--format=custom',
                '--file', str(target),
                '--host', config.get('HOST') or 'localhost',
                '--port', str(config.get('PORT') or 5432),
                '--username', config.get('USER') or '',
                config.get('NAME') or '',
            ]
            try:
                subprocess.run(command, check=True, env=env)
            except FileNotFoundError as exc:
                raise CommandError('pg_dump no está instalado en el servidor.') from exc
            except subprocess.CalledProcessError as exc:
                raise CommandError(f'pg_dump terminó con código {exc.returncode}.') from exc
        else:
            raise CommandError(f'Base de datos no soportada: {vendor}')

        self.stdout.write(self.style.SUCCESS(f'Respaldo creado: {target}'))
