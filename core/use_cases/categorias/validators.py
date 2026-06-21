def normalizar_tipo_categoria(valor: str) -> str:
    return (valor or "").strip()


def validar_tipo_categoria(tipo_categoria: str):
    tipo = normalizar_tipo_categoria(tipo_categoria)

    if not tipo:
        raise RuntimeError("El tipo de categoría es obligatorio")

    if len(tipo) < 3:
        raise RuntimeError("El tipo de categoría es demasiado corto. Debe tener al menos 3 caracteres")

    if len(tipo) > 100:
        raise RuntimeError("El tipo de categoría no puede superar los 100 caracteres")

    return tipo