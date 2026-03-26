import streamlit as st
from conexion import Conexion

conector = (
    "DRIVER={SQL Server};"
    "SERVER=LAPTOP-ADRIAN\\SQLEXPRESS;"
    "DATABASE=almacenamiento;"
    "Trusted_Connection=yes;"
)
c1 = Conexion(conector=conector)

st.set_page_config(page_title="Mi Sitio")

st.title("Inicio")
st.write("Bienvenido a mi sitio web.")
st.info("Usa el menú de la izquierda para navegar.")
