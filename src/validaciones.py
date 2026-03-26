import streamlit as st
import re
from datetime import datetime
from conexion import Conexion

conector = (
    "DRIVER={SQL Server};"
    "SERVER=LAPTOP-ADRIAN\\SQLEXPRESS;"
    "DATABASE=almacenamiento;"
    "Trusted_Connection=yes;"
)
c1 = Conexion(conector=conector)


class Validaciones:
    """
    Crea las validaciones necesarias para todos los datos de la aplicación.
    """

    def __init__(self):
        """
        Inicializa la clase Validaciones sin atributos adicionales.
        """

    def validar_nombre(self, valor, campo, obligatorio=True, tipo="persona"):
        """
        Valida un nombre generico con las siguientes verificaciones:
        - Si tipo es 'persona' valida solo letras y espacios, rechaza números y caracteres especiales.
        - Si tipo es 'pelicula' acepta letras, números y caracteres especiales típicos de títulos.
        - Si está vacío y es obligatorio lanza error de campo vacío.
        - Si no cumple el formato según el tipo lanza error de formato.
        """
        valor = str(valor).strip()

        if not valor:
            if obligatorio:
                raise ValueError(
                    f"Error de campo vacío: El campo '{campo}' es obligatorio."
                )
            return

        if tipo == "persona":
            if not isinstance(valor, str):
                raise ValueError(
                    f"Error de tipo: Se esperaba una cadena de texto para el campo '{campo}'."
                )
            if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", valor):
                raise ValueError(
                    f"Error de formato: El campo '{campo}' solo puede contener letras y espacios."
                )

        elif tipo == "pelicula":
            if len(valor) > 200:
                raise ValueError(
                    f"Error de longitud: El campo '{campo}' excede los 200 caracteres permitidos (actual: {len(valor)})."
                )
            if not re.match(r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\:\-\'\.\!\?\&\(\)\,]+$", valor):
                raise ValueError(
                    f"Error de formato: El campo '{campo}' contiene caracteres no permitidos."
                )

        else:
            raise ValueError(
                f"Error de tipo: El tipo '{tipo}' no es válido. Use 'persona' o 'pelicula'."
            )

    def parsear_nombre(self, valor):
        """
        Separa un nombre completo en primer y segundo nombre con las siguientes verificaciones:
          - Si el valor no es string lanza error de tipo.
          - Si está vacío lanza error de campo vacío.
          - Si solo hay una palabra, el segundo nombre retorna como None.
        """
        if not isinstance(valor, str):
            raise ValueError(
                "Error de tipo: Se esperaba una cadena de texto para parsear el nombre."
            )

        if not valor.strip():
            raise ValueError(
                "Error de campo vacío: El valor para parsear el nombre no puede estar vacío."
            )

        partes = valor.strip().split()
        p = partes[0] if len(partes) > 0 else None
        s = partes[1] if len(partes) > 1 else None
        return p, s

    def extraer_listas(self, tabla):
        """
        Extrae un diccionario con los datos de una tabla con las siguientes verificaciones:
          - Si el valor no es string lanza error de tipo.
          - Si está vacío lanza error de campo vacío.
          - Si contiene caracteres distintos a letras y guiones bajos lanza error de formato.
          - Si pasa las validaciones ejecuta la consulta y retorna un diccionario {nombre: id}.
        """
        if not isinstance(tabla, str):
            raise ValueError(
                "Error de tipo: El nombre de la tabla debe ser una cadena de texto."
            )

        if not tabla.strip():
            raise ValueError(
                "Error de campo vacío: El nombre de la tabla no puede estar vacío."
            )

        if not re.match(r"^[a-zA-Z_]+$", tabla.strip()):
            raise ValueError(
                "Error de formato: El nombre de la tabla contiene caracteres no permitidos (solo letras y guiones bajos)."
            )

        query = f"SELECT id_{tabla.lower()}, nombre FROM {tabla}"
        filas = c1.ejecutar_consulta(query=query)
        return {fila[1]: fila[0] for fila in filas}

    def validar_fecha(self, fecha):
        """
        Valida una fecha en formato DD/MM/AAAA con las siguientes verificaciones:
          - Si el valor no es string lanza error de tipo.
          - Si está vacío lanza error de campo vacío.
          - Si no cumple el formato DD/MM/AAAA lanza error de formato.
          - Si el día o mes no son reales lanza error de fecha inválida.
          - Si el año supera el año actual lanza error de rango.
        """
        if not isinstance(fecha, str):
            raise ValueError("Error de tipo: La fecha debe ser una cadena de texto.")

        if not fecha.strip():
            raise ValueError("Error de campo vacío: La fecha de subida es obligatoria.")

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha.strip()):
            raise ValueError(
                "Error de formato: La fecha debe seguir el formato DD/MM/AAAA (ejemplo: 25/03/2024)."
            )

        try:
            fecha_obj = datetime.strptime(fecha.strip(), "%d/%m/%Y")
        except ValueError:
            raise ValueError(
                f"Error de fecha inválida: '{fecha.strip()}' no corresponde a una fecha real (verifique día y mes)."
            )

        if fecha_obj.year > datetime.now().year:
            raise ValueError(
                f"Error de rango: El año {fecha_obj.year} no puede ser mayor al año actual ({datetime.now().year})."
            )

    def validar_edad(self, valor, obligatorio=True):
        """
        Valida una edad con las siguientes verificaciones:
        - Si está vacío y es obligatorio lanza error de campo vacío.
        - Si el valor no es numérico lanza error de tipo.
        - Si el valor es menor a 0 lanza error de rango.
        - Si supera el límite permitido lanza error de rango sin especificar el límite.
        """
        valor = str(valor).strip()

        if not valor:
            if obligatorio:
                raise ValueError("Error de campo vacío: La edad es obligatoria.")
            return

        if not re.match(r"^\d+$", valor):
            raise ValueError(
                "Error de tipo: La edad debe ser un número entero positivo."
            )

        edad = int(valor)

        if edad < 0:
            raise ValueError("Error de rango: La edad debe ser mayor o igual a 0.")

        if edad > 50:
            raise ValueError("Error de rango: La edad ingresada no es válida.")

    def validar_numero(self, valor, campo, obligatorio=True, minimo=0, maximo=999):
        f"""
        Valida que se ingrese un numero entero con las siguientes condiciones.
        - Si está vacío y es obligatorio lanza error de campo vacío.
        - Si el valor no es numérico lanza error de tipo.
        - Si el valor es menor a minimo lanza error de rango.
        - Si el valor es mayor a maximo lanza un error de rango.
        """
        valor = str(valor).strip()

        if not valor:
            if obligatorio:
                raise ValueError(f"Error de campo vacío: {campo} es obligatoria.")
            return

        if not re.match(r"^\d+$", valor):
            raise ValueError(
                f"Error de tipo: {campo} debe ser un número entero positivo."
            )

        numero = int(valor)

        if numero <= minimo:
            raise ValueError(f"Error de rango: {campo} debe ser mayor o igual a 0.")

        if numero >= maximo:
            raise ValueError(f"Error de rango: {campo} ingresada no es válida.")
