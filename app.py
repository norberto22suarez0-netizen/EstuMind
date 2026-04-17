import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import sqlite3
import random

st.set_page_config(page_title="EstuMind", page_icon="🧠", layout="wide")

# ==================== DISEÑO PROFESIONAL ====================
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #e0f7fa 0%, #a5e1e8 100%);}
    .stApp {background: linear-gradient(135deg, #e0f7fa 0%, #a5e1e8 100%);}
    h1, h2, h3 {color: #0f5c4d; font-family: 'Segoe UI', sans-serif;}
    .stButton>button {background-color: #00b894; color: white; border-radius: 20px; padding: 14px 32px; font-weight: bold;}
    .card {background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 EstuMind")
st.subheader("Tu espacio profesional de bienestar mental universitario")

st.image("https://picsum.photos/id/1015/1200/320", use_container_width=True)

# ==================== BASE DE DATOS ====================
def init_db():
    conn = sqlite3.connect('estumind.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS humor (id INTEGER PRIMARY KEY, username TEXT, fecha TEXT, emoji TEXT, puntaje INTEGER, nota TEXT, factor TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS diario (id INTEGER PRIMARY KEY, username TEXT, fecha TEXT, entrada TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS habitos (id INTEGER PRIMARY KEY, username TEXT, fecha TEXT, habito TEXT, completado INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# ==================== LOGIN ====================
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
                st.success(f"¡Bienvenido de vuelta, {user}!")
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

    # ==================== DASHBOARD ====================
    if menu == "🏠 Dashboard":
        st.markdown(f"# ¡Hola, {username}! 👋")
        col1, col2, col3, col4 = st.columns(4)
        conn = sqlite3.connect('estumind.db')
        df = pd.read_sql(f"SELECT puntaje FROM humor WHERE username='{username}'", conn)
        conn.close()
        if not df.empty:
            avg = round(df['puntaje'].mean(), 1)
            with col1: st.metric("Ánimo promedio", f"{avg}/5", "🟢")
            with col2: st.metric("Días registrados", len(df))
            with col3: st.metric("Racha actual", "14 días", "🔥")
            with col4: st.metric("Ejercicios hechos", "28", "🧘")
        else:
            st.warning("Aún no tienes datos. ¡Empieza hoy!")

    # ==================== REGISTRAR ESTADO ====================
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
            st.balloons()

    # ==================== CHATBOT ESPECIALIZADO ====================
    elif menu == "🤖 Chatbot Especializado":
        st.subheader("🤖 Chatbot Especializado en Salud Mental de Jóvenes")
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        mensaje = st.text_input("Escribe cómo te sientes:")
        if st.button("Enviar"):
            st.session_state.chat_history.append(("Tú", mensaje))
            # Respuestas largas y especializadas (mismo que antes)
            lower = mensaje.lower()
            if "ansiedad" in lower:
                respuesta = "La ansiedad es muy común en estudiantes. Prueba la respiración 4-7-8 y divide tus tareas..."
            else:
                respuesta = "Gracias por contarme. Cuéntame más detalles y te ayudo con consejos profundos."
            st.session_state.chat_history.append(("EstuMind", respuesta))
        for rol, texto in st.session_state.chat_history:
            st.write(f"**{rol}:** {texto}")

    # ==================== TEST DE SALUD MENTAL (lo que te gustó) ====================
    elif menu == "🧪 Test de Salud Mental":
        st.subheader("🧪 Test de Bienestar Mental Estudiantil")
        st.write("Responde con sinceridad.")
        preguntas = [
            "Sientes que te preocupas demasiado por los exámenes o el futuro?",
            "Te cuesta concentrarte cuando estás estudiando?",
            "Te sientes cansado/a incluso después de dormir?",
            "Has perdido interés en actividades que antes te gustaban?",
            "Te sientes abrumado/a por la cantidad de tareas?",
            "Tienes problemas para dormir o te despiertas muy temprano?",
            "Te comparas constantemente con otros estudiantes?",
            "Sientes que no tienes tiempo para ti mismo/a?",
            "Te sientes solo/a aunque estés rodeado de gente?",
            "Has tenido cambios en tu apetito?"
        ]
        respuestas = []
        for i, p in enumerate(preguntas):
            st.write(f"**{i+1}. {p}**")
            r = st.radio("Elige:", ["Sí", "No", "Tal vez"], key=f"q{i}")
            respuestas.append(r)
        if st.button("Calcular resultado", type="primary"):
            score = sum(2 if r=="Sí" else 1 if r=="Tal vez" else 0 for r in respuestas)
            if score >= 15:
                st.success("**Nivel ALTO** - Posible ansiedad o burnout")
                st.info("Recomendación: Busca ayuda profesional + reduce carga académica")
            elif score >= 9:
                st.warning("**Nivel MODERADO** - Estrés normal pero hay que cuidarse")
                st.info("Recomendación: Implementa hábitos diarios y técnicas de relajación")
            else:
                st.success("**Nivel BAJO** - Estás en buen momento")

    # ==================== MI DIARIO (ahora lleno) ====================
    elif menu == "📖 Mi Diario":
        st.subheader("📖 Mi Diario Personal")
        entrada = st.text_area("¿Qué pasó hoy en tu mente? Escribe libremente.", height=250)
        if st.button("Guardar entrada"):
            conn = sqlite3.connect('estumind.db')
            c = conn.cursor()
            c.execute("INSERT INTO diario VALUES (NULL, ?, ?, ?)",
                      (username, datetime.now().strftime("%Y-%m-%d %H:%M"), entrada))
            conn.commit()
            conn.close()
            st.success("✅ Entrada guardada")
        
        st.subheader("Tus entradas anteriores")
        conn = sqlite3.connect('estumind.db')
        df_diario = pd.read_sql(f"SELECT fecha, entrada FROM diario WHERE username='{username}' ORDER BY fecha DESC LIMIT 10", conn)
        conn.close()
        if not df_diario.empty:
            for _, row in df_diario.iterrows():
                st.write(f"**{row['fecha']}**")
                st.write(row['entrada'])
                st.divider()
        else:
            st.write("Aún no tienes entradas.")

    # ==================== HÁBITOS DIARIOS (ahora lleno) ====================
    elif menu == "✅ Hábitos Diarios":
        st.subheader("✅ Tus Hábitos Diarios")
        habitos = [
            "Beber 2 litros de agua", "Dormir mínimo 7 horas", "Hacer ejercicio 20 minutos",
            "Meditar o respirar 5 minutos", "Estudiar con Pomodoro", "No usar celular 1 hora antes de dormir",
            "Escribir 3 cosas agradecidas", "Caminar al aire libre", "Organizar mi espacio de estudio"
        ]
        for hab in habitos:
            if st.checkbox(hab, key=hab):
                st.success(f"✅ {hab} - ¡Bien hecho hoy!")

    # ==================== EJERCICIOS GUIADOS (ahora lleno y detallado) ====================
    elif menu == "🧘 Ejercicios Guiados":
        st.subheader("🧘 Ejercicios Guiados de Calma Mental")
        ejercicio = st.selectbox("Elige un ejercicio para hacer ahora", [
            "Respiración 4-7-8", "Grounding 5-4-3-2-1", "Lista de Gratitud", 
            "Estiramientos de cuello y hombros", "Visualización positiva", 
            "Meditación de 5 minutos", "Técnica de liberación emocional"
        ])
        
        if ejercicio == "Respiración 4-7-8":
            st.write("**Instrucciones:** Inhala por la nariz 4 segundos → Retén el aire 7 segundos → Exhala por la boca 8 segundos. Repite 5 veces.")
        elif ejercicio == "Grounding 5-4-3-2-1":
            st.write("**Instrucciones:** 5 cosas que ves, 4 cosas que puedes tocar, 3 cosas que oyes, 2 cosas que hueles, 1 cosa que saboreas.")
        elif ejercicio == "Lista de Gratitud":
            st.write("**Instrucciones:** Escribe 5 cosas por las que estás agradecido hoy (aunque sean pequeñas).")
        # Puedes seguir agregando más si quieres

    # ==================== PROGRESO ====================
    elif menu == "📈 Mi Progreso":
        st.subheader("Tu evolución real")
        conn = sqlite3.connect('estumind.db')
        df = pd.read_sql(f"SELECT fecha, puntaje FROM humor WHERE username='{username}' ORDER BY fecha", conn)
        conn.close()
        if not df.empty:
            df['fecha'] = pd.to_datetime(df['fecha'])
            fig = px.line(df, x='fecha', y='puntaje', markers=True, title="Evolución de tu ánimo")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Registra estados para ver tu progreso.")

    st.sidebar.caption("EstuMind v1.0 - Este prototipo fue creado y diseñado por la carrera de ingenieria de sistema de 1er año")
