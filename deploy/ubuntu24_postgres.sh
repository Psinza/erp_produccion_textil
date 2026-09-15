#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="${PROJECT_DIR:-/opt/erp_produccion_textil}"
REPOSITORY_URL="${REPOSITORY_URL:-https://github.com/Psinza/erp_produccion_textil.git}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
OWNER="${DEPLOY_USER:-${SUDO_USER:-${USER}}}"
ERP_DB_NAME="${ERP_DB_NAME:-erp_produccion_textil}"
ERP_DB_USER="${ERP_DB_USER:-erp}"

if [[ -z "${ERP_DB_PASSWORD:-}" || -z "${DJANGO_SECRET_KEY:-}" ]]; then
  echo "Defina ERP_DB_PASSWORD y DJANGO_SECRET_KEY antes de ejecutar este script." >&2
  exit 1
fi

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-dev build-essential \
  libpq-dev postgresql postgresql-contrib postgresql-client nginx git

sudo systemctl enable --now postgresql
if ! id -u erp >/dev/null 2>&1; then
  sudo useradd --system --home-dir "${PROJECT_DIR}" --shell /usr/sbin/nologin erp
fi
sudo -u postgres psql \
  -v db_name="$ERP_DB_NAME" \
  -v db_user="$ERP_DB_USER" \
  -v db_password="$ERP_DB_PASSWORD" <<'SQL'
SELECT format('CREATE USER %I WITH PASSWORD %L', :'db_user', :'db_password')
WHERE NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = :'db_user')\gexec
SELECT format('ALTER USER %I WITH PASSWORD %L', :'db_user', :'db_password')\gexec
SELECT format('CREATE DATABASE %I OWNER %I', :'db_name', :'db_user')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'db_name')\gexec
SQL

DATABASE_URL="${DATABASE_URL:-postgresql://${ERP_DB_USER}:${ERP_DB_PASSWORD}@127.0.0.1:5432/${ERP_DB_NAME}}"

if [[ ! -d "${PROJECT_DIR}/.git" ]]; then
  sudo mkdir -p "$(dirname "${PROJECT_DIR}")"
  sudo git clone "${REPOSITORY_URL}" "${PROJECT_DIR}"
else
  sudo git -C "${PROJECT_DIR}" pull --ff-only origin main
fi

sudo chown -R erp:erp "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

"${PYTHON_BIN}" -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

umask 077
cat > .env <<EOF
DEPLOYMENT_ENV=production
SECRET_KEY=${DJANGO_SECRET_KEY}
DJANGO_DEBUG=False
ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS:-localhost,127.0.0.1}
CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS:-}
SECURE_SSL_REDIRECT=${SECURE_SSL_REDIRECT:-False}
SESSION_COOKIE_SECURE=${SESSION_COOKIE_SECURE:-False}
CSRF_COOKIE_SECURE=${CSRF_COOKIE_SECURE:-False}
DATABASE_URL=${DATABASE_URL}
DATABASE_SSL_REQUIRE=${DATABASE_SSL_REQUIRE:-False}
EMPRESA_NOMBRE=${EMPRESA_NOMBRE:-Complejo Industrial Tiuna I}
EOF

.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput
.venv/bin/python manage.py test --noinput
.venv/bin/python manage.py check --deploy

sudo install -d -o erp -g erp -m 0750 /var/backups/erp
sudo install -m 0644 deploy/erp-production.service.example /etc/systemd/system/erp-production.service
sudo install -m 0644 deploy/erp-backup.service /etc/systemd/system/erp-backup.service
sudo install -m 0644 deploy/erp-backup.timer /etc/systemd/system/erp-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable --now erp-production erp-backup.timer

echo "Instalación terminada en ${PROJECT_DIR}."
echo "Configure Nginx usando deploy/nginx/erp.conf.example y HTTPS antes de abrir el servicio."
