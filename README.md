# PyWoo

PyWoo es una aplicación de escritorio (Python + PySide6) para gestionar una tienda WooCommerce mediante la API REST.

## Características
- Interfaz gráfica en **PySide6**.
- Conexión directa a **WooCommerce REST API**.
- Exportación a **Excel (.xlsx)**.
- Barra de progreso y mensajes de estado durante procesos largos.
- Arquitectura modular (controlador + vista + modelo de tabla).

## UX en tablas (aplica a todos los módulos)
- **Ordenamiento asc/desc**: clic en cualquier encabezado.
- **Buscador**: filtra por SKU o nombre (o por Cliente/Pedido en Reporte de Ventas).
- **Selección siempre azul**: la fila encontrada queda resaltada en azul aunque el foco esté en el buscador.
- **Exportación como se ve**: se exporta respetando el **orden** (asc/desc) y el **filtro** activos en la tabla.

## Validaciones
- No se muestran celdas vacías: si WooCommerce no trae un dato, se muestra **N/A**.
- No se permiten valores negativos en cálculos (totales, descuentos, utilidades, precios calculados, etc.).
- Cuando un botón está deshabilitado (por ejemplo **Exportar**), al hacer clic se muestra un mensaje indicando **por qué**.

## Columnas dinámicas
Algunas columnas son opcionales y solo se muestran si existen en la tienda.
Ejemplo: en **Reporte de Ventas**, la columna **Identificación** se muestra únicamente si se encuentra en los datos (billing/meta_data). Si no existe en ningún pedido, la columna no aparece.

## Módulos
- **Reporte de Ventas**: genera pedidos por rango de fechas, muestra métricas y exporta.
- **Inventario**: lista productos simples y variables con filtros de stock.
- **Actualizar Productos**: carga un archivo (CSV/XLSX) para preparar actualizaciones y enviar cambios a WooCommerce.
- **Lista de Distribuidores**: calcula PVP/PVD/ganancia/descuentos y exporta una lista para distribuidores.

## Requisitos
- Python 3.9+ (recomendado 3.10+)
- Conexión a internet
- Tienda WooCommerce con API habilitada

## Instalación
1) Crear y activar entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2) Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración de credenciales
Puedes configurar credenciales desde la UI: **WooCommerce → Credenciales API**.

Opcionalmente también puedes usar un archivo `.env` en la raíz del proyecto:

```env
WC_URL=https://tu-tienda.com
WC_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Ejecución

```bash
python pywoo.py
```

## Estructura del proyecto (resumen)

```
PyWoo/
├── pywoo.py
├── requirements.txt
├── README.md
└── app/
    ├── core/
    ├── menu/
    ├── reporte_ventas/
    ├── inventario/
    ├── actualizar_productos/
    └── lista_distribuidores/
```

## Licencia
Proyecto académico / uso interno.
