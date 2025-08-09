import streamlit as st
import inicio, productos, categoria

def main():
    st.sidebar.title("Navegación")
    pagina = st.sidebar.radio("Ir a", ("Inicio", "Productos", "Categorías"))


    st.session_state.pagina = pagina  # Guardar la página seleccionada en el estado de sesión
    paginacion()
    

def paginacion():
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "Inicio"  # Página por defecto
        
    if st.session_state.pagina == "Inicio":
        inicio.inicio_main()
    elif st.session_state.pagina == "Productos":
        productos.productos_main()
    elif st.session_state.pagina == "Categorías":
        categoria.categoria_main()


if __name__ == "__main__":
    main()
