SENSITIVE_NAMESPACES = {
    'rrhh',
    'servicios_medicos',
    'consultoria_juridica',
    'auditoria_interna',
}


class SensitiveDataHeadersMiddleware:
    """Prevents browser and search-engine caching of confidential module pages."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        namespace = getattr(request.resolver_match, 'namespace', None)
        if namespace in SENSITIVE_NAMESPACES:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        return response
