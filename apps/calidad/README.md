# Coordinación de Aseguramiento de la Calidad

Este módulo adapta el manual de procedimientos de la Coordinación de
Aseguramiento de la Calidad del Complejo Industrial Tiuna. Registra siete
procedimientos diferenciados:

1. Verificación en proceso y despacho de corte.
2. Aprobación de la prenda de arranque de producción.
3. Verificación en proceso de línea de costura.
4. Inspección final de prenda terminada.
5. Inspección de bordado y auditoría de remate.
6. Verificación final de prendas empacadas.
7. Verificación de avíos y telas.

Cada auditoría conserva orden de trabajo/orden de producción, cliente, prenda,
talla, línea, ficha técnica o de arte, tamaño de muestra, piezas aprobadas y
rechazadas, clasificación de defectos, controles ejecutados, decisión,
observaciones, reproceso y validación del inspector.

Las reglas principales del manual se validan en servidor:

- una auditoría de costura registra al menos cinco piezas por operación;
- la inspección de materia prima registra prueba de solidez y color;
- las piezas aprobadas y rechazadas no superan la muestra inspeccionada;
- un registro aprobado no puede conservar piezas rechazadas sin quedar
  observado, en reproceso o rechazado.

Ruta: `/calidad/`.
