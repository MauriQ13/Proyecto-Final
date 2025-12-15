"""
Funciones de validación para la entrada de datos del usuario.
"""


def validate_float(value, field_name):
    """
    Valida que un valor pueda ser convertido a float.
    
    Args:
        value (str): Valor a validar
        field_name (str): Nombre del campo para mensajes de error
        
    Returns:
        float: Valor convertido a float
        
    Raises:
        ValueError: Si el valor no puede ser convertido a float
    """
    if not value or value.strip() == "":
        raise ValueError(f"El campo '{field_name}' no puede estar vacío.")
    
    try:
        return float(value)
    except ValueError:
        raise ValueError(
            f"El campo '{field_name}' debe ser un número válido.\n"
            f"Valor ingresado: '{value}'"
        )
