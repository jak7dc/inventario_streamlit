import streamlit as st
import pandas as pd
from conexion import Conexion


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

    df = pd.DataFrame(data, columns=['ID', 'Referencia', 'Nombre','Id categoria', 'Categoria', 'Unidades', 'Peso', 'Unidad Medida'])

    hd1, hd2, hd3, hd4, hd5, hd6 ,hd7 = st.columns([1, 1, 3, 3, 2, 2, 3])

    with hd1:
        st.write("ID")
    with hd2:
        st.write("Referencia")
    with hd3:
        st.write("Nombre")
    with hd4:
        st.write("Categoria")
    with hd5:
        st.write("Unidades")
    with hd6:
        st.write("Peso")
    with hd7:
        st.write("Acciones")

    for index, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 3, 3, 2, 2, 3])
        
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
            st.write(row['Peso'])
        with col7:
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                if st.button("Editar", key=f"editar_{row['ID']}"):
                    st.success(f"Producto {row['Nombre']} editado exitosamente.")
            with subcol2:
                if st.button("Eliminar", key=f"eliminar_{row['ID']}"):
                    st.success(f"Producto {row['Nombre']} eliminado exitosamente.")
        
    

def insertar_producto():
    with st.form("insertar_producto_form"):
        st.write("Formulario para insertar productos...")
        nombre_producto = st.text_input("Nombre del Producto")
        id_categoria = st.number_input("Categoria", min_value=0, step=1)
        unMedida_producto = st.selectbox("Unidad de Medida", ["kilogramo", "gramo", "litro", "mili litro", "galón", "cuñete" , "unidad"])
        
        
        if st.form_submit_button("Guardar Producto"):
            conn = Conexion()
            conn.cursor.execute(
                """
            INSERT INTO producto (id_producto, referencia_producto, nombre_producto, unidades_producto, 
					            peso_producto, unmedida_producto, id_categoria)
			            values(
			                    (select (coalesce(max(id_producto)) + 1) from producto)	
			                    ,'PR' || CAST((select (coalesce(max(id_producto)) + 1) from producto) as text),
			                    %s, 0, 0, %s, %s)
                """,(nombre_producto, unMedida_producto, id_categoria)
            )
            conn.conexion.commit()
            conn.cerrar()
            st.success(f"Producto '{nombre_producto}'guardado exitosamente.")
            st.session_state.pagina_productos = "Productos"
        