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

mostrar, añadir = st.tabs(["Visualizar Clasificacion", "Añadir Nueva Clasificación"])

with mostrar:
    st.title("Visualizar Todas las Clasificaciones")
    query = "SELECT * FROM Clasificacion"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(
        filas,
        columns=["ID", "Nombre", "Descripción", "Edad Minima"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with añadir:
    st.title("Registro de Nueva Clasificacion")
    nombre = st.text_input("Nombre: *", key="clas_nombre")
    descripcion = st.text_input("Descripcion: (opcional)", key="clas_descripcion")
    edad_minima = st.text_input("Edad minima: (opcional)", key="clas_edad_minima")

    if st.button("Enviar", key="btn_clasificacion"):
        errores = []

        try:
            v1.validar_nombre(nombre, "Nombre", tipo="pelicula")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(descripcion, "Descripcion", obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_edad(edad_minima, obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                c1.insertar_datos(
                    "INSERT INTO Clasificacion (nombre, descripcion, edad_minima) VALUES (?, ?, ?)",
                    nombre.strip(),
                    descripcion.strip() or None,
                    int(edad_minima.strip()) if edad_minima.strip() else None,
                )
                st.success("Clasificación registrada correctamente.")
            except ValueError as e:
                st.error(str(e))
