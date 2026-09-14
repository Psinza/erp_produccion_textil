# Despliegue en Ubuntu 24.04 con PostgreSQL

## 1. Preparar PostgreSQL

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres createuser --createdb erp_user
sudo -u postgres createdb --owner=erp_user erp_produccion_textil
```

Asigne una contraseña al usuario de PostgreSQL con `sudo -u postgres psql` y no la
publique en Git.

## 2. Descargar y configurar

```bash
git clone https://github.com/Psinza/erp_produccion_textil.git /opt/erp_produccion_textil
cd /opt/erp_produccion_textil
export DATABASE_URL='postgresql://erp_user:CAMBIE_ESTA_CLAVE@127.0.0.1:5432/erp_produccion_textil'
export DJANGO_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DJANGO_ALLOWED_HOSTS='erp.midominio.local,127.0.0.1'
sudo -E bash deploy/ubuntu24_postgres.sh
```

El script instala dependencias, crea el entorno virtual, aplica migraciones,
genera estáticos, ejecuta `check --deploy` y crea los usuarios de módulos.

## 3. Usuarios y permisos

El comando idempotente es:

```bash
.venv/bin/python manage.py provision_access --password-mode username
```

Cada usuario recibe únicamente los permisos `view`, `add`, `change` y `delete`
de su aplicación. Las cuentas de Producción tienen además alcances aislados:

`corte`, `udp`, `pci`, `bordados`, `producciontextil`, `mecanica`, `despacho`
y `pool`.

Las contraseñas iniciales son iguales al nombre de usuario porque así fue
solicitado. Deben cambiarse inmediatamente:

```bash
.venv/bin/python manage.py changepassword comercializacion
```

El comando no crea usuarios como superusuarios ni como miembros de `is_staff`.
El middleware bloquea namespaces y rutas de submódulos no autorizados.

## 4. Servicio systemd

```bash
sudo useradd --system --home /opt/erp_produccion_textil --shell /usr/sbin/nologin erp
sudo chown -R erp:erp /opt/erp_produccion_textil
sudo cp deploy/erp-production.service.example /etc/systemd/system/erp-production.service
sudo systemctl daemon-reload
sudo systemctl enable --now erp-production
sudo systemctl status erp-production
```

Configure HTTPS y proxy inverso antes de exponer el servicio a Internet.
Cuando HTTPS esté activo, añada al `.env`:

```dotenv
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```
