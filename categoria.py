import streamlit as st
from conexion import Conexion
import pandas as pd

def categoria_main():
    st.title("Categorías")
    col0, col1, col2, col3 = st.columns(4)
    
    with col0:
        if st.button("Ver Categorías"):
            st.session_state.pagina_categorias = "Ver"
    
    with col1:
        if st.button("insertar categoria"):
            st.session_state.pagina_categorias = "Insertar"

    
    paginacion()  # Llamar a la función de paginación para actualizar la vista

def paginacion():
    if 'pagina_categorias' not in st.session_state:
        st.session_state.pagina_categorias = "Ver"  # Página por defecto
    
    if st.session_state.pagina_categorias == "Insertar":
        insertar_categoria()  
    elif st.session_state.pagina_categorias == "Editar":
        editar_categoria()
    elif st.session_state.pagina_categorias == "Eliminar":
        st.write("Formulario para eliminar categorias...")
    elif st.session_state.pagina_categorias == "Ver":
        ver_categorias()

def editar_categoria():
    with st.form("editar_categoria_form"):
        st.write("Formulario para editar categoria...")
        id_categoria = st.text_input("ID de la categoria", value=st.session_state.get('categoria_id', ''), disabled=True)
        nombre_categoria = st.text_input("Nombre de la categoria", value=st.session_state.get('categoria_nombre', ''))
        descripcion_categoria = st.text_area("Descripcion de la categoria", value=st.session_state.get('categoria_descripcion', ''))
        if st.form_submit_button("Guardar Cambios"):
            conn = Conexion()
            conn.cursor.execute(
                "UPDATE categoria SET nombre_categoria = %s, descripcion_categoria = %s WHERE id_categoria = %s",
                (nombre_categoria, descripcion_categoria, st.session_state.get('categoria_id'))
            )
            conn.conexion.commit()
            conn.cerrar()
            st.success(f"Categoria '{nombre_categoria}' actualizada exitosamente.")
            st.session_state.pagina_categorias = "Ver"

def insertar_categoria():
    with st.form("insertar_categoria_form"):
        st.write("Formulario para insertar categoria...")
        nombre_producto = st.text_input("Nombre de la categoria")
        precio_producto = st.text_area("Descripcion de la categoria")
        
        if st.form_submit_button("Guardar Categoria"):
            conn = Conexion()
            conn.cursor.execute(
                "INSERT INTO categoria (nombre_categoria, descripcion_categoria) VALUES (%s, %s)",
                (nombre_producto, precio_producto)
            )
            conn.conexion.commit()
            conn.cerrar()
            st.success(f"Producto '{nombre_producto}' con precio {precio_producto} guardado exitosamente.")
            st.session_state.pagina_categorias = "Ver"
        
def ver_categorias():
    conn = Conexion()
    conn.cursor.execute("SELECT * FROM categoria;")
    data = conn.cursor.fetchall()
    conn.cerrar()
    df_categorias = pd.DataFrame(data, columns=['ID', 'Nombre de la Categoria', 'Descripcion de la Categoria'])
    df_categorias = df_categorias.sort_values(by='ID', ascending=True)

    for i, row in df_categorias.iterrows():
        col1, col2, col3, col4 = st.columns([1, 6, 6, 5])
        col1.write(row['ID'])
        col2.write(row['Nombre de la Categoria'])
        col3.write(row['Descripcion de la Categoria'])

        with col4:
            sub_col1, sub_col2 = st.columns(2)
            if sub_col1.button("Editar", key=f"btn_{i}"):
                st.session_state.pagina_categorias = "Editar"
                st.session_state.categoria_id = row['ID']
                st.session_state.categoria_nombre = row['Nombre de la Categoria']
                st.session_state.categoria_descripcion = row['Descripcion de la Categoria']
                st.rerun()
            if sub_col2.button("Eliminar", key=f"btn_del_{i}"):
                conn = Conexion()
                conn.cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", (row['ID'],))
                conn.conexion.commit()
                conn.cerrar()
                st.session_state.pagina_categorias = "Ver"
                st.rerun()