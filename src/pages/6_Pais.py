import streamlit as st
from validaciones import Validaciones
from conexion import Conexion
import pandas as pd

conector = (
    "DRIVER={SQL Server};"
    "SERVER=LAPTOP-ADRIAN\\SQLEXPRESS;"
    "DATABASE=almacenamiento;"
    "Trusted_Connection=yes;"
)
c1 = Conexion(conector=conector)
v1 = Validaciones()

mostrar, añadir = st.tabs(["Visualizar Pais", "Añadir Nuevo Pais"])

with mostrar:
    st.title("Visualizar Todos los Paises")
    query = "SELECT * FROM Pais"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(
        filas,
        columns=["Id", "Nombre", "Codigo ISO", "Continente"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with añadir:
    st.title("Registro de Nuevo Pais")
    nombre = st.text_input("Nombre: *", key="pais_nombre")
    codigo_iso = st.text_input("Codigo ISO: *", key="pais_codigo_iso")
    continente = st.text_input("Continente: (opcional)", key="pais_continente")

    if st.button("Enviar", key="btn_pais"):
        errores = []
        try:
            v1.validar_nombre(nombre, "nombre")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(codigo_iso, "codigo ISO")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(continente, "continente", obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                c1.insertar_datos(
                    "INSERT INTO Pais (nombre, codigo_iso, continente) VALUES (?, ?, ?)",
                    nombre.strip(),
                    codigo_iso.strip().upper(),
                    continente.strip() or None,
                )
                st.success("País registrado correctamente.")
            except ValueError as e:
                st.error(str(e))
