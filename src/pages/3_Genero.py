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

mostrar, añadir = st.tabs(["Visualizar Genero", "Añadir Nuevo Genero"])

## ESTO SE DEBE MODIFICAR PARA MOSTRAR CORRECTAMENTE EN DF LO DE LA BD
with mostrar:
    st.title("Visualizar Todas las Categoria")
    query = "SELECT * FROM Genero"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(filas, columns=["ID", "Nombre", "Descripción"])
    st.dataframe(df, use_container_width=True, hide_index=True)


with añadir:
    st.title("Registro de Nueva Categoria")
    nombre = st.text_input("Nombre: *", key="cat_nombre")
    descripcion = st.text_input("Descripcion: (opcional)", key="cat_descripcion")

    if st.button("Enviar", key="btn_categoria"):
        errores = []
        try:
            v1.validar_nombre(valor=nombre, campo="Nombre"),
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(valor=descripcion, campo="Descripción", obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                c1.insertar_datos(
                    "INSERT INTO Genero (nombre, descripcion) VALUES (?, ?)",
                    nombre.strip(),
                    descripcion.strip() or None,
                )
                st.success("Categoría registrada correctamente.")
            except (ValueError, TypeError) as e:
                st.error(str(e))
