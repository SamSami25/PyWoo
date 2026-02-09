from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


def _is_present(v: Any) -> bool:
    """True si el valor cuenta como "dato real" (no vacío)."""
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    return True


def prune_empty_columns(
    rows: List[Dict[str, Any]],
    headers: Sequence[str],
    keys: Sequence[str],
    optional_keys: Iterable[str],
) -> Tuple[List[str], List[str]]:
    """Quita columnas opcionales que no tengan datos reales en ninguna fila.

    - Solo afecta a columnas incluidas en optional_keys.
    - Conserva el orden original de headers/keys.
    """
    opt: Set[str] = set(optional_keys)
    present: Set[str] = set()

    # Detectar qué columnas opcionales tienen al menos un dato "real".
    for r in rows:
        for k in opt:
            if _is_present(r.get(k)):
                present.add(k)

    new_headers: List[str] = []
    new_keys: List[str] = []
    for h, k in zip(headers, keys):
        if k in opt and k not in present:
            continue
        new_headers.append(h)
        new_keys.append(k)

    return new_headers, new_keys
