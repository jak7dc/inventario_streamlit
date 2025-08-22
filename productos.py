import streamlit as st
import pandas as pd
from conexion import Conexion
import numpy as np

def productos_main():
    st.markdown("""
    <style>     
    .stMainBlockContainer {      
            max-width: 90%;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Productos")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Ver Productos"):
            st.session_state.pagina_productos = "Ver"
        
    with col2:    
        if st.button("Insertar Productos"):
            st.session_state.pagina_productos = "Insertar"

    paginacion()  # Llamar a la función de paginación para actualizar la vista

def paginacion():
    if 'pagina_productos' not in st.session_state:
        st.session_state.pagina_productos = "Ver"  # Página por defecto
    
    if st.session_state.pagina_productos == "Ver":
        ver_productos()
    elif st.session_state.pagina_productos == "Insertar":
        insertar_producto()
    elif st.session_state.pagina_productos == "Editar":
        editar_productos()

def ver_productos():
    conn = Conexion()
    conn.cursor.execute("""
        SELECT producto.id_producto, producto.referencia_producto, producto.nombre_producto, 
		producto.id_categoria, categoria.nombre_categoria,
		producto.unidades_producto, producto.unmedida_producto, producto.peso_producto
		FROM producto join categoria
		on producto.id_categoria = categoria.id_categoria
                        """)
    data = conn.cursor.fetchall()
    conn.cerrar()

    df = pd.DataFrame(data, columns=['ID', 'Referencia', 'Nombre','Id categoria', 'Categoria', 'Unidades', 'Unidad Medida', 'Peso'])
    df = df.sort_values(by='ID', ascending=True)

    hd1, hd2, hd3, hd4, hd5, hd6, hd7, hd8 = st.columns([1, 1, 3, 3, 2, 2, 2, 3])

    with hd1:
        st.write("Id")
    with hd2:
        st.write("Referencia")
    with hd3:
        st.write("Nombre")
    with hd4:
        st.write("Categoria")
    with hd5:
        st.write("Unidades")
    with hd6:
        st.write("und/Medida")
    with hd7:
        st.write("Peso")
    with hd8:
        st.write("Acciones")

    for index, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 1, 3, 3, 2, 2, 2, 3])
        
        with col1:
            st.write(row['ID']) 
        with col2:
            st.write(row['Referencia'])
        with col3:
            st.write(row['Nombre'])
        with col4:
            st.write(row['Categoria'])
        with col5:
            st.write(row['Unidades'])
        with col6:
            st.write(row['Unidad Medida'])
        with col7:
            st.write(row['Peso'])
        with col8:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                if st.button("Editar", key=f"editar_{row['ID']}"):
                    st.session_state.pagina_productos = "Editar"
                    st.session_state.productos_id = row['ID']
                    st.session_state.productos_nombre = row['Nombre']
                    st.session_state.productos_unMedida = row['Unidad Medida']
                    st.session_state.productos_id_categoria = row['Categoria']
                    st.rerun()
            with subcol2:
                if st.button("Eliminar", key=f"eliminar_{row['ID']}"):
                    eliminar_producto(row['ID'])
                    st.session_state.pagina_productos = "Ver"
                    st.rerun()
        
def insertar_producto():
    conn = Conexion()
    conn.cursor.execute("""
        select categoria.id_categoria ,categoria.nombre_categoria from categoria                
    """)
    categorias = conn.cursor.fetchall()
    conn.cerrar()
    df_categorias = pd.DataFrame(categorias, columns=['id', 'NombreCat'])
    df_categorias_array = df_categorias['NombreCat'].to_numpy() 
    with st.form("insertar_producto_form"):
        st.write("Formulario para insertar productos...")
        nombre_producto = st.text_input("Nombre del Producto")
        categoria = st.selectbox("Categoria", df_categorias_array)
        unMedida_producto = st.selectbox("Unidad de Medida", ["kilogramo", "gramo", "litro", "mili litro", "galón", "cuñete" , "unidad"])
        
        
        if st.form_submit_button("Guardar Producto"):
            id_categoria = df_categorias[df_categorias['NombreCat'] == categoria]['id'].values[0]

            conn.conectar()
            conn.cursor.execute(
                """
            INSERT INTO producto (id_producto, referencia_producto, nombre_producto, unidades_producto, 
					            peso_producto, unmedida_producto, id_categoria)
			            values(
			                    (select (coalesce(max(id_producto)) + 1) from producto)	
			                    ,'PR' || CAST((select (coalesce(max(id_producto)) + 1) from producto) as text),
			                    %s, 0, 0, %s, %s)
                """,(nombre_producto, unMedida_producto, int(id_categoria))
            )
            conn.conexion.commit()
            conn.cerrar()
            st.success(f"Producto '{nombre_producto}'guardado exitosamente.")
            st.session_state.pagina_productos = "Ver"
            st.rerun()
        
def editar_productos():
    conn = Conexion()
    conn.cursor.execute("""
        select categoria.id_categoria ,categoria.nombre_categoria from categoria                
    """)
    categorias = conn.cursor.fetchall()
    conn.cerrar()
    df_categorias = pd.DataFrame(categorias, columns=['id', 'NombreCat'])
    # st.write(df_categorias)
    df_categorias_array = df_categorias['NombreCat'].to_numpy()

    with st.form("Editar productos fomulario"):
        id_producto = st.text_input('ID producto', value=st.session_state.productos_id ,disabled=True)
        nombre_producto = st.text_input('Nombre producto', value=st.session_state.productos_nombre)
        unMedida_producto = st.selectbox('unidad de medida', ["kilogramo", "gramo", "litro", "mili litro", "galón", "cuñete" , "unidad"])
        id_categoria = df_categorias[df_categorias['NombreCat'] == st.session_state.productos_id_categoria]['id'].values[0]
        categoria = st.selectbox('categoria', df_categorias_array, index=(int(id_categoria) - 1))

        if st.form_submit_button("Editar producto"):
            id_categoria = df_categorias[df_categorias["NombreCat"] == categoria]['id'].values[0]
            conn.conectar()
            conn.cursor.execute(
                """
                    UPDATE producto SET nombre_producto = %s, unmedida_producto = %s, id_categoria = %s
                    WHERE id_producto = %s
                """,(nombre_producto, unMedida_producto, int(id_categoria), id_producto)
            )
            conn.conexion.commit()
            conn.cerrar()
            st.success(f'{nombre_producto} editado exitosamente.')
            st.session_state.pagina_productos = "Ver"
            st.rerun()

def eliminar_producto(id_producto):
    conn = Conexion()
    conn.conectar()
    conn.cursor.execute(
        """
        DELETE FROM producto WHERE id_producto = %s
        """, (id_producto,)
    )
    conn.conexion.commit()
    conn.cerrar()
    st.success(f"Producto con ID {id_producto} eliminado exitosamente.")
    st.session_state.pagina_productos = "Ver"
    st.rerun()