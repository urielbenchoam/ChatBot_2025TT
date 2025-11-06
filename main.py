#LIBRERIAS
import streamlit as st
import groq

#VARIABLES
altura_contenedor_chat = 600
stream_status = True

#CONSTANTES
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-4-12b"]

#FUNCIONES

#ESTA FUNCIÓN UTILIZA STREAMLIT PARA CREAR LA INTERFAZ DE LA PÁGINA Y ADEMÁS RETORNA El
#MODELO ELEGIDO POR EL USUARIO
def configurar_pagina():

    st.set_page_config(page_title="El gigachad digo chat de Bencho", page_icon= "😎")

    st.title("El gigachad digo chat de Bencho")

    st.sidebar.title("Seleccion de modelos")

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo

#ESTA FUNCION LLAMA A st.secrets PARA OBTENER LA CLAVE DE LA API DE GROQ Y CREA UN USUARIO
def crear_usuario():    
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)

#CONFIGURA EL MODELO DE LENGUAJE PARA QUE PROCESE EL PROMPT DEL USUARIO
def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model = modelo_elegido,
        messages = [{"role" : "user", "content" : prompt_usuario}],
        stream = stream_status
    )

#CREAMOS UNA SESION LLAMADA "mensajes" QUE VA A GUARDAR LO QUE LE ESCRIBIMOS AL CHATBOT
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_completa_del_bot):
    _respuesta_posta = ""
    for frase in respuesta_completa_del_bot:
        if frase.choices[0].delta.content:
            _respuesta_posta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return _respuesta_posta

#---------------------------IMPLEMENTACION-------------------------------------

def main():
    modelo_elegido_por_el_usuario = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()

    area_chat()

    promt_del_usuario = st.chat_input("Escribí tu prompt: ")

    if promt_del_usuario:
        actualizar_historial("user", promt_del_usuario, "😠")
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido_por_el_usuario, promt_del_usuario)
        
        if respuesta_del_bot:
            with st.chat_message("assistant"):
                respuesta_posta = st.write_stream(generar_respuesta(respuesta_del_bot))
                actualizar_historial("assistant", respuesta_posta, "😎")

                st.rerun()


if __name__ == "__main__":
    main()

