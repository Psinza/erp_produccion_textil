# Módulo PCPI

El módulo de Planificación y Control de la Producción e Inventario implementa
los procedimientos `MAN-NORYPROC-CITGPPCPI-0001` a `0004`:

- planificación de fechas de entrega según pedido;
- programación semanal y distribución a UDP, Producción, Ingeniería y Calidad;
- resumen de requerimientos de materiales;
- elaboración y distribución de órdenes de trabajo.

PCPI reutiliza la orden de producción, la hoja de consumo/requerimiento y la
orden de trabajo del módulo de Producción. No duplica esos documentos: los
expedientes PCPI conservan la planificación, las validaciones, referencias de
documentos recibidos y la distribución administrativa.

## Reglas principales

- Una planificación no puede comprometer una fecha anterior a su solicitud.
- Una programación semanal exige un rango de fechas válido y una eficiencia de
  referencia entre 0 y 100%.
- Un resumen emitido, validado, atendido o archivado debe conservar la
  referencia de la hoja de consumo.
- La aprobación definitiva de la orden de trabajo continúa protegida por las
  reglas de Producción: debe existir hoja de consumo y solicitud de materiales.

Ruta operativa: `/pcpi/`.
