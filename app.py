import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

# ==========================================
# 1. ESTILOS UI PREMIUM Y TYPOGRAPHY (DARK EMERALD & BLUE)
# ==========================================

st.set_page_config(page_title="ProGym Engine v6.0 - Science Edition", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Montserrat:wght@700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo principal y estructura */
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }
    
    /* Titulares principales */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Sidebars */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Tarjetas de Bloque de Entrenamiento */
    .block-card {
        padding: 1.4rem;
        border-radius: 12px;
        margin-bottom: 1.3rem;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #ffffff;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    .block-warmup { border-left: 6px solid #00e676; }
    .block-b { border-left: 6px solid #29b6f6; }
    .block-c { border-left: 6px solid #ab47bc; }
    .block-d { border-left: 6px solid #ff7043; }

    /* Badges Técnicos */
    .badge {
        display: inline-block;
        padding: 0.35em 0.75em;
        font-size: 75%;
        font-weight: 700;
        border-radius: 6px;
        margin-right: 6px;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-stress { background: linear-gradient(135deg, #ef5350, #d32f2f); }
    .badge-equip { background: linear-gradient(135deg, #0288d1, #01579b); }
    .badge-athletic { background: linear-gradient(135deg, #00c853, #007e33); }
    .badge-hypertrophy { background: linear-gradient(135deg, #aa00ff, #4a148c); }

    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(90deg, #00e676 0%, #29b6f6 100%);
        color: #0d1117;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        text-transform: uppercase;
        box-shadow: 0 4px 14px 0 rgba(0, 230, 118, 0.39);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(41, 182, 246, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODELOS DE DATOS & BASE AMPLIA (+60 EJERCICIOS)
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    bloque: str
    patron_movimiento: str
    musculo_principal: str
    equipamiento: str
    estres_articular: int
    longitud_muscular_maxima: bool  # Basado en hipertrofia mediada por estiramiento
    url_video: str = ""
    es_atletico: bool = False

if "base_ejercicios" not in st.session_state:
    st.session_state.base_ejercicios = [
        # --- WARM-UP, MOVILIDAD & PLIOMETRÍA (12 EJERCICIOS) ---
        Ejercicio("W1", "Gato-Camello Dinámico", "Warm-Up", "Movilidad Columna", "Zona Media", "Peso Corporal", 1, False, "https://www.youtube.com/watch?v=kqnua4rHVVA"),
        Ejercicio("W2", "World's Greatest Stretch", "Warm-Up", "Movilidad Cadera", "Cadera/Isquios", "Peso Corporal", 1, True, "https://www.youtube.com/watch?v=vV1p24vLuh4"),
        Ejercicio("W3", "Dislocaciones de Hombro con Banda", "Warm-Up", "Movilidad Hombros", "Manguito Rotador", "Banda elástica", 1, False, "https://www.youtube.com/watch?v=33P5AI27eiU"),
        Ejercicio("W4", "Rotación Torácica Quadrupedal", "Warm-Up", "Movilidad Torácica", "Espalda Alta", "Peso Corporal", 1, False, "https://www.youtube.com/watch?v=d_kXpW_QpNA"),
        Ejercicio("W5", "Saltos Pliométricos al Cajón", "Warm-Up", "Potencia / RFD", "Tren Inferior", "Peso Corporal", 2, False, "https://www.youtube.com/watch?v=52r_Ul5k03g", True),
        Ejercicio("W6", "Drop Jumps (Pliometría Reactiva)", "Warm-Up", "Stiffness Tendinoso", "Tríceps Sural", "Peso Corporal", 3, False, "", True),
        Ejercicio("W7", "Lanzamiento Balón Medicinal Medial", "Warm-Up", "Potencia Rotacional", "Core/Rotadores", "Balón Medicinal", 2, False, "", True),
        Ejercicio("W8", "Bear Crawl Isométrico", "Warm-Up", "Activación Core", "Zona Media", "Peso Corporal", 1, False, ""),
        Ejercicio("W9", "Dorsiflexión de Tobillo en Banco", "Warm-Up", "Movilidad Tobillo", "Sóleo/Gemelos", "Peso Corporal", 1, False, ""),
        Ejercicio("W10", "Aductores en Posición Roca", "Warm-Up", "Movilidad Cadera", "Aductores", "Peso Corporal", 1, True, ""),
        Ejercicio("W11", "90/90 de Cadera Dinámico", "Warm-Up", "Movilidad Cadera", "Rotadores Cadera", "Peso Corporal", 1, False, ""),
        Ejercicio("W12", "Y-T-W en Banco Inclinado", "Warm-Up", "Activación Escapular", "Trapecio Inferior", "Mancuernas", 1, False, ""),

        # --- EMPUJES: HORIZONTAL Y VERTICAL (14 EJERCICIOS) ---
        Ejercicio("E1", "Press de Banca Plano con Barra", "Bloque B", "Empuje Horizontal", "Pectoral Mayor", "Barra", 4, False, "https://www.youtube.com/watch?v=rT7DgCr-3pg"),
        Ejercicio("E2", "Press Inclinado 30° con Mancuernas", "Bloque B", "Empuje Horizontal", "Pectoral Clavicular", "Mancuernas", 3, True, "https://www.youtube.com/watch?v=8iPEnn-ltC8"),
        Ejercicio("E3", "Press Militar de Pie con Barra", "Bloque B", "Empuje Vertical", "Deltoides Anterior", "Barra", 4, False, "https://www.youtube.com/watch?v=2yjwXTZQDDI"),
        Ejercicio("E4", "Push Press Explosivo", "Bloque B", "Potencia Superior", "Deltoides / Tríceps", "Barra", 4, False, "", True),
        Ejercicio("E5", "Fondos en Paralelas Lastrados", "Bloque B", "Empuje Vertical", "Pectoral / Tríceps", "Peso Corporal", 4, True, ""),
        Ejercicio("E6", "Press Landmine Unilateral", "Bloque C", "Empuje Unilateral", "Pectoral / Deltoides", "Barra", 2, False, "", True),
        Ejercicio("E7", "Press Declinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral Esternal", "Mancuernas", 3, False, ""),
        Ejercicio("E8", "Cruces de Polea Alta a Baja", "Bloque D", "Aislamiento", "Pectoral Inferior", "Polea", 1, True, ""),
        Ejercicio("E9", "Press Arnold Sentado", "Bloque C", "Empuje Vertical", "Deltoides", "Mancuernas", 3, False, ""),
        Ejercicio("E10", "Flexiones Deficitarias sobre Parralettes", "Bloque C", "Empuje Horizontal", "Pectoral Mayor", "Peso Corporal", 2, True, ""),
        Ejercicio("E11", "Press de Pecho en Máquina Convergente", "Bloque C", "Empuje Horizontal", "Pectoral", "Máquina", 2, True, ""),
        Ejercicio("E12", "Press Z-Press con Barra", "Bloque C", "Empuje Vertical / Core", "Deltoides / Core", "Barra", 3, False, True),
        Ejercicio("E13", "Extensiones de Tríceps tras Nuca Polea", "Bloque D", "Aislamiento", "Tríceps Cabeza Larga", "Polea", 1, True, ""),
        Ejercicio("E14", "Press Francés Inclinado con Barra Z", "Bloque D", "Aislamiento", "Tríceps Cabeza Larga", "Barra", 2, True, ""),

        # --- TRACCIONES: HORIZONTAL Y VERTICAL (14 EJERCICIOS) ---
        Ejercicio("T1", "Dominadas Neutras Lastradas", "Bloque B", "Tracción Vertical", "Dorsal Ancho", "Peso Corporal", 4, True, "https://www.youtube.com/watch?v=eGo4IYlbE5g"),
        Ejercicio("T2", "Remo Pendlay con Barra", "Bloque B", "Tracción Horizontal", "Dorsal / Romboide", "Barra", 4, False, ""),
        Ejercicio("T3", "Jalón al Pecho Agarre Abierto", "Bloque C", "Tracción Vertical", "Dorsal Ancho", "Polea", 2, True, "https://www.youtube.com/watch?v=CAwf7n6Luuc"),
        Ejercicio("T4", "Remo Unilateral con Mancuerna (Kroc)", "Bloque C", "Tracción Horizontal", "Dorsal Ancho", "Mancuernas", 2, True, ""),
        Ejercicio("T5", "Remo Pecho Apoyado en Banco 45°", "Bloque C", "Tracción Horizontal", "Espalda Alta", "Mancuernas", 2, False, ""),
        Ejercicio("T6", "Pull-over con Cuerda en Polea Alta", "Bloque D", "Aislamiento", "Dorsal Ancho", "Polea", 1, True, ""),
        Ejercicio("T7", "Remo Gironda con Agarre Estrecho", "Bloque C", "Tracción Horizontal", "Dorsal / Redondo", "Polea", 2, False, ""),
        Ejercicio("T8", "Dominadas Explosivas al Pecho", "Bloque B", "Potencia Superior", "Dorsal", "Peso Corporal", 3, False, "", True),
        Ejercicio("T9", "Face Pull en Polea con Cuerda", "Bloque D", "Salud Articular", "Deltoides Post / Rotadores", "Polea", 1, False, "https://www.youtube.com/watch?v=rep-qVOkqgk"),
        Ejercicio("T10", "Remo Invertido en Anillas", "Bloque C", "Tracción Horizontal", "Romboide / Core", "Peso Corporal", 2, False, True),
        Ejercicio("T11", "Jalón Unilateral en Polea Alta", "Bloque C", "Tracción Vertical", "Dorsal Ancho", "Polea", 1, True, ""),
        Ejercicio("T12", "Pájaro con Mancuernas en Banco", "Bloque D", "Aislamiento", "Deltoides Posterior", "Mancuernas", 1, False, ""),
        Ejercicio("T13", "Curl de Bíceps Inclinado 45°", "Bloque D", "Aislamiento", "Bíceps Cabeza Larga", "Mancuernas", 1, True, "https://www.youtube.com/watch?v=soxrZlIl35U"),
        Ejercicio("T14", "Curl Spider en Banco Inclinado", "Bloque D", "Aislamiento", "Bíceps Cabeza Corta", "Barra", 1, False, ""),

        # --- DOMINANTES DE RODILLA & CADERA (16 EJERCICIOS) ---
        Ejercicio("R1", "Sentadilla Trasera Barra Alta", "Bloque B", "Dominante de Rodilla", "Cuádriceps", "Barra", 5, True, "https://www.youtube.com/watch?v=ultWZbUMPL8"),
        Ejercicio("R2", "Sentadilla Frontal con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps / Core", "Barra", 5, True, "", True),
        Ejercicio("R3", "Peso Muerto Rumano con Barra", "Bloque B", "Dominante de Cadera", "Isquiosurales", "Barra", 4, True, "https://www.youtube.com/watch?v=JCXUYuzwNrM"),
        Ejercicio("R4", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Cadena Posterior", "Barra", 5, False, "https://www.youtube.com/watch?v=op9kVnSso6Q"),
        Ejercicio("R5", "Power Clean desde Bloques", "Bloque B", "Potencia Olímpica", "Cadena Posterior", "Barra", 5, False, "", True),
        Ejercicio("R6", "Sentadilla Búlgara con Mancuernas", "Bloque C", "Dominante Unilateral", "Cuádriceps / Glúteo", "Mancuernas", 3, True, ""),
        Ejercicio("R7", "Hip Thrust con Barra Lastrada", "Bloque B", "Dominante de Cadera", "Glúteo Mayor", "Barra", 3, False, ""),
        Ejercicio("R8", "Prensa 45° Pies Abajos", "Bloque C", "Dominante de Rodilla", "Cuádriceps", "Máquina", 2, True, "https://www.youtube.com/watch?v=IZxyjW7MPJQ"),
        Ejercicio("R9", "Curl Femoral Tumbado", "Bloque D", "Aislamiento", "Isquiosurales", "Máquina", 1, True, ""),
        Ejercicio("R10", "Curl Nórdico de Isquios", "Bloque D", "Excéntrico Intenso", "Isquiosurales", "Peso Corporal", 4, True, "", True),
        Ejercicio("R11", "Sentadilla Hack en Máquina", "Bloque B", "Dominante de Rodilla", "Cuádriceps", "Máquina", 3, True, ""),
        Ejercicio("R12", "Step-Up Unilateral Explosivo", "Bloque C", "Potencia Unilateral", "Cuádriceps / Glúteo", "Mancuernas", 3, False, "", True),
        Ejercicio("R13", "Peso Muerto Sumo", "Bloque B", "Dominante de Cadera", "Glúteos / Aductores", "Barra", 4, False, ""),
        Ejercicio("R14", "Extensiones de Cuádriceps", "Bloque D", "Aislamiento", "Recto Femoral", "Máquina", 1, False, ""),
        Ejercicio("R15", "Kettlebell Swing de Potencia", "Bloque C", "Potencia Cadera", "Glúteo / Isquios", "Mancuernas", 2, False, "", True),
        Ejercicio("R16", "Sentadilla Sissy Peso Corporal", "Bloque D", "Aislamiento Estiramiento", "Cuádriceps", "Peso Corporal", 3, True, "")
    ]

if "historial_feedback" not in st.session_state:
    st.session_state.historial_feedback = []

if "profesor_autenticado" not in st.session_state:
    st.session_state.profesor_autenticado = False

@dataclass
class PerfilAtleta:
    nombre: str
    tipo_rutina: str
    objetivo: str
    es_deportista: bool = False
    musculo_especializacion: Optional[str] = None
    equipamiento_disponible: List[str] = field(default_factory=list)

    def evaluar_wellness(self, sueno: int, estres: int, agujetas: int, fatiga: int) -> float:
        return round(((min(max(sueno, 1), 5)) + (6 - min(max(estres, 1), 5)) + (6 - min(max(agujetas, 1), 5)) + (6 - min(max(fatiga, 1), 5))) / 4.0, 2)

# ==========================================
# 3. MOTOR DE PROGRAMACIÓN CIENTÍFICA
# ==========================================

class MotorEntrenamientoCientifico:

    @staticmethod
    def obtener_parametros_objetivo(objetivo: str) -> Dict[str, str]:
        if objetivo == "Hipertrofia (Tensión & Estiramiento)":
            return {"reps_b": "6-8", "reps_c": "8-12", "reps_d": "10-15", "rir_base": 1, "factor_volumen": 1.0}
        elif objetivo == "Pérdida de Grasa (Preservación Muscular)":
            return {"reps_b": "6-8", "reps_c": "10-12", "reps_d": "12-15", "rir_base": 1, "factor_volumen": 0.8}
        elif objetivo == "Performance Deportiva (Potencia & RFD)":
            return {"reps_b": "3-5 (Max Vel)", "reps_c": "5-8", "reps_d": "8-10", "rir_base": 2, "factor_volumen": 1.0}
        else:
            return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "12-15", "rir_base": 2, "factor_volumen": 0.75}

    @staticmethod
    def filtrar_patrones_por_rutina(tipo_rutina: str, sub_dia: str) -> List[str]:
        if tipo_rutina == "Fullbody": return ["Empuje Horizontal", "Dominante de Rodilla", "Tracción Vertical", "Dominante de Cadera"]
        elif tipo_rutina == "Torso-Pierna": return ["Empuje Horizontal", "Tracción Vertical", "Empuje Vertical", "Tracción Horizontal"] if sub_dia == "Torso" else ["Dominante de Rodilla", "Dominante de Cadera", "Dominante Unilateral"]
        elif tipo_rutina == "Push-Pull-Legs (PPL)":
            if sub_dia == "Push (Empuje)": return ["Empuje Horizontal", "Empuje Vertical"]
            elif sub_dia == "Pull (Tracción)": return ["Tracción Vertical", "Tracción Horizontal"]
            else: return ["Dominante de Rodilla", "Dominante de Cadera"]
        else: return ["Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", "Dominante de Rodilla"]

    @staticmethod
    def sustituir_ejercicio(ejercicio_actual: Ejercicio, equipamiento_disponible: List[str]) -> Optional[Ejercicio]:
        candidatos = [
            e for e in st.session_state.base_ejercicios
            if e.id != ejercicio_actual.id and e.bloque == ejercicio_actual.bloque
            and (e.patron_movimiento == ejercicio_actual.patron_movimiento or e.musculo_principal == ejercicio_actual.musculo_principal)
            and e.estres_articular <= ejercicio_actual.estres_articular and e.equipamiento in equipamiento_disponible
        ]
        candidatos.sort(key=lambda x: (not x.longitud_muscular_maxima, x.estres_articular))
        return candidatos[0] if candidatos else None

    @staticmethod
    def generar_rutina_cientifica(atleta: PerfilAtleta, sub_dia: str, score_wellness: float) -> Dict[str, List[Dict]]:
        rutina_bloques = {"Warm-Up": [], "Bloque B": [], "Bloque C": [], "Bloque D": []}
        params_obj = MotorEntrenamientoCientifico.obtener_parametros_objetivo(atleta.objetivo)
        mod_series = -1 if score_wellness < 3.0 else 0
        mod_rir = +2 if score_wellness < 3.0 else 0
        patrones_sesion = MotorEntrenamientoCientifico.filtrar_patrones_por_rutina(atleta.tipo_rutina, sub_dia)

        # WARM-UP & PLIOMETRÍA
        warmup = [e for e in st.session_state.base_ejercicios if e.bloque == "Warm-Up" and e.equipamiento in atleta.equipamiento_disponible]
        if atleta.es_deportista: warmup.sort(key=lambda x: not x.es_atletico)
        for ej in warmup[:3]:
            rutina_bloques["Warm-Up"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": "2 Series x 8-10 Reps (RIR 4 - Control Explosivo)",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "estiramiento": ej.longitud_muscular_maxima
            })

        # BLOQUE B (Tensión Mecánica / Potencia)
        principales = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque B" and (e.patron_movimiento in patrones_sesion or (atleta.es_deportista and e.es_atletico)) and e.equipamiento in atleta.equipamiento_disponible]
        # Priorizar ejercicios en máxima longitud muscular para hipertrofia o atléticos para rendimiento
        principales.sort(key=lambda x: (not x.es_atletico if atleta.es_deportista else not x.longitud_muscular_maxima))
        for ej in principales[:2]:
            series = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque B"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_b']} | RIR {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "estiramiento": ej.longitud_muscular_maxima
            })

        # BLOQUE C (Hipertrofia Complementaria / Estiramiento)
        secundarios = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque C" and e.equipamiento in atleta.equipamiento_disponible]
        secundarios.sort(key=lambda x: not x.longitud_muscular_maxima)
        for ej in secundarios[:2]:
            series_finales = max(2, int(3 * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque C"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_c']} | RIR {params_obj['rir_base'] + mod_rir + 1}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "estiramiento": ej.longitud_muscular_maxima
            })

        # BLOQUE D (Aislamiento & Metábólico)
        accesorios = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque D" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in accesorios[:2]:
            series_acc = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series_acc * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque D"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_d']} | RIR {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "estiramiento": ej.longitud_muscular_maxima
            })

        return rutina_bloques

# ==========================================
# 4. INTERFAZ GRÁFICA DE USUARIO
# ==========================================

st.title("⚡ ProGym Engine v6.0 — Science & Performance")

# Selector de Rol y Autenticación
st.sidebar.header("🔑 Control de Rol & Acceso")
rol_usuario = st.sidebar.radio("Selecciona tu Rol:", ["Alumno / Deportista", "Profesor / Entrenador"])

if rol_usuario == "Profesor / Entrenador":
    if not st.session_state.profesor_autenticado:
        st.sidebar.subheader("🔒 Autenticación Docente")
        password_input = st.sidebar.text_input("Ingrese Contraseña:", type="password", key="pwd_input")
        if st.sidebar.button("Ingresar Panel Profe"):
            if password_input == "1234":
                st.session_state.profesor_autenticado = True
                st.sidebar.success("✅ Acceso Concedido")
                st.rerun()
            else:
                st.sidebar.error("❌ Contraseña Incorrecta")
    else:
        st.sidebar.success("🔓 Acceso Docente Activo")
        if st.sidebar.button("Cerrar Sesión Profesor"):
            st.session_state.profesor_autenticado = False
            st.rerun()

st.sidebar.divider()
st.sidebar.header("👤 Perfil del Atleta")
nombre = st.sidebar.text_input("Nombre Usuario", "Carlos Pérez")
es_deportista = st.sidebar.checkbox("🏅 Atleta de Alto Rendimiento", value=False)
tipo_rutina = st.sidebar.selectbox("Modalidad de Rutina", ["Fullbody", "Torso-Pierna", "Push-Pull-Legs (PPL)", "Weider"])
objetivo = st.sidebar.selectbox("Objetivo Científico", ["Hipertrofia (Tensión & Estiramiento)", "Performance Deportiva (Potencia & RFD)", "Pérdida de Grasa (Preservación Muscular)", "Mantenimiento / Salud"])
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral Mayor", "Cuádriceps", "Dorsal Ancho", "Deltoides", "Isquiosurales"])

equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"]
)

st.sidebar.divider()
st.sidebar.header("📊 Wellness Pre-Entreno")
sueno = st.sidebar.slider("Sueño (1-5)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1-5)", 1, 5, 3)
agujetas = st.sidebar.slider("Agujetas (1-5)", 1, 5, 3)
fatiga = st.sidebar.slider("Fatiga General (1-5)", 1, 5, 3)

atleta = PerfilAtleta(nombre=nombre, tipo_rutina=tipo_rutina, objetivo=objetivo, es_deportista=es_deportista, musculo_especializacion=especializacion, equipamiento_disponible=equipamiento)
score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Banner Principal
col_w1, col_w2 = st.columns([1, 3])
with col_w1: st.metric("Score Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0: st.error("⚠️ **Autorregulación Activa:** Se reduce el volumen total y la intensidad para evitar sobre-fatiga central.")
    else: st.success(f"✅ Estado Óptimo | Paradigma: **{objetivo}** | Formato: **{tipo_rutina}**")

st.divider()

# Pestañas
tab_rutina, tab_docente, tab_plan, tab_crud, tab_remplazo = st.tabs([
    "📋 Sesión Diaria & Feedback",
    "👨‍🏫 Panel Docente",
    "🗓️ Programación Semanal / Mensual",
    "🛠️ Banco de Ejercicios (+60)",
    "🔄 Sustitución Científica"
])

# ==========================================
# PESTAÑA 1: SESIÓN DIARIA & FEEDBACK
# ==========================================
with tab_rutina:
    sub_dia = "General"
    if tipo_rutina == "Torso-Pierna": sub_dia = st.radio("Día:", ["Torso", "Pierna"], horizontal=True)
    elif tipo_rutina == "Push-Pull-Legs (PPL)": sub_dia = st.radio("Día:", ["Push (Empuje)", "Pull (Tracción)", "Legs (Pierna)"], horizontal=True)

    rutina = MotorEntrenamientoCientifico.generar_rutina_cientifica(atleta, sub_dia, score_wellness)
    inputs_feedback = {}

    def render_bloque(titulo: str, lista_ejercicios: List[Dict], css_class: str):
        st.markdown(f'<div class="block-card {css_class}"><h3>{titulo}</h3></div>', unsafe_allow_html=True)
        for item in lista_ejercicios:
            col_info, col_feed = st.columns([2, 1])
            with col_info:
                badge_stretch = '<span class="badge badge-hypertrophy">Max Estiramiento</span>' if item['estiramiento'] else ''
                badge_atl = '<span class="badge badge-athletic">Atrapado RFD</span>' if item['atletico'] else ''
                st.markdown(f"**{item['nombre']}** — *{item['patron']}* | {badge_stretch} {badge_atl} <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
                st.caption(f"📌 Prescripción: **{item['detalles']}**")
                if item["video"]:
                    with st.expander("🎥 Ver Ejecución Técnica"):
                        st.video(item["video"])
            with col_feed:
                st.markdown("**📝 Registro de Serie Real:**")
                carga_reps = st.text_input(f"Carga / Reps ({item['id']})", placeholder="Ej: 90kg x 8", key=f"c_{item['id']}")
                rir_rpe = st.select_slider(f"RIR Percibido ({item['id']})", options=["RIR 0 (Fallo)", "RIR 1", "RIR 2", "RIR 3", "RIR 4+"], value="RIR 1", key=f"r_{item['id']}")
                nota = st.text_input(f"Notas ({item['id']})", placeholder="Fatiga, molestia...", key=f"n_{item['id']}")
                
                inputs_feedback[item['nombre']] = {
                    "ejercicio_id": item['id'],
                    "carga_reps": carga_reps,
                    "rir_rpe": rir_rpe,
                    "nota": nota
                }
            st.divider()

    render_bloque("🔥 WARM-UP & PLIOMETRÍA (OBLIGATORIO)", rutina["Warm-Up"], "block-warmup")
    render_bloque("BLOQUE B: Tensión Mecánica / Potencia Principal", rutina["Bloque B"], "block-b")
    render_bloque("BLOQUE C: Hipertrofia Mediada por Estiramiento", rutina["Bloque C"], "block-c")
    render_bloque("BLOQUE D: Accesorios & Cargas Metabólicas", rutina["Bloque D"], "block-d")

    if st.button("💾 Enviar Feedback al Entrenador", type="primary"):
        registro_sesion = {
            "fecha": str(datetime.date.today()),
            "alumno": nombre,
            "objetivo": objetivo,
            "rutina": tipo_rutina,
            "detalles_ejercicios": inputs_feedback
        }
        st.session_state.historial_feedback.append(registro_sesion)
        st.success("✅ Feedback registrado. Tu entrenador puede supervisarlo inmediatamente.")

# ==========================================
# PESTAÑA 2: PANEL DOCENTE
# ==========================================
with tab_docente:
    st.subheader("👨‍🏫 Panel de Control del Entrenador")
    
    if rol_usuario == "Profesor / Entrenador" and st.session_state.profesor_autenticado:
        st.write("### 📥 Historial de Feedback de Alumnos")
        
        if not st.session_state.historial_feedback:
            st.info("No hay registros en la sesión actual.")
        else:
            for idx, reg in enumerate(reversed(st.session_state.historial_feedback)):
                with st.expander(f"👤 Alumno: {reg['alumno']} | Fecha: {reg['fecha']} | {reg['rutina']} ({reg['objetivo']})"):
                    st.write("**Desglose del Entrenamiento:**")
                    for ej_nombre, datos in reg["detalles_ejercicios"].items():
                        if datos["carga_reps"] or datos["nota"]:
                            st.markdown(f"- **{ej_nombre}**: {datos['carga_reps']} | RIR Real: **{datos['rir_rpe']}** | *Comentarios: {datos['nota']}*")
                    
                    st.text_area(f"✍️ Notas / Correcciones del Profesor", key=f"resp_prof_{idx}")
                    if st.button(f"Guardar Ajuste #{idx}"):
                        st.success("Ajuste registrado.")
    else:
        st.warning("🔒 Requiere autenticación de **Profesor** (Contraseña `1234`).")

# ==========================================
# PESTAÑA 3: PROGRAMACIÓN SEMANAL / MENSUAL
# ==========================================
with tab_plan:
    st.subheader("🗓️ Programación Basada en la Ciencia")
    vista_plan = st.radio("Seleccionar Estrategia", ["Ondulación Diaria (Microciclo)", "Periodización del Mesociclo (4 Semanas)"], horizontal=True)

    if vista_plan == "Ondulación Diaria (Microciclo)":
        st.markdown("### Estrategia de Microciclo (Ondulada)")
        dias = ["Lunes (Hipertrofia / Fuerza)", "Martes (Potencia / Tensión)", "Miércoles (Descanso Activo)", "Jueves (Hipertrofia en Estiramiento)", "Viernes (Volumen Metabólico)", "Sábado (Pliometría / Cardio)", "Domingo (Descanso Total)"]
        for d in dias:
            with st.expander(f"📅 {d}"):
                st.write(f"Estructura asignada bajo **{tipo_rutina}**.")
                st.caption("Frecuencia 2x por grupo muscular con distribución biomecánica variada.")
    else:
        st.markdown("### Programación Científica del Mesociclo")
        prog_mensual = [
            {"Semana": "Semana 1", "Fase": "Sensibilización al Volumen", "Volumen": "10-12 Series / Músculo", "Intensidad": "RIR 2-3"},
            {"Semana": "Semana 2", "Fase": "Sobrecarga Progresiva", "Volumen": "14-16 Series / Músculo", "Intensidad": "RIR 1-2"},
            {"Semana": "Semana 3", "Fase": "Pico de Overreaching", "Volumen": "18-20 Series / Músculo", "Intensidad": "RIR 0-1 (Fallo Técnico)"},
            {"Semana": "Semana 4", "Fase": "Descarga Funcional (Deload)", "Volumen": "6-8 Series / Músculo", "Intensidad": "RIR 3-4"},
        ]
        st.table(prog_mensual)

# ==========================================
# PESTAÑA 4: BANCO DE EJERCICIOS (CRUD PROFESOR)
# ==========================================
with tab_crud:
    st.subheader("🛠️ Banco de Ejercicios Masivo")
    
    if rol_usuario == "Profesor / Entrenador" and st.session_state.profesor_autenticado:
        st.markdown("### ➕ Registrar Nuevo Ejercicio")
        with st.form("form_nuevo_ejercicio"):
            col1, col2, col3 = st.columns(3)
            with col1:
                n_id = st.text_input("ID Ejercicio", f"EX{len(st.session_state.base_ejercicios)+1}")
                n_nombre = st.text_input("Nombre Ejercicio", "")
                n_bloque = st.selectbox("Bloque", ["Warm-Up", "Bloque B", "Bloque C", "Bloque D"])
            with col2:
                n_patron = st.selectbox("Patrón de Movimiento", ["Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", "Tracción Horizontal", "Dominante de Rodilla", "Dominante de Cadera", "Movilidad Cadera", "Aislamiento", "Potencia / RFD"])
                n_musculo = st.text_input("Músculo Principal", "")
                n_equipo = st.selectbox("Equipamiento Required", ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"])
            with col3:
                n_estres = st.slider("Estrés Articular (1-5)", 1, 5, 2)
                n_url = st.text_input("URL Video YouTube", "")
                n_atletico = st.checkbox("¿Es para Atletismo/Performance?", value=False)
                n_stretch = st.checkbox("¿Énfasis en Posición de Estiramiento?", value=False)
            
            if st.form_submit_button("Guardar Ejercicio"):
                if n_nombre:
                    nuevo_ej = Ejercicio(n_id, n_nombre, n_bloque, n_patron, n_musculo, n_equipo, n_estres, n_stretch, n_url, n_atletico)
                    st.session_state.base_ejercicios.append(nuevo_ej)
                    st.success(f"✔️ Ejercicio '{n_nombre}' guardado exitosamente.")
                else:
                    st.error("Ingresa el nombre del ejercicio.")

        st.divider()
        st.markdown("### ❌ Eliminar Ejercicio")
        ej_eliminar = st.selectbox("Selecciona ejercicio a eliminar:", [e.nombre for e in st.session_state.base_ejercicios])
        if st.button("Eliminar Ejercicio Seleccionado"):
            st.session_state.base_ejercicios = [e for e in st.session_state.base_ejercicios if e.nombre != ej_eliminar]
            st.success(f"Ejercicio '{ej_eliminar}' eliminado de la base de datos.")
            st.rerun()

    else:
        st.warning("🔒 Requiere autenticación de **Profesor** para modificar la base de datos.")

    st.subheader(f"📚 Catálogo Completo ({len(st.session_state.base_ejercicios)} Ejercicios Disponibles)")
    tabla_datos = [{
        "ID": e.id, "Bloque": e.bloque, "Nombre": e.nombre, "Patrón": e.patron_movimiento,
        "Músculo": e.musculo_principal, "Equipo": e.equipamiento, "Estrés": f"{e.estres_articular}/5",
        "Max Estiramiento": "Sí" if e.longitud_muscular_maxima else "No", "Deportivo": "Sí" if e.es_atletico else "No"
    } for e in st.session_state.base_ejercicios]
    st.dataframe(tabla_datos, use_container_width=True)

# ==========================================
# PESTAÑA 5: SUSTITUCIÓN CIENTÍFICA
# ==========================================
with tab_remplazo:
    st.subheader("🔄 Sustitución Inteligente Basada en Biomecánica")
    ej_sel = st.selectbox("Selecciona el ejercicio a cambiar:", [e.nombre for e in st.session_state.base_ejercicios])
    if st.button("Buscar Alternativa Inteligente"):
        obj_ej = next(e for e in st.session_state.base_ejercicios if e.nombre == ej_sel)
        reemplazo = MotorEntrenamientoCientifico.sustituir_ejercicio(obj_ej, atleta.equipamiento_disponible)
        if reemplazo:
            st.success(f"✔️ **Sustituto Sugerido:** {reemplazo.nombre}")
            st.write(f"- **Bloque:** {reemplazo.bloque} | **Patrón:** {reemplazo.patron_movimiento}")
            st.write(f"- **Énfasis en Estiramiento:** {'Sí' if reemplazo.longitud_muscular_maxima else 'No'} | **Estrés Articular:** {reemplazo.estres_articular}/5")
            if reemplazo.url_video: st.video(reemplazo.url_video)
        else:
            st.warning("No hay alternativas disponibles para ese patrón con el equipamiento disponible.")
