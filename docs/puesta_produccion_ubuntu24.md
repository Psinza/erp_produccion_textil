# Puesta en producción en Ubuntu 24.04

Este procedimiento instala PostgreSQL local, Gunicorn, Nginx y respaldos diarios.
Debe ejecutarse en el servidor Ubuntu, no desde el navegador ni con `runserver`.

## 1. Preparar el servidor

Actualice Ubuntu y cree un usuario con `sudo`. El servidor debe tener una IP fija
en la red y un nombre DNS interno o dominio público.

```bash
sudo apt update
sudo apt install -y git ca-certificates curl
```

## 2. Ejecutar el instalador

No coloque estas variables en Git ni en un archivo compartido:

```bash
export ERP_DB_PASSWORD='una-clave-larga-y-aleatoria'
export DJANGO_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(64))')"
export DJANGO_ALLOWED_HOSTS='erp.example.ve,192.168.1.20'
export CSRF_TRUSTED_ORIGINS='https://erp.example.ve'
export DEPLOY_USER="$USER"
```

Luego:

```bash
git clone https://github.com/Psinza/erp_produccion_textil.git
cd erp_produccion_textil
sudo -E bash deploy/ubuntu24_postgres.sh
```

El instalador crea la base `erp_produccion_textil`, el usuario PostgreSQL `erp`,
aplica migraciones, ejecuta las pruebas, instala Gunicorn y activa el respaldo
diario a las 02:30 con una variación de hasta 15 minutos.

## 3. Configurar Nginx y HTTPS

Para una red interna sin dominio público se puede usar un certificado emitido
por la autoridad certificadora interna. Un certificado autofirmado funciona
para cifrar, pero los navegadores mostrarán una advertencia hasta confiar en
la autoridad.

Con un dominio público resoluble:

```bash
sudo cp deploy/nginx/erp.conf.example /etc/nginx/sites-available/erp
sudo sed -i 's/erp.example.local/erp.example.ve/' /etc/nginx/sites-available/erp
sudo ln -s /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/erp
sudo nginx -t
sudo systemctl reload nginx
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d erp.example.ve
```

Después de emitir el certificado, configure en `.env`:

```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://erp.example.ve
```

```bash
sudo systemctl restart erp-production
```

No exponga el puerto 8000; Gunicorn escucha únicamente en `127.0.0.1`.

## 4. Comprobar PostgreSQL y respaldos

```bash
sudo systemctl status postgresql erp-production nginx
sudo -u postgres psql -d erp_produccion_textil -c '\dt'
sudo systemctl list-timers erp-backup.timer
sudo systemctl start erp-backup.service
ls -lh /var/backups/erp
```

Un respaldo no se considera válido hasta probar su restauración en una base
separada. Para PostgreSQL:

```bash
createdb -h 127.0.0.1 -U erp erp_restore_test
pg_restore -h 127.0.0.1 -U erp -d erp_restore_test /var/backups/erp/erp_postgresql_FECHA.dump
```

Copie además los respaldos a otro almacenamiento con acceso restringido y
defina retención, cifrado y responsable de restauración.

## 5. Pruebas por módulo

La suite actual ejecuta seis pruebas, incluyendo puntos de entrada de los
módulos principales:

```bash
.venv/bin/python manage.py test --noinput -v 1
```

Antes de la aceptación formal se debe ampliar cada smoke test con creación,
consulta, modificación, eliminación, permisos y validaciones de negocio del
módulo. Los módulos médicos, jurídicos, RRHH y auditoría requieren además una
revisión de autorización con usuarios que no sean superusuarios.
