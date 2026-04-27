import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3
import random

st.set_page_config(page_title="EstuMind", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #e0f7fa 0%, #a5e1e8 100%);}
    h1, h2, h3 {color: #0f5c4d;}
    .stButton>button {background-color: #00b894; color: white; border-radius: 20px; padding: 14px 32px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 EstuMind")
st.subheader("Espacio de bienestar mental para estudiantes")

# Logo centrado y mediano
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo2.png", width=450)

def init_db():
    conn = sqlite3.connect('estumind.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS humor (id INTEGER PRIMARY KEY, username TEXT, fecha TEXT, emoji TEXT, puntaje INTEGER, nota TEXT, factor TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS diario (id INTEGER PRIMARY KEY, username TEXT, fecha TEXT, entrada TEXT)''')
    conn.commit()
    conn.close()

init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
    st.subheader("🔑 Bienvenido a tu espacio seguro")
    tab1, tab2 = st.tabs(["Iniciar sesión", "Crear cuenta"])
    with tab1:
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Entrar", type="primary"):
            conn = sqlite3.connect('estumind.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
            if c.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
            conn.close()
    with tab2:
        new_user = st.text_input("Usuario nuevo")
        new_pw = st.text_input("Contraseña nueva", type="password")
        if st.button("Registrarse", type="primary"):
            conn = sqlite3.connect('estumind.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pw))
                conn.commit()
                st.success("¡Cuenta creada!")
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.rerun()
            except:
                st.error("Ese usuario ya existe")
            conn.close()

else:
    username = st.session_state.username
    st.sidebar.success(f"✅ {username} | Conectado")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.selectbox("Menú Principal", 
        ["🏠 Dashboard", "📊 Registrar Estado", "🤖 Chatbot Especializado", 
         "🧪 Test de Salud Mental", "📖 Mi Diario", "✅ Hábitos Diarios", 
         "🧘 Ejercicios Guiados", "📈 Mi Progreso", "🛠 Recursos"])

    if menu == "🏠 Dashboard":
        st.markdown(f"# ¡Hola, {username}! 👋")
        col1, col2, col3, col4 = st.columns(4)
        conn = sqlite3.connect('estumind.db')
        df = pd.read_sql("SELECT puntaje FROM humor WHERE username=?", conn, params=(username,))
        conn.close()
        if not df.empty:
            avg = round(df['puntaje'].mean(), 1)
            with col1: st.metric("Ánimo promedio", f"{avg}/5")
            with col2: st.metric("Días registrados", len(df))
            with col3: st.metric("Racha actual", "14 días")
            with col4: st.metric("Ejercicios hechos", "28")
        else:
            st.warning("Aún no tienes datos. ¡Empieza hoy!")

    elif menu == "📊 Registrar Estado":
        st.subheader("¿Cómo te sientes hoy?")
        emojis = {"😭 Muy mal":1, "😟 Mal":2, "😐 Regular":3, "🙂 Bien":4, "😃 Excelente":5}
        emoji_sel = st.selectbox("Estado actual", list(emojis.keys()))
        puntaje = emojis[emoji_sel]
        factores = st.multiselect("¿Qué te afecta?", ["Exámenes","Sueño","Ansiedad","Carga académica","Familia","Motivación","Procrastinación","Otro"])
        nota = st.text_area("Nota adicional")
        if st.button("💾 Guardar estado", type="primary"):
            conn = sqlite3.connect('estumind.db')
            c = conn.cursor()
            c.execute("INSERT INTO humor VALUES (NULL,?,?,?,?,?,?)", 
                      (username, datetime.now().strftime("%Y-%m-%d %H:%M"), emoji_sel, puntaje, nota, ", ".join(factores)))
            conn.commit()
            conn.close()
            st.success("✅ Guardado correctamente")

    elif menu == "🤖 Chatbot Especializado":
        st.subheader("🤖 EstuMind - Tu asistente de salud mental")

        groq_api_key = st.sidebar.text_input("🔑 Groq API Key", type="password", 
                                             value="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")

        if not groq_api_key:
            st.warning("Ingresa tu Groq API Key")
            st.stop()

        from groq import Groq
        client = Groq(api_key=groq_api_key)

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        def obtener_respuesta_ia(mensaje):
            try:
                system_prompt = "Eres EstuMind, compañero empático de salud mental para estudiantes nicaragüenses. Responde en español con calidez y consejos prácticos. En crisis redirige al 118 y CAPS del MINSA."
                messages = [{"role": "system", "content": system_prompt}]
                for rol, texto in st.session_state.chat_history[-6:]:
                    messages.append({"role": "user" if rol == "Tú" else "assistant", "content": texto})
                messages.append({"role": "user", "content": mensaje})

                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=600
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                return f"Error: {str(e)}"

        for rol, texto in st.session_state.chat_history:
            with st.chat_message("user" if rol == "Tú" else "assistant", avatar="🧠" if rol == "EstuMind" else None):
                st.write(texto)

        prompt = st.chat_input("Escribe cómo te sientes o tu consulta...")

        if prompt:
            st.session_state.chat_history.append(("Tú", prompt))
            with st.chat_message("user"):
                st.write(prompt)
            respuesta = obtener_respuesta_ia(prompt)
            st.session_state.chat_history.append(("EstuMind", respuesta))
            with st.chat_message("assistant", avatar="🧠"):
                st.write(respuesta)

        if st.button("🗑️ Limpiar conversación"):
            st.session_state.chat_history = []
            st.rerun()

    elif menu == "🧪 Test de Salud Mental":
        st.subheader("🧪 Test de Bienestar Mental")
        st.write("Responde con sinceridad.")
        preguntas = ["Sientes que te preocupas demasiado por los exámenes o el futuro?","Te cuesta concentrarte cuando estás estudiando?","Te sientes cansado/a incluso después de dormir?","Has perdido interés en actividades que antes te gustaban?","Te sientes abrumado/a por la cantidad de tareas?","Tienes problemas para dormir o te despiertas muy temprano?","Te comparas constantemente con otros estudiantes?","Sientes que no tienes tiempo para ti mismo/a?","Te sientes solo/a aunque estés rodeado de gente?","Has tenido cambios en tu apetito?"]
        respuestas = []
        for i, p in enumerate(preguntas):
            st.write(f"**{i+1}. {p}**")
            r = st.radio("Elige:", ["Sí", "No", "Tal vez"], key=f"q{i}")
            respuestas.append(r)
        if st.button("Calcular resultado", type="primary"):
            score = sum(2 if r=="Sí" else 1 if r=="Tal vez" else 0 for r in respuestas)
            if score >= 15: st.success("**Nivel ALTO** - Posible ansiedad o burnout")
            elif score >= 9: st.warning("**Nivel MODERADO**")
            else: st.success("**Nivel BAJO** - Estás bien")

    elif menu == "📖 Mi Diario":
        st.subheader("📖 Mi Diario Personal")
        entrada = st.text_area("¿Qué pasó hoy?", height=200)
        if st.button("Guardar"):
            conn = sqlite3.connect('estumind.db')
            c = conn.cursor()
            c.execute("INSERT INTO diario VALUES (NULL, ?, ?, ?)", (username, datetime.now().strftime("%Y-%m-%d %H:%M"), entrada))
            conn.commit()
            conn.close()
            st.success("Guardado")

    elif menu == "✅ Hábitos Diarios":
        st.subheader("✅ Hábitos")
        for hab in ["Beber 2 litros de agua", "Dormir mínimo 7 horas", "Hacer ejercicio 20 minutos", "Meditar 5 minutos"]:
            if st.checkbox(hab): st.success(f"✅ {hab}")

    elif menu == "🧘 Ejercicios Guiados":
        st.subheader("🧘 Ejercicios")
        ejercicio = st.selectbox("Elige", ["Respiración 4-7-8", "Grounding 5-4-3-2-1", "Lista de Gratitud"])
        if ejercicio == "Respiración 4-7-8": st.write("Inhala 4s → Retén 7s → Exhala 8s")
        elif ejercicio == "Grounding 5-4-3-2-1": st.write("5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles, 1 que saboreas")
        else: st.write("Escribe 5 cosas por las que estás agradecido")

    elif menu == "📈 Mi Progreso":
        st.subheader("Tu evolución")
        conn = sqlite3.connect('estumind.db')
        df = pd.read_sql("SELECT fecha, puntaje FROM humor WHERE username=? ORDER BY fecha", conn, params=(username,))
        conn.close()
        if not df.empty:
            df['fecha'] = pd.to_datetime(df['fecha'])
            st.plotly_chart(px.line(df, x='fecha', y='puntaje', markers=True), use_container_width=True)

    elif menu == "🛠 Recursos":
        st.subheader("🛠 Recursos Nicaragua")
        st.markdown("""
        **🚨 118** → Emergencias Nacionales  
        **🏥 CAPS MINSA** → Gratuitos en todo el país  
        **Managua**: Hospital Psicosocial Dr. Jacobo Marcos Frech (km 12.5 carretera vieja a León
        **Juigalpa-Chontales**: Hospital "Camilo Ortega" 
                     Hospital Clínica Médica Previsional (CMP) "Pablo Úbeda")
        """)

    st.sidebar.caption("EstuMind v1.0 - Feria Universitaria | SIS-1M1-J")
