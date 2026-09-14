#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="${PROJECT_DIR:-/opt/erp_produccion_textil}"
REPOSITORY_URL="${REPOSITORY_URL:-https://github.com/Psinza/erp_produccion_textil.git}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
OWNER="${DEPLOY_USER:-${SUDO_USER:-${USER}}}"

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "Defina DATABASE_URL antes de ejecutar este script." >&2
  echo "Ejemplo: postgresql://erp_user:password@127.0.0.1:5432/erp_produccion_textil" >&2
  exit 1
fi

if [[ -z "${DJANGO_SECRET_KEY:-}" ]]; then
  echo "Defina DJANGO_SECRET_KEY antes de ejecutar este script." >&2
  exit 1
fi

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-dev build-essential \
  libpq-dev postgresql-client git

if [[ ! -d "${PROJECT_DIR}/.git" ]]; then
  sudo mkdir -p "$(dirname "${PROJECT_DIR}")"
  sudo git clone "${REPOSITORY_URL}" "${PROJECT_DIR}"
else
  sudo git -C "${PROJECT_DIR}" pull --ff-only origin main
fi

sudo chown -R "${OWNER}:${OWNER}" "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

"${PYTHON_BIN}" -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

umask 077
cat > .env <<EOF
SECRET_KEY=${DJANGO_SECRET_KEY}
DJANGO_DEBUG=False
ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS:-localhost,127.0.0.1}
CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS:-}
DATABASE_URL=${DATABASE_URL}
DATABASE_SSL_REQUIRE=${DATABASE_SSL_REQUIRE:-False}
EMPRESA_NOMBRE=${EMPRESA_NOMBRE:-Complejo Industrial Tiuna I}
EOF

.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput
.venv/bin/python manage.py check --deploy
.venv/bin/python manage.py provision_access --password-mode username

echo "Instalación terminada en ${PROJECT_DIR}."
echo "Las cuentas iniciales tienen como clave su mismo nombre: cambie esas claves inmediatamente."
echo "Para producción, configure Gunicorn/systemd usando deploy/erp-production.service.example."
