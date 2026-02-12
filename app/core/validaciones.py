import re

def validar_numero(valor, permitir_decimal=False):
    if valor is None:
        return 0

    txt = str(valor).strip().replace(",", ".")
    if txt == "":
        return 0

    if permitir_decimal:
        patron = r"^\d{1,4}(\.\d{1,2})?$"
        if not re.match(patron, txt):
            raise ValueError("Número decimal inválido")
        return round(float(txt), 2)
    else:
        if not txt.isdigit() or len(txt) > 4:
            raise ValueError("Número entero inválido")
        return int(txt)


def normalizar_decimal_api(valor):
    try:
        if valor in (None, "", " "):
            return 0.0
        num = float(str(valor).replace(",", "."))
        if num < 0:
            return 0.0
        return round(num, 2)
    except Exception:
        return 0.0
