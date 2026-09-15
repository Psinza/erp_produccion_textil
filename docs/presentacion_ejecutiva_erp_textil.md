# Presentación ejecutiva
## ERP Textil Venezuela

**Documento base para directiva, aliados y redes sociales**  
**Fecha de evaluación:** 15 de septiembre de 2026  
**Estado evaluado:** prototipo funcional avanzado / piloto controlado

> Este documento describe las capacidades observadas en el repositorio y distingue
> entre funcionalidades implementadas, validaciones técnicas y aspectos que todavía
> requieren preparación antes de una publicación comercial o exposición a Internet.

---

## Diapositiva 1 — Portada

### ERP Textil Venezuela

**Una plataforma integrada para coordinar producción, administración, finanzas,
servicios y control gerencial en una organización textil e industrial.**

**Mensaje clave:** pasar de procesos aislados a una visión institucional trazable,
medible y escalable.

---

## Diapositiva 2 — ¿Qué problema resuelve?

- Información dispersa entre hojas de cálculo, correos y registros manuales.
- Dificultad para conocer el estado real de las operaciones.
- Retrasos en solicitudes, aprobaciones, mantenimientos y seguimiento.
- Poca trazabilidad de responsables, fechas, evidencias y estados.
- Indicadores gerenciales construidos manualmente.
- Necesidad de separar el acceso según área, rol y responsabilidad.

---

## Diapositiva 3 — Propuesta de valor

- **Centralización:** un solo portal para las áreas operativas y administrativas.
- **Trazabilidad:** cada registro conserva responsable, estado y fecha.
- **Control:** permisos por usuario, área, rol y módulo.
- **Gestión por indicadores:** tableros para operación y gerencia.
- **Escalabilidad:** arquitectura modular Django para crecer por fases.
- **Movilidad:** interfaz adaptada a computadora, tableta y teléfono.
- **Contexto venezolano:** módulos para contrataciones públicas, presupuesto,
  seguridad industrial, atención ciudadana y control normativo.

---

## Diapositiva 4 — Mapa de módulos activos

### Operaciones

- Producción y confección.
- Logística e inventarios.
- Compras.
- Ventas.
- Comercialización.
- Transportes y despachos.
- Seguridad integral e industrial.
- Servicios generales.
- Contrataciones públicas.
- Planificación y presupuesto.
- Tecnología de la información.

### Finanzas y administración

- Contabilidad.
- Facturación.
- Tesorería.
- Ordenación de pagos.
- Recursos Humanos.
- Viáticos.
- Activos fijos.

### Atención, control y dirección

- Oficina de Atención a la Ciudadanía.
- Servicios médicos.
- Auditoría interna.
- Consultoría jurídica.
- Gerencia de calidad.
- Gerencia e indicadores integrales.
- Administración del sistema.

---

## Diapositiva 5 — Funcionalidades principales

### Producción y operaciones

- Órdenes y registros de producción.
- Seguimiento de procesos textiles.
- Corte, bordado, mecánica, despacho y áreas especializadas.
- Inventario, almacenes y movimientos.
- Compras, proveedores y solicitudes.
- Ventas, clientes, pedidos y facturación.
- Transportes, flota y despachos.

### Administración y dirección

- Personal, cargos y relación con áreas.
- Presupuesto, partidas, modificaciones y ejecución.
- Contrataciones, ofertas, evaluaciones y contratos.
- Auditorías, hallazgos y acciones correctivas.
- Calidad, procesos, riesgos, indicadores y no conformidades.
- Tableros gerenciales con indicadores de distintas gerencias.

---

## Diapositiva 6 — Módulos institucionales diferenciadores

### Seguridad integral e industrial

- Personal de seguridad y puestos.
- Turnos 24x72.
- Dotación de equipos.
- Pases de ingreso y registros de acceso.
- Control de salida de materiales.
- Rondas, inspecciones SST e incidentes.
- Catálogo de normas aplicables.

### Tecnología de la información

- Tickets y prioridades.
- Monitoreo de red.
- Asignaciones diarias.
- Inventario y mantenimiento de equipos.
- Solicitudes y recepción de equipos.
- Servicios tecnológicos activos o apagados.
- Planes de trabajo, modernización e indicadores.

### OAC y Servicios Médicos

- Donaciones, citas, medicamentos y jornadas médicas.
- Chequeo de nuevos ingresos, reposos y afectaciones.
- Dotación de equipos médicos.
- Presupuesto de atención y salud ocupacional.

---

## Diapositiva 7 — Control y seguridad de acceso

- Usuario personalizado basado en Django.
- Usuarios activos/inactivos y estados operativos.
- Áreas y roles institucionales.
- Grupos de módulo con permisos `view`, `add`, `change` y `delete`.
- Superusuario institucional para administración global.
- Middleware de control de acceso por módulo y submódulo.
- Separación de áreas como Tecnología, Finanzas, RRHH, Producción y Gerencia.
- Menú lateral condicionado por los módulos autorizados.

**Resultado observado:** se validaron usuarios de módulos nuevos con acceso CRUD
aislado y el superusuario `psinza` con control global.

---

## Diapositiva 8 — Indicadores gerenciales

El dashboard de Gerencia integra métricas de:

- Producción y operaciones.
- Atención a la ciudadanía.
- Servicios médicos.
- Auditoría interna.
- Consultoría jurídica.
- Gerencia de calidad.
- Tecnología de la información.

### Ejemplos de indicadores TI

- Personal TI activo.
- Tickets abiertos y críticos.
- Alertas de red.
- Equipos en mantenimiento.
- Servicios activos y apagados.
- Asignaciones pendientes.
- Modernizaciones activas.

**Beneficio directivo:** priorizar decisiones con datos operativos actuales y no
solo con reportes manuales.

---

## Diapositiva 9 — Experiencia de uso

- Dashboard principal para acceder a los módulos autorizados.
- Menú lateral organizado por áreas.
- Barra lateral con desplazamiento independiente.
- Navegación móvil mediante botón de menú.
- Adaptación para teléfonos, tabletas y computadoras.
- Tablas con desplazamiento horizontal en pantallas pequeñas.
- Formularios y tarjetas con diseño responsive.
- Interfaz con Bootstrap, iconos y estilos institucionales.

---

## Diapositiva 10 — Ejecución del sistema

### Entorno de demostración local

```bash
cd erp_produccion_textil-main
source venv/bin/activate
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Acceso local:

```text
http://127.0.0.1:8000/
```

Acceso desde otro equipo de la red:

```text
http://IP_DEL_SERVIDOR:8000/
```

### Ejecución recomendada para una demostración

1. Iniciar sesión con un usuario autorizado.
2. Mostrar el dashboard principal.
3. Abrir Producción, Tecnología y Gerencia.
4. Registrar un caso controlado.
5. Mostrar el cambio de estado y el indicador.
6. Mostrar cómo otro usuario solo ve su módulo.
7. Repetir la navegación desde un teléfono o tableta.

> `runserver` es apropiado para demostración local. Para producción se requiere
> un servidor WSGI/ASGI, HTTPS, dominio, base de datos administrada y políticas
> de respaldo.

---

## Diapositiva 11 — Evidencia técnica de la evaluación

### Verificaciones realizadas

- `python manage.py check`: **correcto, sin errores reportados**.
- Migraciones del proyecto: **aplicadas**.
- Rutas de los módulos: **registradas en `config/urls.py`**.
- Aplicaciones Django evaluadas: **30**.
- Migraciones encontradas: **92**.
- Modelos registrados: **216 modelos Django**.
- Usuarios y grupos CRUD por módulo: **verificados**.
- Superusuario global de Tecnología: **verificado**.

### Alcance de esta evidencia

La evidencia confirma la integración técnica y el funcionamiento del flujo
principal. No equivale por sí sola a una certificación de cumplimiento legal,
ISO, seguridad informática o auditoría financiera.

---

## Diapositiva 12 — Ventajas

- Arquitectura modular: permite crecer sin rehacer el sistema completo.
- Unifica información de áreas operativas y administrativas.
- Reduce duplicidad de registros y seguimiento manual.
- Mejora la trazabilidad institucional.
- Permite delegar acceso sin entregar privilegios globales.
- Facilita indicadores transversales para la dirección.
- Incluye áreas normalmente olvidadas en ERPs genéricos.
- Puede ejecutarse inicialmente en red interna.
- Tiene una base adecuada para integrar reportes, notificaciones y flujos de
  aprobación.
- Es adaptable a las necesidades de una organización venezolana.

---

## Diapositiva 13 — Desventajas y limitaciones actuales

- El sistema todavía requiere pruebas automatizadas más amplias por módulo.
- La suite completa de pruebas no finalizó correctamente durante esta evaluación
  por un problema de descubrimiento de módulos de pruebas.
- Algunas funcionalidades deben validarse con usuarios reales y datos reales.
- Los datos médicos, jurídicos y de auditoría requieren controles reforzados.
- El cumplimiento normativo está modelado como controles y catálogos; no sustituye
  la revisión de un abogado, contador, especialista SST o auditor certificado.
- La configuración predeterminada no debe exponerse directamente a Internet.
- Se requiere endurecer configuración de producción, HTTPS, secretos, copias de
  seguridad y monitoreo.
- Deben definirse políticas de retención, respaldo y recuperación ante desastres.
- La migración desde sistemas actuales requiere levantamiento y depuración de
  datos.

---

## Diapositiva 14 — Riesgos antes de una publicación pública

### Prioridad alta

- Cambiar la `SECRET_KEY` de desarrollo por una variable segura.
- Ejecutar con `DEBUG=False`.
- Restringir `ALLOWED_HOSTS` a dominios e IP autorizados.
- Configurar HTTPS, cookies seguras y protección HSTS.
- Usar PostgreSQL administrado en lugar de depender de SQLite para producción.
- Establecer respaldos automáticos y pruebas de restauración.
- Revisar permisos sobre información médica, jurídica y de personal.

### Prioridad media

- Completar pruebas de integración y aceptación por módulo.
- Añadir auditoría de operaciones sensibles.
- Definir observabilidad: errores, rendimiento, disponibilidad y alertas.
- Documentar procedimientos operativos y de recuperación.
- Capacitar usuarios y responsables funcionales.

---

## Diapositiva 15 — Plan recomendado de puesta en marcha

### Fase 1 — Piloto interno

- Seleccionar Producción, Tecnología, RRHH y Gerencia.
- Usar datos de prueba y un grupo pequeño de usuarios.
- Validar flujos diarios y permisos.

### Fase 2 — Validación institucional

- Revisar normas, formatos y responsables.
- Confirmar indicadores y reportes requeridos.
- Formalizar catálogos, consecutivos y políticas de aprobación.

### Fase 3 — Producción controlada

- Activar HTTPS, respaldos, monitoreo y base de datos productiva.
- Migrar datos depurados.
- Capacitar por área.
- Operar con mesa de ayuda y control de incidencias.

### Fase 4 — Escalamiento

- Integrar correo, notificaciones, firma digital y reportes.
- Optimizar consultas e indicadores.
- Habilitar nuevos módulos según prioridades directivas.

---

## Diapositiva 16 — Mensaje para redes sociales

### Opción 1 — Enfoque integral y productividad

**Título:** Del hilo a la entrega: el ERP diseñado para escalar tu fábrica textil.

Unificar la cadena de producción textil no tiene por qué ser un caos. ERP Textil
Venezuela conecta las áreas de la empresa en tiempo real:

- **Operaciones y logística:** inventario, compras, insumos y flota de transporte.
- **Planta y producción:** órdenes de manufactura y control de calidad con enfoque
  de procesos alineado a ISO 9001:2015.
- **Administración y finanzas:** tesorería, RRHH, salud ocupacional y facturación
  fiscal.
- **Dirección estratégica:** indicadores gerenciales y trazabilidad mediante
  registro de auditoría.

Optimiza tus costos operativos y toma el control de tu fábrica.

**Llamado a la acción:** Agenda una demo personalizada hoy.

### Opción 2 — Enfoque dolor / solución

**Título:** ¿Cuellos de botella en producción, inventarios descuadrados o falta de
trazabilidad?

Centraliza la gestión de tu empresa textil con un ecosistema modular:

- **Trazabilidad total:** registro de auditoría para conocer qué ocurre y quién
  ejecuta cada acción.
- **Salud y personal:** RRHH, servicios médicos ocupacionales y gestión de
  jornadas.
- **Control legal y de calidad:** consultoría jurídica, auditoría interna y
  estandarización de procesos basada en ISO 9001:2015.

Transformamos la complejidad de la manufactura en procesos controlables,
medibles y orientados a la rentabilidad.

**Llamado a la acción:** Solicita más información y moderniza tu planta.

### Versión institucional

> Presentamos ERP Textil Venezuela, una plataforma integral para conectar
> producción, logística, compras, ventas, finanzas, talento humano, tecnología,
> seguridad, calidad y gestión directiva en un solo sistema.
>
> Más trazabilidad. Más control. Mejores decisiones.
>
> Diseñado para acompañar la transformación digital de organizaciones textiles e
> industriales en Venezuela.

### Versión corta

> ERP Textil Venezuela: producción, administración, seguridad, tecnología y
> gerencia conectadas en una sola plataforma.

### Llamados sugeridos

- “Conoce nuestra transformación digital.”
- “Del registro manual a la gestión trazable.”
- “Indicadores para decidir. Módulos para operar.”
- “Un ERP diseñado para nuestra realidad.”

### Mensajes por perfil de cliente

| Perfil | Dolor principal | Módulos a destacar | Propuesta de valor |
|---|---|---|---|
| Gerente de planta / producción | Retrasos en órdenes y falta de insumos | Producción, Compras, Logística y Mantenimiento | Insumos disponibles, flujo de manufactura trazable y menos interrupciones |
| Director general / CEO | Falta de visibilidad y riesgos normativos | Gerencia, Auditoría Interna, Gerencia de Calidad y Consultoría Jurídica | Reportes ejecutivos, control de auditoría y procesos alineados a ISO 9001:2015 |
| Jefe de Recursos Humanos | Ausentismo y poca integración de salud ocupacional | RRHH, Servicios Médicos y Atención a la Ciudadanía | Información laboral y seguimiento ocupacional centralizados, con acceso controlado |

### Recomendaciones de publicación

- Usar la **Opción 1** para LinkedIn, presentaciones institucionales y campañas
  de posicionamiento.
- Usar la **Opción 2** para campañas B2B orientadas a formularios o solicitudes
  de demo.
- Segmentar los anuncios por cargo y mostrar únicamente funcionalidades
  disponibles en el entorno demostrado.
- Sustituir “en tiempo real” por “actualizado en el sistema” cuando el flujo
  dependa de una carga manual o de una integración aún no habilitada.
- No afirmar certificación ISO, cumplimiento legal automático ni resultados
  financieros garantizados: el ERP aporta controles y trazabilidad, pero la
  certificación y la validación normativa requieren responsables competentes.

---

## Diapositiva 17 — Guion de demostración de 10 minutos

1. **Minuto 1:** presentar el problema y la propuesta de valor.
2. **Minutos 2–3:** mostrar login, dashboard y menú por permisos.
3. **Minutos 4–5:** mostrar un flujo operativo de Producción o Compras.
4. **Minutos 6–7:** mostrar Tecnología: ticket, inventario e indicador.
5. **Minuto 8:** mostrar Gerencia y sus indicadores integrales.
6. **Minuto 9:** demostrar la vista móvil.
7. **Minuto 10:** presentar ventajas, plan piloto y próximos pasos.

---

## Diapositiva 18 — Conclusión ejecutiva

### Evaluación global

**Resultado:** plataforma con alto potencial institucional y base funcional
avanzada para iniciar un piloto controlado.

### Recomendación

Autorizar una fase de piloto interno, condicionada a:

1. Completar pruebas funcionales y de seguridad.
2. Endurecer la configuración de producción.
3. Validar los flujos con los responsables de cada gerencia.
4. Definir un plan de respaldo, soporte y capacitación.
5. Aprobar una hoja de ruta de implementación por fases.

**No se recomienda presentarla todavía como producto certificado o totalmente
listo para exposición pública sin completar esas condiciones.**

---

## Anexo — Ficha técnica para la directiva

| Elemento | Evaluación |
|---|---|
| Tipo | ERP web modular |
| Backend | Django / Python |
| Base de datos | SQLite para entorno local; PostgreSQL configurable |
| Interfaz | HTML, CSS, Bootstrap, Bootstrap Icons |
| Usuarios | Usuario personalizado, áreas, roles y grupos |
| Acceso | Módulo, submódulo y superusuario |
| Indicadores | Dashboard principal y dashboard de Gerencia |
| Aplicaciones registradas | 30 aplicaciones Django |
| Modelos registrados | 216 modelos Django |
| Migraciones encontradas | 92 |
| Estado de `manage.py check` | Correcto |
| Pruebas automatizadas | Suite ejecutable con pruebas de módulos y flujos principales; falta ampliar cobertura CRUD y permisos |
| Uso recomendado actual | Demo y piloto interno |
| Condición para producción pública | Hardening, pruebas, respaldos y HTTPS |
