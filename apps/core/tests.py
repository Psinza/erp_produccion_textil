from django.test import TestCase, override_settings

from apps.core.models import Usuario


@override_settings(SECRET_KEY='test-only-secret-key-for-smoke-tests')
class ModuleSmokeTests(TestCase):
    MODULE_PATHS = (
        '/',
        '/rrhh/',
        '/contabilidad/',
        '/compras/',
        '/ventas/',
        '/produccion/',
        '/logistica/',
        '/transportes/',
        '/seguridad/',
        '/servicios-generales/',
        '/contrataciones-publicas/',
        '/planificacion-presupuesto/',
        '/tecnologia-informacion/',
        '/oac/',
        '/servicios-medicos/',
        '/auditoria-interna/',
        '/consultoria-juridica/',
        '/gerencia-calidad/',
    )

    @classmethod
    def setUpTestData(cls):
        cls.user = Usuario.objects.create_superuser(
            username='smoke-admin',
            email='smoke-admin@example.invalid',
            password='test-only-password-123',
            nombres='Smoke',
            apellidos='Admin',
        )

    def test_authenticated_user_can_open_module_entry_points(self):
        self.client.force_login(self.user)
        for path in self.MODULE_PATHS:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertIn(response.status_code, (200, 301, 302))
