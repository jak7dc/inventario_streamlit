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

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 1, 3, 1, 3, 2, 2, 3])
    with col1:
        st.write("ID")
    with col2:
        st.write("Referencia")
    with col3:
        st.write("Nombre")
    with col5:
        st.write("Categoria")
    with col6:
        st.write("Unidades")
    with col7:
        st.write("Peso")
    with col8:
        st.write("Acciones")

    for index, row in df.iterrows():
        with col1:
            st.write(row['ID']) 
        with col2:
            st.write(row['Referencia'])
        with col3:
            st.write(row['Nombre'])
        with col5:
            st.write(row['Categoria'])
        with col6:
            st.write(row['Unidades'])
        with col7:
            st.write(row['Peso'])
        with col8:
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
        nombre = st.text_input("Nombre del Producto")
        categoria = st.number_input("Categoria", min_value=0, step=1)
        unMedida = st.selectbox("Unidad de Medida", ["kilogramo", "gramo", "litro", "mili litro", "galón", "cuñete" , "unidad"])
        
        
        if st.form_submit_button("Guardar Producto"):
            st.success(f"Producto '{nombre}'guardado exitosamente.")
            st.session_state.pagina_productos = "Productos"
        