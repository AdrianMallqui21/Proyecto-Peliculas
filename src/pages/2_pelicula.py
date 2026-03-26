import streamlit as st
from validaciones import Validaciones
from conexion import Conexion
import pandas as pd
from datetime import date
from datetime import datetime

conector = (
    "DRIVER={SQL Server};"
    "SERVER=LAPTOP-ADRIAN\\SQLEXPRESS;"
    "DATABASE=almacenamiento;"
    "Trusted_Connection=yes;"
)
c1 = Conexion(conector=conector)
v1 = Validaciones()

temporadas = None
duracion_minutos = None

tipos = v1.extraer_listas("Tipo")
clasificaciones = v1.extraer_listas("Clasificacion")
generos = v1.extraer_listas("Genero")
paises = v1.extraer_listas("Pais")

mostrar, añadir = st.tabs(["Visualizar Pelicula", "Añadir Nueva Pelicula"])

with mostrar:
    st.title("Visualizar Todas las Pelicula")
    query = "SELECT * FROM Pelicula"
    filas = c1.ejecutar_consulta(query=query)
    df = pd.DataFrame(
        filas,
        columns=[
            "ID",
            "Título",
            "Fecha Subida",
            "Año Lanzamiento",
            "Duración (min)",
            "Temporadas",
            "Descripción",
            "ID Clasificación",
            "ID Tipo",
            "ID País",
        ],
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

with añadir:
    st.title("Registro de Nueva Pelicula")
    titulo = st.text_input("Titulo: *", key="pel_titulo")
    descripcion = st.text_input("Descripcion: (opcional)", key="pel_descripcion")
    fecha_subida = st.text_input(
        "Fecha de subida: * (DD/MM/AAAA)", key="pel_fecha_subida"
    )
    año_lanzamiento = st.text_input("Año de lanzamiento: *", key="pel_año_lanzamiento")

    clasificacion_sel = st.selectbox(
        "Clasificación: *",
        list(clasificaciones.keys()),
        key="pel_clasificacion",
    )
    pais_sel = st.selectbox("País: *", list(paises.keys()), key="pel_pais")
    genero_sel = st.selectbox("Genero: *", list(generos.keys()), key="pel_genero")

    tipo_sel = st.selectbox("Tipo: *", list(tipos.keys()), key="pel_tipo")
    primer_tipo = list(tipos.keys())[0]

    if tipo_sel == primer_tipo:
        temporadas = st.text_input("Cantidad de temporadas: *", key="pel_temporadas")
    else:
        duracion_minutos = st.text_input("Duracion en minutos: *", key="pel_duracion")

    if st.button("Enviar", key="btn_pelicula"):
        errores = []

        try:
            v1.validar_nombre(valor=titulo, campo="Titulo", tipo="pelicula")
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_nombre(valor=descripcion, campo="Descripcion", obligatorio=False)
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_fecha(fecha=fecha_subida)
        except ValueError as e:
            errores.append(str(e))

        try:
            v1.validar_numero(
                valor=año_lanzamiento,
                campo="Año de Lanzamiento",
                minimo=1800,
                maximo=int(date.today().year),
            )
        except ValueError as e:
            errores.append(str(e))

        # FIX 2: solo validar el campo que corresponde según el tipo seleccionado
        if tipo_sel == primer_tipo:
            try:
                v1.validar_numero(valor=temporadas, campo="Temporadas", maximo=50)
            except ValueError as e:
                errores.append(str(e))
        else:
            try:
                v1.validar_numero(
                    valor=duracion_minutos, campo="Duracion", minimo=60, maximo=350
                )
            except ValueError as e:
                errores.append(str(e))

        # FIX 3: el else de inserción va aquí dentro, no en el else del botón
        if errores:
            for error in errores:
                st.error(error)
        else:
            try:
                id_tipo = tipos[tipo_sel]
                id_clasificacion = clasificaciones[clasificacion_sel]
                id_pais = paises[pais_sel]
                id_genero = generos[genero_sel]

                dur = (
                    int(duracion_minutos.strip())
                    if duracion_minutos and duracion_minutos.strip()
                    else None
                )
                temp = (
                    int(temporadas.strip())
                    if temporadas and temporadas.strip()
                    else None
                )
                año_int = int(año_lanzamiento.strip())

                c1.insertar_datos(
                    """INSERT INTO Pelicula
    (titulo, fecha_subida, año_lanzamiento,
     duracion_minutos, temporadas, descripcion,
     id_clasificacion, id_tipo, id_pais)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    titulo.strip(),
                    datetime.strptime(fecha_subida.strip(), "%d/%m/%Y").strftime(
                        "%Y-%m-%d"
                    ),
                    año_int,
                    dur,
                    temp,
                    descripcion.strip() or None,
                    id_clasificacion,
                    id_tipo,
                    id_pais,
                )

                id_pelicula = c1.ejecutar_consulta(
                    "SELECT TOP 1 id_pelicula FROM Pelicula ORDER BY id_pelicula DESC"
                )[0][0]

                c1.insertar_datos(
                    "INSERT INTO Pelicula_Genero (id_pelicula, id_genero) VALUES (?, ?)",
                    id_pelicula,
                    id_genero,
                )
                st.success("Película registrada correctamente.")
            except Exception as e:
                st.error(f"Error al registrar: {str(e)}")
