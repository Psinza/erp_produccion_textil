from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string

from apps.core.models import Area, Usuario


MODULES = {
    'comercializacion': ('COMERCIAL', 'Comercialización'),
    'logistica': ('LOGISTICA', 'Logística'),
    'produccion': ('PRODUCCION', 'Producción'),
    'transportes': ('TRANSPORTE', 'Transportes'),
    'compras': ('COMPRAS', 'Compras'),
    'ventas': ('VENTAS', 'Ventas'),
    'tesoreria': ('TESORERIA', 'Tesorería'),
    'contabilidad': ('CONTAB', 'Contabilidad'),
    'facturacion': ('FACTURACION', 'Facturación'),
    'rrhh': ('RRHH', 'Recursos Humanos'),
    'activos_fijos': ('ACTIVOS', 'Activos Fijos'),
    'calidad': ('CALIDAD', 'Calidad'),
    'pcpi': ('PCPI', 'PCPI'),
    'seguridad': ('SEGURIDAD', 'Seguridad Integral e Industrial'),
    'servicios_generales': ('SERVICIOS_GENERALES', 'Servicios Generales'),
    'contrataciones_publicas': ('CONTRATACIONES_PUBLICAS', 'Contrataciones Públicas'),
    'planificacion_presupuesto': ('PLANIFICACION', 'Planificación y Presupuesto'),
    'tecnologia_informacion': ('TECNOLOGIA', 'Tecnología de la Información'),
    'oac': ('OAC', 'Oficina de Atención a la Ciudadanía'),
    'servicios_medicos': ('SERVICIOS_MEDICOS', 'Servicios Médicos'),
    'auditoria_interna': ('AUDITORIA_INTERNA', 'Auditoría Interna'),
    'consultoria_juridica': ('CONSULTORIA_JURIDICA', 'Consultoría Jurídica'),
    'gerencia_calidad': ('CALIDAD', 'Gerencia de Calidad'),
    'gerencia': ('GERENCIA', 'Gerencia'),
}

PRODUCTION_SCOPES = {
    'corte': 'Corte',
    'udp': 'UDP',
    'pci': 'PCPI',
    'bordados': 'Bordados',
    'producciontextil': 'Producción Textil',
    'mecanica': 'Mecánica Industrial',
    'despacho': 'Despacho',
    'pool': 'Pool / Calidad',
}

USERS = {
    'comercializacion': ('comercializacion', 'comercializacion'),
    'logistica': ('logistica', 'logistica'),
    'produccion': ('produccion', 'produccion'),
    **{
        name: (name, 'pcpi' if name == 'pci' else 'produccion')
        for name in PRODUCTION_SCOPES
    },
    'transporte': ('transporte', 'transportes'),
    'compras': ('compras', 'compras'),
    'ventas': ('ventas', 'ventas'),
    'tesoreria': ('tesoreria', 'tesoreria'),
    'contabilidad': ('contabilidad', 'contabilidad'),
    'facturacion': ('facturacion', 'facturacion'),
    'rrhh': ('rrhh', 'rrhh'),
    'activos_fijos': ('activos_fijos', 'activos_fijos'),
    'calidad': ('calidad', 'calidad'),
    'seguridad': ('seguridad', 'seguridad'),
    'servicios_generales': ('servicios_generales', 'servicios_generales'),
    'contrataciones_publicas': ('contrataciones_publicas', 'contrataciones_publicas'),
    'planificacion_presupuesto': ('planificacion_presupuesto', 'planificacion_presupuesto'),
    'tecnologia_informacion': ('tecnologia_informacion', 'tecnologia_informacion'),
    'oac': ('oac', 'oac'),
    'servicios_medicos': ('servicios_medicos', 'servicios_medicos'),
    'auditoria_interna': ('auditoria_interna', 'auditoria_interna'),
    'consultoria_juridica': ('consultoria_juridica', 'consultoria_juridica'),
    'gerencia_calidad': ('gerencia_calidad', 'gerencia_calidad'),
    'gerencia': ('gerencia_produccion', 'gerencia'),
}


def permissions_for_app(app_label):
    content_types = ContentType.objects.filter(app_label=app_label)
    return Permission.objects.filter(
        content_type__in=content_types,
        codename__regex=r'^(add|change|delete|view)_',
    )


class Command(BaseCommand):
    help = 'Crea usuarios y grupos CRUD aislados por módulo y submódulo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password-mode',
            choices=('username', 'random'),
            default='username',
            help='Contraseña inicial igual al usuario o aleatoria. Por defecto: username.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password_mode = options['password_mode']
        area_map = {}
        for code, name in MODULES.values():
            area_map[code] = Area.objects.get_or_create(
                codigo=code, defaults={'nombre': name}
            )[0]

        module_groups = {}
        for module, (area_code, area_name) in MODULES.items():
            group, _ = Group.objects.get_or_create(name=f'erp:module:{module}')
            group.permissions.set(permissions_for_app(module))
            module_groups[module] = group
            self.stdout.write(f'Grupo CRUD: {group.name} ({area_name})')

        for scope, label in PRODUCTION_SCOPES.items():
            group, _ = Group.objects.get_or_create(
                name=f'erp:scope:produccion:{scope}'
            )
            group.permissions.set(permissions_for_app('produccion' if scope != 'pci' else 'pcpi'))
            self.stdout.write(f'Grupo submódulo: {group.name} ({label})')

        for key, (username, module) in USERS.items():
            email = f'{username}@erp.local'
            user, created = Usuario.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'nombres': username.replace('_', ' ').title(),
                    'apellidos': 'ERP',
                    'cargo': f'Usuario de {module}',
                    'area': area_map[MODULES[module][0]],
                    'is_staff': False,
                    'is_superuser': False,
                },
            )
            user.email = email
            user.area = area_map[MODULES[module][0]]
            user.is_staff = False
            user.is_superuser = False
            initial_password = None
            if password_mode == 'username' or created:
                initial_password = (
                    username
                    if password_mode == 'username'
                    else get_random_string(16)
                )
                user.set_password(initial_password)
            user.groups.set([module_groups[module]])
            if key in PRODUCTION_SCOPES:
                scope_group = Group.objects.get(
                    name=f'erp:scope:produccion:{key}'
                )
                user.groups.add(scope_group)
            if key == 'pool':
                user.groups.add(module_groups['calidad'])
            user.save()
            status = 'creado' if created else 'actualizado'
            password_note = (
                f' / clave temporal: {initial_password}'
                if initial_password
                else ' / clave conservada'
            )
            self.stdout.write(self.style.SUCCESS(
                f'Usuario {status}: {username}{password_note}'
            ))

        if password_mode == 'username':
            self.stdout.write(self.style.WARNING(
                'Cambie las claves iniciales iguales al usuario antes de operar en producción.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'Guarde las claves temporales mostradas y cámbielas después del primer acceso.'
            ))
