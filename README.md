```markdown
# PyWoo v1  
Aplicación de Gestión WooCommerce con Interfaz Gráfica (GUI)

PyWoo es una aplicación de escritorio desarrollada en Python con PySide6 que permite gestionar información clave de una tienda WooCommerce a través de una interfaz gráfica moderna, intuitiva y modular. La aplicación centraliza procesos administrativos como reportes de ventas, inventario, actualización de productos y generación de listas para distribuidores, reduciendo la dependencia de procesos manuales y del panel web de WooCommerce.

---

## Características Principales

- Interfaz gráfica moderna desarrollada con PySide6  
- Conexión directa con la API REST de WooCommerce  
- Gestión centralizada de credenciales mediante archivo `.env`  
- Exportación automática de información a Excel (XLSX)  
- Indicadores de progreso en tiempo real  
- Arquitectura modular y escalable  
- Separación clara entre lógica de negocio y presentación (MVC)  
- Diseñada para usuarios no técnicos  

---

## Módulos del Sistema

### Reporte de Ventas
- Selección de rango de fechas con validación
- Obtención de órdenes desde WooCommerce
- Visualización en dos pestañas:
  - Productos Simples
  - Productos Variados
- Exportación automática a Excel
- Barra de progreso durante la generación
- Encabezados estandarizados en mayúsculas y negrita

### Inventario
- Filtros disponibles:
  - Todos los productos
  - Productos con stock
  - Productos sin stock
- Visualización en dos pestañas:
  - Productos Simples
  - Productos Variados
- Exportación del inventario a Excel
- Selección exclusiva de filtros
- Progreso visual durante la carga de datos

### Actualizar Productos
- Carga de archivos Excel o CSV
- Validación de formato y encabezados:
  - SKU
  - PRECIO_VENTA
- Actualización masiva de productos en WooCommerce
- Edición controlada desde la tabla:
  - Stock
  - Precio de compra
  - Precio de venta
- Estado de actualización:
  - Actualizado
  - Sin actualizar
- Exportación del resultado final a Excel

### Lista de Distribuidores
- Obtención de productos desde WooCommerce
- Cálculo de precios, descuentos y márgenes
- Visualización en tablas con encabezados definidos
- Exportación a Excel con formato específico para distribuidores
- Barra de progreso y mensajes de estado

---

## Menú y Navegación

- Menú principal con acceso a todos los módulos
- Menú superior:
  - WooCommerce → Credenciales API
  - Ayuda → Acerca de

### Acerca de
- PyWoo v1  
- Aplicación de gestión administrativa para WooCommerce  
- Desarrollado por Sami Aldaz  

---

## Estructura del Proyecto

```

PyWoo/
├── pywoo.py
├── requirements.txt
├── README.md
├── .env
│
├── app/
│   ├── core/
│   │   ├── cliente_woocommerce.py
│   │   ├── configuracion.py
│   │   ├── excepciones.py
│   │   ├── dialogos.py
│   │   └── controlador_credenciales.py
│   │
│   ├── menu/
│   │   ├── menu_view.py
│   │   └── ui/
│   │
│   ├── reporte_ventas/
│   ├── inventario/
│   ├── actualizar_productos/
│   └── lista_distribuidores/
│
└── assets/

````

---

## Instalación

### Requisitos Previos
- Python 3.9 o superior
- pip
- Conexión a Internet
- Acceso a una tienda WooCommerce con API habilitada

### Instalación de Dependencias

```bash
pip install -r requirements.txt
````

### Dependencias Principales

* PySide6
* requests
* openpyxl
* python-dotenv

---

## Configuración

### Archivo .env

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
WC_URL=https://tu-tienda.com
WC_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Obtener Credenciales de WooCommerce

1. Ingresar al panel de WordPress
2. WooCommerce → Configuración → Avanzado → API REST
3. Crear una nueva clave
4. Asignar permisos de Lectura y Escritura
5. Copiar el Consumer Key y Consumer Secret

---

## Ejecución

```bash
python pywoo.py
```

Al iniciar, la aplicación mostrará la ventana de Credenciales API y posteriormente el Menú Principal.

---

## Arquitectura del Sistema

### Principios Aplicados

* Modelo–Vista–Controlador (MVC)
* Separación de responsabilidades
* Código reutilizable y mantenible
* Arquitectura modular

### Beneficios

* Fácil incorporación de nuevos módulos
* Código claro y documentado
* Interfaz desacoplada de la lógica de negocio

---

## Manejo de Errores

* Validación de credenciales
* Manejo de errores de conexión con WooCommerce
* Mensajes claros para el usuario
* Uso de excepciones personalizadas (PyWooError)

---

## Licencia

Proyecto académico y de uso interno.
No destinado a distribución comercial.

---

## Autor

Sami Aldaz
PyWoo v1
Aplicación de Gestión WooCommerce con PySide6

```
```
