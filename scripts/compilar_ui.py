import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

UI_FILES = [
    ("app/core/ui/view_credenciales_api.ui", "app/core/ui/ui_view_credenciales_api.py"),
    ("app/menu/ui/view_menu.ui", "app/menu/ui/ui_view_menu.py"),
    ("app/reporte_ventas/ui/view_reporte_ventas.ui", "app/reporte_ventas/ui/ui_view_reporte_ventas.py"),
    ("app/inventario/ui/view_inventario.ui", "app/inventario/ui/ui_view_inventario.py"),
    ("app/actualizar_productos/ui/view_actualizar_productos.ui", "app/actualizar_productos/ui/ui_view_actualizar_productos.py"),
    ("app/lista_distribuidores/ui/view_lista_distribuidores.ui", "app/lista_distribuidores/ui/ui_view_lista_distribuidores.py"),
    ("app/core/ui/proceso.ui", "app/core/ui/ui_proceso.py"),
]

QRC_FILE = ("iconos.qrc", "iconos_rc.py")


def run(cmd: list[str]):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    # Compilar .ui
    for ui, py in UI_FILES:
        ui_path = ROOT / ui
        py_path = ROOT / py
        py_path.parent.mkdir(parents=True, exist_ok=True)
        run(["pyside6-uic", str(ui_path), "-o", str(py_path)])

    # Compilar .qrc (iconos)
    qrc_in = ROOT / QRC_FILE[0]
    qrc_out = ROOT / QRC_FILE[1]
    run(["pyside6-rcc", str(qrc_in), "-o", str(qrc_out)])

    print("\n✅ Listo: UI y recursos compilados.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("\n❌ Error compilando assets:", e)
        sys.exit(1)
