import subprocess

def compilar_ui():
    ui_files = [
        ("app/core/ui/view_credenciales_api.ui", "app/core/ui/ui_view_credenciales_api.py"),
        ("app/menu/ui/view_menu.ui", "app/menu/ui/ui_view_menu.py"),
        ("app/reporte_ventas/ui/view_reporte_ventas.ui", "app/reporte_ventas/ui/ui_view_reporte_ventas.py"),
        ("app/inventario/ui/view_inventario.ui", "app/inventario/ui/ui_view_inventario.py"),
        ("app/actualizar_productos/ui/view_actualizar_productos.ui", "app/actualizar_productos/ui/ui_view_actualizar_productos.py"),
        ("app/lista_distribuidores/ui/view_lista_distribuidores.ui", "app/lista_distribuidores/ui/ui_view_lista_distribuidores.py"),
        ("app/core/ui/view_credenciales_api.ui", "app/core/ui/ui_view_credenciales_api.py"),
    ]

    for ui, py in ui_files:
        subprocess.run(["pyside6-uic", ui, "-o", py], check=True)

    print("✔ Interfaces UI compiladas correctamente")
