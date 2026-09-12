from .access import allowed_modules, can_modify_module


def module_access(request):
    modules = allowed_modules(request.user)
    return {
        'allowed_modules': modules,
        'editable_modules': modules,
        'can_modify_module': can_modify_module,
    }
