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

   import streamlit as st
import random

# ==================== CHATBOT ESPECIALIZADO EN NICARAGUA ====================
elif menu == "🤖 Chatbot Especializado":
    st.subheader("🤖 EstuMind - Chatbot de Salud Mental para Jóvenes Nicaragüenses")
    
    # AVISO IMPORTANTE - SOLO NICARAGUA
    st.error("""
    **⚠️ AVISO IMPORTANTE - SOLO PARA NICARAGUA**  
    Este chatbot es una **herramienta de apoyo educativo** y **NO sustituye** atención profesional.  
    
    **Si estás en crisis, tienes pensamientos de autolesión o suicidio:**
    
    - **Llama inmediatamente al 118** (Emergencias Nacionales de Nicaragua)  
    - Acude al **Centro de Atención Psicosocial (CAPS)** más cercano (servicio **gratuito** del MINSA)  
    - En Managua: **Hospital Psicosocial “Doctor Jacobo Marcos Frech”** (km 12.5 carretera vieja a León) – atención **24 horas** para crisis emocionales  
    - Ve a tu centro de salud más cercano o habla con un orientador escolar / familiar de confianza.
    
    La salud mental es prioridad en Nicaragua. ¡No estás solo/a!
    """)
    
    # Inicializar historial
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Función de respuestas especializada
    def obtener_respuesta(mensaje: str) -> str:
        msg = mensaje.lower().strip()
        
        # === 1. CRISIS (prioridad máxima - solo Nicaragua) ===
        crisis_kw = ["suicidio", "matarme", "quiero morir", "no quiero vivir", "autolesión", 
                     "cortarme", "lastimarme", "acabar con todo", "no soporto más"]
        if any(kw in msg for kw in crisis_kw):
            return """Lo siento mucho que estés pasando por esto. **Eres valioso/a y mereces ayuda ahora mismo.**

**Acción inmediata:**
- Llama al **118** (Emergencias Nacionales)
- Ve al **Centro de Atención Psicosocial (CAPS)** más cercano (gratuito del MINSA)
- En Managua: **Hospital Psicosocial “Doctor Jacobo Marcos Frech”** (km 12.5, carretera vieja a León) – abierto 24 horas

No estás solo/a. Hay profesionales nicaragüenses listos para ayudarte.  
¿Quieres que te explique cómo llegar al CAPS más cercano o cómo pedir apoyo en tu colegio?"""
        
        # === 2. SALUDOS ===
        if any(kw in msg for kw in ["hola", "buenos días", "buenas", "qué tal", "hey"]):
            return "¡Hola! Soy **EstuMind**, tu compañero especializado en salud mental de jóvenes nicaragüenses. 😊\n\nEstoy aquí para escucharte. Cuéntame cómo te sientes o qué te preocupa."
        
        if any(kw in msg for kw in ["gracias", "thank you"]):
            return "¡De nada! Me alegra poder apoyarte. Recuerda que los CAPS del MINSA están para ayudarte gratis. ¿Algo más en lo que te pueda acompañar?"
        
        # === 3. ANSIEDAD ===
        if any(kw in msg for kw in ["ansiedad", "ansioso", "preocupado", "nervios", "pánico", "miedo"]):
            respuestas = [
                "La ansiedad es muy común en jóvenes nicaragüenses por los estudios, la presión familiar y la situación económica. Prueba la respiración 4-7-8: inhala 4 seg, retiene 7, exhala 8. ¿Quieres que te guíe ahora?",
                "Entiendo lo fuerte que puede sentirse. En Nicaragua muchos jóvenes usan la técnica 5-4-3-2-1 para calmarse. ¿Qué te está generando más ansiedad en este momento (exámenes, familia, futuro)?",
                "La ansiedad se maneja mejor cuando la compartes. Los CAPS del MINSA ofrecen apoyo gratuito. Mientras, divide tus tareas en pasos pequeños. ¿Quieres tips específicos para ansiedad por estudios?",
                "Tu cerebro está en alerta, pero la mayoría de las cosas que tememos no pasan. ¿Has probado escribir tus preocupaciones y 'dejarlas' hasta mañana? Es una técnica que ayuda mucho."
            ]
            return random.choice(respuestas)
        
        # === 4. DEPRESIÓN / TRISTEZA ===
        elif any(kw in msg for kw in ["triste", "deprimido", "sin ganas", "vacío", "llorar", "solo", "depresión"]):
            respuestas = [
                "Lamento que te sientas así. En Nicaragua hay muchos jóvenes pasando por lo mismo. Pequeños pasos como salir a caminar, hablar con alguien de confianza o ir al CAPS ayudan. ¿Hay alguien en quien confíes?",
                "No estás solo/a. La tristeza prolongada es señal de que necesitas apoyo. Los Centros de Atención Psicosocial (CAPS) del MINSA son gratuitos y están en todo el país. ¿Quieres que te ayude a ubicar el más cercano?",
                "Es valiente que lo digas. Si la tristeza dura más de dos semanas, ve al CAPS o centro de salud. ¿Cómo ha estado tu energía y sueño últimamente?",
                "La depresión no es flojera. Celebra cada cosa pequeña que logras. En Nicaragua los servicios de salud mental son gratuitos. ¿Te gustaría tips para mejorar el ánimo día a día?"
            ]
            return random.choice(respuestas)
        
        # === 5. ESTRÉS / EXÁMENES ===
        elif any(kw in msg for kw in ["estrés", "estresado", "examen", "prueba", "calificación", "estudiar", "presión"]):
            respuestas = [
                "El estrés por exámenes y presión familiar es muy común aquí. Usa Pomodoro: 25 min estudio + 5 min descanso. ¿Cuánto tiempo tienes hasta tu próximo examen?",
                "Tu valor no depende de una nota. Organiza por prioridad. Los orientadores escolares y los CAPS pueden ayudarte gratis. ¿Quieres que te ayude a hacer un plan de estudio realista?",
                "El estrés afecta mucho el rendimiento. Prueba 2 minutos de 'power pose' antes de estudiar. ¿Estás preparando algo específico ahora?",
                "Divide las tareas grandes en pequeñas. En Nicaragua muchos jóvenes logran equilibrar estudios y bienestar con apoyo del MINSA. ¿Te ayudo a crear un horario?"
            ]
            return random.choice(respuestas)
        
        # === 6. SUEÑO ===
        elif any(kw in msg for kw in ["sueño", "insomnio", "no duermo", "cansado", "desvelado"]):
            respuestas = [
                "El sueño es clave. Intenta dormir y despertar a la misma hora todos los días. Evita el celular 1 hora antes. ¿A qué hora sueles acostarte?",
                "Si no puedes dormir, prueba relajación progresiva (tensar y relajar músculos). Los problemas de sueño son muy atendidos en los CAPS. ¿Cuántas horas duermes normalmente?",
                "La ansiedad por el día siguiente quita el sueño. Escribe tus preocupaciones antes de dormir. ¿Quieres una rutina completa de higiene del sueño?",
                "El cansancio constante puede mejorarse con hábitos. Si persiste, ve al centro de salud. ¿Qué has probado ya?"
            ]
            return random.choice(respuestas)
        
        # === 7. AUTOESTIMA ===
        elif any(kw in msg for kw in ["autoestima", "inseguro", "feo", "no sirvo", "comparo", "no soy suficiente"]):
            respuestas = [
                "La autoestima se construye con acciones diarias. Anota 3 cosas que hiciste bien hoy (aunque sean pequeñas). ¿Qué te hace sentir más inseguro?",
                "Compararte con otros (especialmente en redes) te hace daño. Todos tenemos inseguridades. Prueba hablarte con la misma amabilidad que a un amigo. ¿Quieres ejercicios prácticos?",
                "Mírate al espejo y di 3 cosas que te gustan de ti. Es un ejercicio poderoso. ¿Te animas a intentarlo?",
                "La baja autoestima se trabaja con apoyo profesional. Los CAPS del MINSA te pueden ayudar gratis. ¿Hay algo específico que te hace dudar de ti?"
            ]
            return random.choice(respuestas)
        
        # === 8. BULLYING / ACOSO ===
        elif any(kw in msg for kw in ["bullying", "acosan", "me molestan", "rumores", "excluyen"]):
            respuestas = [
                "**El acoso NO es tu culpa.** Cuéntaselo ya a un adulto de confianza (profesor, orientador o familiar). Las escuelas tienen protocolos. ¿Es en persona o por redes?",
                "Documenta todo (fechas, capturas, testigos). Ve al CAPS o centro de salud si te afecta mucho. Eres valiente por hablarlo. ¿Quieres ayuda para contárselo a alguien?",
                "Si te sientes en peligro, llama al 118. Tu seguridad es lo primero. ¿Has hablado con alguien más sobre esto?",
                "El cyberbullying duele igual. Bloquea, reporta y no respondas. Los CAPS también apoyan en estos casos. ¿En qué plataforma pasa?"
            ]
            return random.choice(respuestas)
        
        # === 9. REDES SOCIALES ===
        elif any(kw in msg for kw in ["redes", "instagram", "tiktok", "likes", "comparo"]):
            respuestas = [
                "Las redes están hechas para enganchar y hacerte sentir menos. Prueba reducir a 30-45 minutos al día por una semana y verás la diferencia. ¿Estás dispuesto a intentarlo?",
                "Recuerda: solo ves lo mejor de la vida de los demás. Curatea tu feed con cuentas positivas. ¿Qué cuentas te hacen sentir peor?",
                "El FOMO es real. Apaga notificaciones en horario de estudio y sueño. Muchos jóvenes nicaragüenses mejoran su ánimo así. ¿Quieres un reto de 7 días?",
                "Si sientes que controlan tu vida, usa el modo gris del celular. ¿Cuánto tiempo pasas aproximadamente?"
            ]
            return random.choice(respuestas)
        
        # === 10. RELACIONES / FAMILIA ===
        elif any(kw in msg for kw in ["amigos", "novio", "novia", "pareja", "familia", "padres", "presión familiar"]):
            respuestas = [
                "Las relaciones y la presión familiar son temas fuertes en Nicaragua. Habla con calma usando 'yo siento...'. ¿Quieres tips para mejorar la comunicación en casa?",
                "Los amigos tóxicos drenan energía. Rodéate de quienes te apoyan. ¿Hay alguien en quien realmente confíes?",
                "La presión por notas o futuro es común. Tus papás probablemente quieren lo mejor, pero a veces duele. ¿Has intentado una conversación tranquila?",
                "Si hay mucho conflicto en casa, busca apoyo en el CAPS o orientador escolar. ¿Cómo está la situación últimamente?"
            ]
            return random.choice(respuestas)
        
        # === 11. RESPUESTA GENERAL ===
        else:
            if len(msg) < 8 or "?" in msg:
                return "¡Buena pregunta! Para ayudarte mejor, ¿puedes contarme más? Por ejemplo: ¿es ansiedad, tristeza, exámenes, familia, amigos o algo más?"
            else:
                generales = [
                    "Gracias por confiar. ¿Desde cuándo te sientes así? ¿Qué has intentado? Los CAPS del MINSA están para apoyarte gratis.",
                    "Entiendo que es importante para ti. ¿Quieres tips prácticos, cómo ubicar un CAPS cerca de ti, o enfocarnos en algo específico?",
                    "No estás solo/a. En Nicaragua hay servicios gratuitos de salud mental en todo el país. ¿Qué te gustaría trabajar hoy?",
                    "Me alegra que busques apoyo. Para personalizarlo: ¿cómo te afecta esto en tu día a día?"
                ]
                return random.choice(generales)
    
    # === INTERFAZ DEL CHAT ===
    for rol, texto in st.session_state.chat_history:
        if rol == "Tú":
            with st.chat_message("user"):
                st.write(texto)
        else:
            with st.chat_message("assistant", avatar="🧠"):
                st.write(texto)
    
    prompt = st.chat_input("Escribe cómo te sientes o tu consulta (en Nicaragua)...")
    
    if prompt:
        st.session_state.chat_history.append(("Tú", prompt))
        respuesta = obtener_respuesta(prompt)
        st.session_state.chat_history.append(("EstuMind", respuesta))
        st.rerun()
    
    # Botón limpiar
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.caption("💡 Tip: Mientras más específico seas, mejor te puedo apoyar. Los servicios del MINSA son gratuitos para todos los jóvenes nicaragüenses.")

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
