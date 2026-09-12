from django.http import HttpResponseForbidden


MODULE_AREA_CODES = {
    'produccion': {'PRODUCCION'},
    'logistica': {'LOGISTICA'},
    'compras': {'COMPRAS'},
    'ventas': {'VENTAS'},
    'comercializacion': {'COMERCIALIZACION'},
    'vendedores': {'VENTAS'},
    'transportes': {'TRANSPORTE'},
    'tesoreria': {'FINANZAS'},
    'contabilidad': {'FINANZAS'},
    'facturacion': {'FINANZAS'},
    'ordenacion_pagos': {'FINANZAS'},
    'rrhh': {'TALENTO_HUMANO'},
    'viaticos': {'TALENTO_HUMANO'},
    'activos_fijos': {'ACTIVOS'},
    'gerencia': {'GERENCIA'},
    'inventarios': {'LOGISTICA'},
}


def _normalizar(valor):
    return ''.join(
        caracter for caracter in (valor or '').upper()
        if caracter.isalnum() or caracter == '_'
    ).replace('Í', 'I').replace('Ó', 'O').replace('Á', 'A').replace('É', 'E').replace('Ú', 'U').replace('Ñ', 'N')


def user_area_codes(user):
    if not user.is_authenticated:
        return set()
    codes = set()
    if user.area:
        codes.update({_normalizar(user.area.codigo), _normalizar(user.area.nombre)})
    if user.rol:
        codes.update(
            value
            for area in user.rol.areas.all()
            for value in (_normalizar(area.codigo), _normalizar(area.nombre))
        )
        codes.add(_normalizar(user.rol.nombre))
    return codes


def allowed_modules(user):
    if not user.is_authenticated:
        return set()
    if user.is_superuser:
        return set(MODULE_AREA_CODES)
    codes = user_area_codes(user)
    return {
        module for module, area_codes in MODULE_AREA_CODES.items()
        if codes.intersection(area_codes)
    }


def can_access_module(user, namespace):
    return user.is_authenticated and (
        user.is_superuser
        
        or namespace not in MODULE_AREA_CODES
        or namespace in allowed_modules(user)
    )


def can_modify_module(user, namespace):
    """Users with an assigned module may use all operations in that module."""
    return can_access_module(user, namespace)


class GerenciaAccessMiddleware:
    """Restricts each user to the modules granted by their assigned role."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        namespace = getattr(request.resolver_match, 'namespace', None)
        if (
            request.user.is_authenticated
            and namespace
            and not can_access_module(request.user, namespace)
        ):
            return HttpResponseForbidden(
                'No tiene permisos para acceder a este módulo. Solicite autorización al administrador.'
            )
        return None
