# Módulo PRODUCCIÓN TEXTIL — ERP
## Django + PostgreSQL | Bootstrap 5 + Bootstrap Icons

---

Este módulo gestiona el flujo UDP, Corte, Producción textil, Pool de calidad, Bordados y Despacho. Incluye trazabilidad por lote, planes de proceso, indicadores, notificaciones y no conformidades alineados con ISO 9001:2015. Las referencias venezolanas deben ser confirmadas por el responsable de calidad según el producto y contrato aplicable.

## 📦 Estructura del módulo

```
apps/produccion/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── urls.py
├── views.py
├── migrations/
│   └── __init__.py
└── templates/produccion/
    ├── dashboard_produccion.html
    ├── materia_prima_list.html
    ├── materia_prima_form.html
    ├── materia_prima_ajuste_stock.html
    ├── producto_terminado_list.html
    ├── producto_terminado_form.html
    ├── formula_list.html
    ├── formula_form.html
    ├── formula_detail.html
    ├── orden_list.html
    ├── orden_form.html
    ├── orden_detail.html
    ├── lote_list.html
    ├── lote_form.html
    ├── lote_detail.html
    └── control_calidad_form.html
```

---

## 🗃️ Modelos textiles y de calidad

| Modelo                      | Descripción                                                  |
|-----------------------------|--------------------------------------------------------------|
| `CategoriaProductoTerminado`| Agrupación de productos terminados                           |
| `CategoriaMateriaPrima`     | Agrupación de materias primas                                |
| `ProductoTerminado`         | Producto final con stock y costo estimado                    |
| `MateriaPrima`              | Insumo con stock, costo y alerta de mínimo                   |
| `OrdenProduccion`           | Orden y lote físico de una prenda                            |
| `DepartamentoUDP`           | Diseño, ficha técnica, tallaje y requerimientos              |
| `DepartamentoCorte`         | Programación, mesa de corte, calidad, fusionado, habilitado y carro de carga |
| `DepartamentoProduccionTextil` | Confección por línea y fallas de costura                   |
| `DepartamentoCalidadISO9001`| Pool de calidad y liberación del lote                        |
| `DepartamentoBordado`       | Logos, nombres y emblemas                                    |
| `DepartamentoDespacho`      | Planchado, fibras sueltas, empaque y entrega                 |
| `CatalogoProceso`            | Catálogo maestro de los seis procesos                        |
| `ProcesoDepartamento`       | Plan documentado por orden, versión y cláusula ISO            |
| `IndicadorProceso`           | Definición de KPI y objetivo                                 |
| `MedicionIndicador`          | Evidencia fechada de medición                                |
| `Notificacion`               | Avisos de avance y calidad                                   |
| `NoConformidad`              | Registro, causa y acción correctiva                          |
| `RegistroProduccionTurno`    | Control bi-horario de meta, avance, rechazo, paradas y materiales por línea |
| `MuestraPrenda`              | Requisitos del cliente, confección, inspección y aprobación de la muestra |
| `DigitalizacionMolde`        | Expediente Audaces: molde base, piezas, tallas, medidas, versión y tizado |
| `ProgramacionProduccion`     | Planificación PCPI de fechas, cuotas, capacidad, líneas y restricciones |
| `OrdenTrabajoProduccion`     | Orden formal distribuida a UDP, Corte, Logística y áreas productivas |

---

## 🔄 Flujo textil implementado

### Orden de producción
```
UDP → Programación de corte → Mesa de corte → Calidad en proceso
→ Fusionado/Habilitado → Calidad post corte → Carro de carga
→ Línea de confección → Bordados → Despacho → Pool → Completada
```

Cada transición genera una notificación. Un rechazo igual o superior al 5% abre una no conformidad y retiene el lote para análisis del Pool.

### Documentos previos a la producción

Desde el detalle de cada orden se registran los documentos exigidos por los
manuales de UDP y PCPI:

1. **Muestra de prenda:** conserva requisitos del cliente, referencia física,
   materiales, medidas, inspección y aprobación.
2. **Digitalización Audaces:** relaciona la muestra con el molde base, piezas
   digitalizadas, tallas escaladas, hoja de medidas, versión y referencia del
   archivo/tizado. El tizado solo se marca disponible cuando el expediente
   queda validado.
3. **Programación PCPI:** registra fechas, periodicidad, tiempo estándar,
   capacidad, línea, disponibilidad de maquinaria, calidad de materia prima,
   restricciones y escenarios.
4. **Orden de trabajo:** formaliza la secuencia de fabricación, cuotas y áreas
   destinatarias. No puede aprobarse o distribuirse sin hoja de consumo y
   solicitud de materiales disponibles.

Los campos `referencia_archivo` y `referencia_archivo_audaces` son referencias
documentales, no una subida directa de archivos. Esto evita almacenar formatos
propietarios sin validación de extensión, tamaño y almacenamiento; la
integración de adjuntos debe realizarse posteriormente con una política de
almacenamiento aprobada.

### Ruta y control del corte

En cada orden, **Gestionar Corte** registra:

1. Programación, orden de corte, jefe, supervisor y equipo de cortadores/ayudantes.
2. Disponibilidad de tela y consumibles, ficha técnica, tizado digital o manual y aprovechamiento.
3. Tendido, piezas obtenidas, validación del tipo de tela y calidad durante el procesamiento.
4. Partes fusionadas, conteo, paquete completo y habilitado.
5. Revisión de la mesa principal de calidad post corte, línea destino y envío al carro de carga.

El corte solo puede pasar a confección cuando todos los controles están conformes. Si existe una irregularidad, el supervisor debe mantener el corte retenido, registrar la observación y corregir antes de marcarlo como habilitado.

## 📊 Indicadores iniciales

Se cargan mediante la migración `0008_seed_produccion_textil`: merma de tela, rechazo en corte, FPY de confección, FPY del Pool, rechazo de bordados y OTIF de Despacho.

## 🔧 Plan de mantenimiento mecánico textil

El dashboard de **Mecánica Industrial Textil** contempla el procedimiento del Complejo Industrial Tiuna:

- Planes preventivos con periodicidad semanal, mensual, trimestral o anual, objetivo, alcance, actividades y aprobación de jefatura.
- Órdenes preventivas, correctivas y predictivas con actividades realizadas, bloqueo de seguridad, prueba de costura, aceptación de muestra, garantía y minuta.
- Minuta diaria con máquinas intervenidas, novedades, restricciones, herramientas y seguridad.
- Traslado de máquinas con orden de Ingeniería, ficha, origen/destino, supervisión, aprobación, instalación, calibración y verificación de espacios en líneas.
- Diagnóstico codificado de elementos de máquina, estado, resultado y necesidad de repuesto.
- Solicitud de piezas vinculada a Logística/Compras.

Una orden de mantenimiento no puede marcarse como completada desde el formulario si no registra los controles de seguridad, prueba de costura, aceptación de muestra y minuta correspondiente.

## ✅ Gestión de calidad: NC, OM y SNC

El menú **No conformidades** implementa el procedimiento de Gestión de
No Conformidad/Oportunidad de Mejora `NOV-2025 PRC-GC-003 Rev. 06` y el
procedimiento de Salidas No Conformes `PRC-GC-005 Rev. 01` de forma
adaptada al flujo textil.

Cada registro permite clasificar:

- **NC:** incumplimiento de un requisito del producto, proceso, cliente,
  documento o norma.
- **OM:** oportunidad de mejora para el Sistema de Gestión de la Calidad.
- **SNC:** salida o producto no conforme detectado en recepción, corte,
  confección, bordado, calidad, despacho o después de la entrega.

El formulario conserva la trazabilidad de orden/lote, tipo, origen, requisito,
ubicación, persona que detecta, cantidad, porcentaje de rechazo, riesgo,
contención, causa raíz, acción correctiva y tratamiento. Los tratamientos
disponibles son corrección, reproceso, separación/contención, rechazo/desecho
y liberación bajo concesión.

Una SNC liberada bajo concesión exige registrar la autorización documentada.
Un registro no puede cerrarse hasta indicar fecha y criterio de verificación,
resultado y eficacia de la acción; esto materializa la verificación de eficacia
de ISO 9001:2015, cláusula 10.2. Los registros permanecen asociados a la
orden y pueden ser consultados por Calidad y los responsables del proceso.

## 📘 Manual operativo y control bi-horario

El enlace **Manual operativo** del dashboard incorpora al ERP el manual de
la Jefatura de Producción: roles de Jefatura, Galpón, Corte, Supervisión,
Bordado, Acabado, Calidad y Mecánica; flujo de documentos; reglas de
calidad, seguridad y 5S; y registros que deben conservarse.

El enlace **Control bi-horario** permite al líder o supervisor registrar por
orden, línea, fecha, turno y período de dos horas:

- meta, piezas buenas y piezas rechazadas;
- minutos planificados y paradas con causa;
- cuellos de botella y disponibilidad de materiales;
- observaciones y usuario responsable.

El sistema calcula la eficiencia del período como `piezas buenas / meta x
100` y conserva el registro para los indicadores de la Jefatura. La ruta
operativa es `produccion/registros-turno/`.

---

## ⚙️ Instalación

### 1. settings.py
```python
INSTALLED_APPS = [
    ...
    'apps.core',
    'apps.rrhh',
    'apps.compras',
    'apps.ventas',
    'apps.produccion',   # ← agregar
]
```

### 2. config/urls.py
```python
path('produccion/', include('apps.produccion.urls', namespace='produccion')),
```

### 3. Migrar
```bash
python manage.py makemigrations produccion
python manage.py migrate
```

---

## 🔗 URLs (35 rutas)

| Grupo              | Rutas principales                                                      |
|--------------------|------------------------------------------------------------------------|
| Dashboard          | `/produccion/`                                                         |
| Materias Primas    | lista / nueva / editar / ajuste-stock                                  |
| Productos Terminados| lista / nuevo / editar                                                |
| Fórmulas           | lista / nueva / detalle / editar / agregar-línea / calcular-costos / activar |
| Órdenes            | lista / nueva / detalle / iniciar / pausar / reanudar / completar / anular / consumo |
| Lotes              | lista / nuevo / detalle / enviar-control / liberar                     |
| Control Calidad    | crear desde lote                                                       |

---

## 🧪 Particularidades — Productos de Limpieza

- Control de calidad con parámetros específicos: **pH, viscosidad, densidad, color, olor, aspecto**
- Alertas de stock bajo para materias primas y productos terminados
- Ajuste manual de stock de materia prima (compras, mermas, inventario)
- Trazabilidad completa: Fórmula → Orden → Lote → Control QC → Almacén
- Costo automático: al registrar consumos reales, el costo de la orden se actualiza

---

## 📊 Progreso del ERP

| # | Módulo        | Estado       |
|---|---------------|--------------|
| 1 | `core`        | ✅ Completado |
| 2 | `rrhh`        | ✅ Completado |
| 3 | `compras`     | ✅ Completado |
| 4 | `ventas`      | ✅ Completado |
| 5 | `produccion`  | ✅ Completado |
| 6 | `tesoreria`   | ⏳ Pendiente  |
| 7 | `contabilidad`| ⏳ Pendiente  |
| 8 | `transportes` | ⏳ Pendiente  |
