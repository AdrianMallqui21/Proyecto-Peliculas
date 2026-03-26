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

mostrar, añadir = st.tabs(["Visualizar Tipo", "Añadir Nuevo Tipo"])

with mostrar:
    st.title("Visualizar Todos los Tipos")
    query = "SELECT * FROM Tipo"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(
        filas,
        columns=["ID", "Nombre", "Descripción"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with añadir:
    st.title("Registro de Nuevo Tipo")
    nombre = st.text_input("Nombre: *", key="tipo_nombre")
    descripcion = st.text_input("Descripcion: (opcional)", key="tipo_descripcion")

    if st.button("Enviar", key="btn_tipo"):
        errores = []

        try:
            v1.validar_nombre(nombre, "nombre")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(descripcion, "descripcion", obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                c1.insertar_datos(
                    "INSERT INTO Tipo (nombre, descripcion) VALUES (?, ?)",
                    nombre.strip(),
                    descripcion.strip() or None,
                )
                st.success("Tipo registrado correctamente.")
            except ValueError as e:
                st.error(str(e))
