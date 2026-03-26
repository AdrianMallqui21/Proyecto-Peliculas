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

mostrar, añadir = st.tabs(["Visualizar Director", "Añadir Nuevo Director"])

with mostrar:
    st.title("Visualizar Todos los Directores")
    query = "SELECT * FROM Director"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(
        filas,
        columns=["ID", "Nombre", "Apellido", "Segundo Nombre", "Segundo Apellido"],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with añadir:
    st.title("Registro de Nuevo Director")
    nombre_completo = st.text_input("Nombre: *", key="dir_nombre")
    apellido_completo = st.text_input("Apellido: *", key="dir_apellido")

    if st.button("Enviar", key="btn_director"):
        errores = []

        try:
            v1.validar_nombre(nombre_completo, "nombre")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(apellido_completo, "apellido")
        except ValueError as e:
            errores.append(str(e))

        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                p_nombre, s_nombre = v1.parsear_nombre(nombre_completo)
                p_apellido, s_apellido = v1.parsear_nombre(apellido_completo)
                c1.insertar_datos(
                    "INSERT INTO Director (nombre, segundo_nombre, apellido, segundo_apellido) VALUES (?, ?, ?, ?)",
                    p_nombre,
                    s_nombre,
                    p_apellido,
                    s_apellido,
                )
                st.success("Director registrado correctamente.")
            except ValueError as e:
                st.error(str(e))
