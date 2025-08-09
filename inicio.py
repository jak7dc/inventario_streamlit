import streamlit as st
import app

def inicio_main():
    pagnacion()  
    
def pagnacion():
    if 'pagina_inicio' not in st.session_state:
        st.session_state.pagina_inicio = "Inicio"

    if st.session_state.pagina_inicio == "Inicio":
        main_inicio()
    elif st.session_state.pagina_inicio == "Productos":
        ir_productos()

def main_inicio():
    st.title("Inicio de la Aplicación")
    st.write("Esta es la página de inicio de la aplicación Streamlit.")
    if st.button("ir a Productos"):
        st.session_state.pagina_inicio = "Productos"
        st.rerun()  

def ir_productos():
    st.session_state.pagina_inicio = "Inicio"
    st.session_state.pagina = "Productos"
    app.paginacion()  

    

        
        