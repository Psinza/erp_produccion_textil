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
| `DepartamentoCorte`         | Tendido, validación de tela y habilitación                   |
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

---

## 🔄 Flujo textil implementado

### Orden de producción
```
UDP → Corte → Bordados → Producción textil → Despacho → Pool → Completada
```

Cada transición genera una notificación. Un rechazo igual o superior al 5% abre una no conformidad y retiene el lote para análisis del Pool.

## 📊 Indicadores iniciales

Se cargan mediante la migración `0008_seed_produccion_textil`: merma de tela, rechazo en corte, FPY de confección, FPY del Pool, rechazo de bordados y OTIF de Despacho.

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
