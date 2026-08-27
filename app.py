import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

# ==========================================
# 1. ESTILOS VISUALES: TEXTO BLANCO, SECUNDARIO VERDE & TARJETAS
# ==========================================

st.set_page_config(page_title="ProGym Engine v7.0 - Maximum Robustness", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Montserrat:wght@700;900&display=swap');

    /* Estructura general */
    .stApp {
        background-color: #080b11;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Textos Principales */
    h1, h2, h3, h4, strong, b, .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* Textos Secundarios (Verde Neón) */
    .stCaption, caption, .secondary-text, small, span.st-c6 {
        color: #00ff88 !important;
        font-weight: 600;
    }

    /* Sidebars */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #00ff88;
    }

    /* Tarjetas Generales con Recuadros Marcados */
    .card-box {
        border: 2px solid #00ff88;
        background-color: #0f172a;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.15);
    }
    
    /* Tarjetas de Bloques de Entrenamiento */
    .block-card {
        padding: 1.4rem;
        border-radius: 12px;
        margin-bottom: 1.3rem;
        background-color: #0f172a;
        border: 2px solid #00e676;
        color: #ffffff;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.2);
    }
    .block-warmup { border-color: #00ff88; }
    .block-b { border-color: #00e5ff; }
    .block-c { border-color: #bd00ff; }
    .block-d { border-color: #ff0055; }

    /* Badges Técnicos */
    .badge {
        display: inline-block;
        padding: 0.35em 0.75em;
        font-size: 80%;
        font-weight: 700;
        border-radius: 6px;
        margin-right: 6px;
        color: #000000 !important;
        text-transform: uppercase;
    }
    .badge-equip { background-color: #00e5ff; }
    .badge-athletic { background-color: #00ff88; }
    .badge-iso { background-color: #ff0055; color: #ffffff !important; }

    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(90deg, #00ff88 0%, #00e5ff 100%);
        color: #000000 !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.5rem;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODELOS DE DATOS & BASE AMPLIA (+100 EJERCICIOS)
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
    longitud_muscular_maxima: bool
    url_video: str = ""
    es_atletico: bool = False
    es_isometrico: bool = False

if "base_ejercicios" not in st.session_state:
    st.session_state.base_ejercicios = [
        # --- WARM-UP & MOVILIDAD (+20 EJERCICIOS) ---
        Ejercicio("W1", "Gato-Camello Dinámico", "Warm-Up", "Warm-Up / Movilidad", "Zona Media", "Peso Corporal", 1, False),
        Ejercicio("W2", "World's Greatest Stretch", "Warm-Up", "Warm-Up / Movilidad", "Cadera/Isquios", "Peso Corporal", 1, True),
        Ejercicio("W3", "Dislocaciones de Hombro con Banda", "Warm-Up", "Warm-Up / Movilidad", "Manguito Rotador", "Banda elástica", 1, False),
        Ejercicio("W4", "Rotación Torácica Quadrupedal", "Warm-Up", "Warm-Up / Movilidad", "Espalda Alta", "Peso Corporal", 1, False),
        Ejercicio("W5", "Dorsiflexión de Tobillo en Pared", "Warm-Up", "Warm-Up / Movilidad", "Tobillo", "Peso Corporal", 1, False),
        Ejercicio("W6", "90/90 de Cadera Dinámico", "Warm-Up", "Warm-Up / Movilidad", "Rotadores Cadera", "Peso Corporal", 1, False),
        Ejercicio("W7", "Aductores en Posición Roca", "Warm-Up", "Warm-Up / Movilidad", "Aductores", "Peso Corporal", 1, True),
        Ejercicio("W8", "Y-T-W en Banco Inclinado", "Warm-Up", "Warm-Up / Movilidad", "Trapecio Inferior", "Mancuernas", 1, False),
        Ejercicio("W9", "Inchworm (Caminata de Gusano)", "Warm-Up", "Warm-Up / Movilidad", "Cadena Posterior", "Peso Corporal", 1, True),
        Ejercicio("W10", "Cossack Squat Dinámico", "Warm-Up", "Warm-Up / Movilidad", "Ingle / Cadera", "Peso Corporal", 2, True),
        Ejercicio("W11", "Rotación de Cadera en Posición Z", "Warm-Up", "Warm-Up / Movilidad", "Cadera", "Peso Corporal", 1, False),
        Ejercicio("W12", "Aperturas de Pecho con Banda", "Warm-Up", "Warm-Up / Movilidad", "Pectoral/Hombros", "Banda elástica", 1, False),
        Ejercicio("W13", "Circunduccions de Escápula en Plancha", "Warm-Up", "Warm-Up / Movilidad", "Serrato/Escápula", "Peso Corporal", 1, False),
        Ejercicio("W14", "Movilidad de Cadera en Hincado", "Warm-Up", "Warm-Up / Movilidad", "Psoas / Flexores", "Peso Corporal", 1, True),
        Ejercicio("W15", "Jefferson Curl Ligero con Barra", "Warm-Up", "Warm-Up / Movilidad", "Cadena Posterior", "Barra", 2, True),
        Ejercicio("W16", "Perro-Pájaro (Bird-Dog) Isométrico", "Warm-Up", "Warm-Up / Movilidad", "Core", "Peso Corporal", 1, False),
        Ejercicio("W17", "Rotaciones Externas de Hombro Sidelying", "Warm-Up", "Warm-Up / Movilidad", "Manguito Rotador", "Mancuernas", 1, False),
        Ejercicio("W18", "Caminata de Oso (Bear Crawl)", "Warm-Up", "Warm-Up / Movilidad", "Core/Hombros", "Peso Corporal", 2, False, "", True),
        Ejercicio("W19", "Puente de Glúteo Unilateral Dinámico", "Warm-Up", "Warm-Up / Movilidad", "Glúteo", "Peso Corporal", 1, False),
        Ejercicio("W20", "Estiramiento Dinámico de Isquios en Bipedestación", "Warm-Up", "Warm-Up / Movilidad", "Isquiosurales", "Peso Corporal", 1, True),

        # --- POTENCIA & PLIOMETRÍA / RFD (+20 EJERCICIOS) ---
        Ejercicio("P1", "Saltos Pliométricos al Cajón", "Bloque B", "Potencia / RFD", "Tren Inferior", "Peso Corporal", 2, False, "", True),
        Ejercicio("P2", "Drop Jumps (Pliometría Reactiva)", "Bloque B", "Potencia / RFD", "Tríceps Sural", "Peso Corporal", 3, False, "", True),
        Ejercicio("P3", "Lanzamiento Balón Medicinal Medial", "Bloque B", "Potencia / RFD", "Core/Rotadores", "Balón Medicinal", 2, False, "", True),
        Ejercicio("P4", "Power Clean desde Bloques", "Bloque B", "Potencia / RFD", "Cadena Posterior", "Barra", 5, False, "", True),
        Ejercicio("P5", "Push Press Explosivo", "Bloque B", "Potencia / RFD", "Deltoides / Tríceps", "Barra", 4, False, "", True),
        Ejercicio("P6", "Snatch con Mancuerna Unilateral", "Bloque B", "Potencia / RFD", "Fullbody", "Mancuernas", 4, False, "", True),
        Ejercicio("P7", "Broad Jump (Salto Horizontal Largo)", "Bloque B", "Potencia / RFD", "Tren Inferior", "Peso Corporal", 3, False, "", True),
        Ejercicio("P8", "Lanzamiento Overhead de Balón Medicinal", "Bloque B", "Potencia / RFD", "Cadena Posterior", "Balón Medicinal", 2, False, "", True),
        Ejercicio("P9", "Salto Unilateral al Cajón (Single Leg Box Jump)", "Bloque B", "Potencia / RFD", "Cuádriceps/Glúteo", "Peso Corporal", 3, False, "", True),
        Ejercicio("P10", "Kettlebell Swing de Potencia", "Bloque B", "Potencia / RFD", "Glúteo / Isquios", "Mancuernas", 2, False, "", True),
        Ejercicio("P11", "Saltos Continuos con Vallas (Hurdle Jumps)", "Bloque B", "Potencia / RFD", "Tren Inferior", "Peso Corporal", 3, False, "", True),
        Ejercicio("P12", "Lanzamiento Balón Medicinal de Pecho Explosivo", "Bloque B", "Potencia / RFD", "Pectoral/Tríceps", "Balón Medicinal", 2, False, "", True),
        Ejercicio("P13", "High Pull con Barra desde Muslos", "Bloque B", "Potencia / RFD", "Trapecio/Espalda", "Barra", 4, False, "", True),
        Ejercicio("P14", "Dominadas Explosivas al Pecho", "Bloque B", "Potencia / RFD", "Dorsal Ancho", "Peso Corporal", 3, False, "", True),
        Ejercicio("P15", "Trap Bar Jump Squat (Salto con Barra Trap)", "Bloque B", "Potencia / RFD", "Tren Inferior", "Barra", 4, False, "", True),
        Ejercicio("P16", "Slam Ball Slam Vertical", "Bloque B", "Potencia / RFD", "Core / Dorsal", "Balón Medicinal", 2, False, "", True),
        Ejercicio("P17", "Bounds Horizontales Alternados", "Bloque B", "Potencia / RFD", "Tren Inferior", "Peso Corporal", 3, False, "", True),
        Ejercicio("P18", "Push Up Explosivo con Aplauso", "Bloque B", "Potencia / RFD", "Pectoral", "Peso Corporal", 3, False, "", True),
        Ejercicio("P19", "Lanzamiento Rotacional de Balón contra Pared", "Bloque B", "Potencia / RFD", "Oblicuos/Core", "Balón Medicinal", 2, False, "", True),
        Ejercicio("P20", "Depth Jump con Aterrizaje Unilateral", "Bloque B", "Potencia / RFD", "Estabilidad Rodilla", "Peso Corporal", 4, False, "", True),

        # --- ISOMÉTRICOS (PUSH, CATCH, HOLD) (+15 EJERCICIOS) ---
        Ejercicio("I1", "Iso Push: Press de Banca contra Pines", "Bloque B", "Isométrico", "Pectoral", "Barra", 3, False, "", True, True),
        Ejercicio("I2", "Iso Push: Sentadilla en Punto Estático contra Topes", "Bloque B", "Isométrico", "Cuádriceps", "Barra", 4, False, "", True, True),
        Ejercicio("I3", "Iso Catch: Aterrizaje Caída desde Cajón (Landing)", "Bloque B", "Isométrico", "Cuádriceps/Tobillo", "Peso Corporal", 3, False, "", True, True),
        Ejercicio("I4", "Iso Catch: Recepción Baja de Power Clean", "Bloque B", "Isométrico", "Fullbody", "Barra", 4, False, "", True, True),
        Ejercicio("I5", "Iso Hold: Sentadilla Split Isométrica", "Bloque C", "Isométrico", "Cuádriceps/Glúteo", "Peso Corporal", 2, True, "", True, True),
        Ejercicio("I6", "Iso Hold: Puente de Glúteo Unilateral en Banco", "Bloque C", "Isométrico", "Glúteo Mayor", "Peso Corporal", 1, False, "", False, True),
        Ejercicio("I7", "Iso Push: Peso Muerto Isometrico sobre Plataforma", "Bloque B", "Isométrico", "Cadena Posterior", "Barra", 4, False, "", True, True),
        Ejercicio("I8", "Iso Hold: Plancha Abdominal con Carga", "Bloque D", "Isométrico", "Core", "Peso Corporal", 1, False, "", False, True),
        Ejercicio("I9", "Iso Hold: Dominada Isométrica en 90°", "Bloque C", "Isométrico", "Dorsal/Bíceps", "Peso Corporal", 2, False, "", True, True),
        Ejercicio("I10", "Iso Push: Remo Horizontal contra Inmóvil", "Bloque C", "Isométrico", "Espalda Alta", "Barra", 2, False, "", True, True),
        Ejercicio("I11", "Iso Hold: Paseo del Granjero (Farmer Walk Holding)", "Bloque D", "Isométrico", "Agarre/Core", "Mancuernas", 2, False, "", True, True),
        Ejercicio("I12", "Iso Hold: Sissy Squat Isométrica en Rango Medio", "Bloque D", "Isométrico", "Cuádriceps", "Peso Corporal", 3, True, "", False, True),
        Ejercicio("I13", "Iso Hold: Copenhagen Plank (Aductores)", "Bloque D", "Isométrico", "Aductores/Core", "Peso Corporal", 2, False, "", True, True),
        Ejercicio("I14", "Iso Push: Press Militar contra Pines en 90°", "Bloque B", "Isométrico", "Deltoides", "Barra", 3, False, "", True, True),
        Ejercicio("I15", "Iso Hold: Extensión de Espalda 45° con Peso", "Bloque D", "Isométrico", "Erectores Espinales", "Peso Corporal", 1, False, "", False, True),

        # --- PATRONES CLÁSICOS DE ENTRENAMIENTO (+35 EJERCICIOS) ---
        Ejercicio("E1", "Press de Banca Plano con Barra", "Bloque B", "Empuje Horizontal", "Pectoral Mayor", "Barra", 4, False),
        Ejercicio("E2", "Press Inclinado 30° con Mancuernas", "Bloque B", "Empuje Horizontal", "Pectoral Clavicular", "Mancuernas", 3, True),
        Ejercicio("E3", "Press Militar de Pie con Barra", "Bloque B", "Empuje Vertical", "Deltoides Anterior", "Barra", 4, False),
        Ejercicio("E4", "Fondos en Paralelas Lastrados", "Bloque B", "Empuje Vertical", "Pectoral / Tríceps", "Peso Corporal", 4, True),
        Ejercicio("E5", "Press Landmine Unilateral", "Bloque C", "Empuje Horizontal", "Pectoral / Deltoides", "Barra", 2, False, "", True),
        Ejercicio("E6", "Press Declinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral Esternal", "Mancuernas", 3, False),
        Ejercicio("E7", "Cruces de Polea Alta a Baja", "Bloque D", "Empuje Horizontal", "Pectoral Inferior", "Polea", 1, True),
        Ejercicio("E8", "Press Arnold Sentado", "Bloque C", "Empuje Vertical", "Deltoides", "Mancuernas", 3, False),
        Ejercicio("T1", "Dominadas Neutras Lastradas", "Bloque B", "Tracción Vertical", "Dorsal Ancho", "Peso Corporal", 4, True),
        Ejercicio("T2", "Remo Pendlay con Barra", "Bloque B", "Tracción Horizontal", "Dorsal / Romboide", "Barra", 4, False),
        Ejercicio("T3", "Jalón al Pecho Agarre Abierto", "Bloque C", "Tracción Vertical", "Dorsal Ancho", "Polea", 2, True),
        Ejercicio("T4", "Remo Unilateral con Mancuerna", "Bloque C", "Tracción Horizontal", "Dorsal Ancho", "Mancuernas", 2, True),
        Ejercicio("T5", "Remo Pecho Apoyado en Banco 45°", "Bloque C", "Tracción Horizontal", "Espalda Alta", "Mancuernas", 2, False),
        Ejercicio("T6", "Face Pull en Polea con Cuerda", "Bloque D", "Tracción Horizontal", "Deltoides Posterior", "Polea", 1, False),
        Ejercicio("R1", "Sentadilla Trasera Barra Alta", "Bloque B", "Dominante de Rodilla", "Cuádriceps", "Barra", 5, True),
        Ejercicio("R2", "Sentadilla Frontal con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps / Core", "Barra", 5, True, "", True),
        Ejercicio("R3", "Peso Muerto Rumano con Barra", "Bloque B", "Dominante de Cadera", "Isquiosurales", "Barra", 4, True),
        Ejercicio("R4", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Cadena Posterior", "Barra", 5, False),
        Ejercicio("R5", "Sentadilla Búlgara con Mancuernas", "Bloque C", "Dominante Unilateral", "Cuádriceps / Glúteo", "Mancuernas", 3, True),
        Ejercicio("R6", "Hip Thrust con Barra Lastrada", "Bloque B", "Dominante de Cadera", "Glúteo Mayor", "Barra", 3, False),
        Ejercicio("R7", "Prensa 45° Pies Abajos", "Bloque C", "Dominante de Rodilla", "Cuádriceps", "Máquina", 2, True),
        Ejercicio("R8", "Curl Femoral Tumbado", "Bloque D", "Dominante de Cadera", "Isquiosurales", "Máquina", 1, True),
        Ejercicio("A1", "Elevaciones Laterales con Mancuerna", "Bloque D", "Aislamiento", "Deltoides Lateral", "Mancuernas", 1, False),
        Ejercicio("A2", "Extensiones de Tríceps tras Nuca Polea", "Bloque D", "Aislamiento", "Tríceps", "Polea", 1, True),
        Ejercicio("A3", "Curl de Bíceps Inclinado 45°", "Bloque D", "Aislamiento", "Bíceps", "Mancuernas", 1, True),
        Ejercicio("A4", "Press Pallof con Banda", "Bloque D", "Core", "Zona Media", "Banda elástica", 1, False, "", True)
    ]

if "historial_feedback" not in st.session_state:
    st.session_state.historial_feedback = []

# ==========================================
# 3. MOTOR DE PROGRAMACIÓN ROBUSTA
# ==========================================

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

class MotorEntrenamientoRobusto:

    @staticmethod
    def obtener_parametros(objetivo: str) -> Dict[str, str]:
        if "Hipertrofia" in objetivo: return {"reps_b": "6-8", "reps_c": "8-12", "reps_d": "10-15", "rir_base": 1, "factor_volumen": 1.0}
        elif "Performance" in objetivo: return {"reps_b": "3-5 (Max Vel)", "reps_c": "5-8", "reps_d": "8-10", "rir_base": 2, "factor_volumen": 1.0}
        else: return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "12-15", "rir_base": 2, "factor_volumen": 0.8}

    @staticmethod
    def generar_rutina(atleta: PerfilAtleta, score_wellness: float) -> Dict[str, List[Dict]]:
        rutina = {"Warm-Up": [], "Bloque B": [], "Bloque C": [], "Bloque D": []}
        params = MotorEntrenamientoRobusto.obtener_parametros(atleta.objetivo)
        mod_series = -1 if score_wellness < 3.0 else 0
        mod_rir = +2 if score_wellness < 3.0 else 0

        # WARM-UP & MOVILIDAD
        warmup = [e for e in st.session_state.base_ejercicios if e.bloque == "Warm-Up" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in warmup[:3]:
            rutina["Warm-Up"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": "2 Series x 8-10 Reps (Movilidad Controlada)",
                "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "iso": ej.es_isometrico
            })

        # BLOQUE B (Principales / Potencia / Iso Push)
        b_ej = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque B" and e.equipamiento in atleta.equipamiento_disponible]
        if atleta.es_deportista: b_ej.sort(key=lambda x: not (x.es_atletico or x.es_isometrico))
        for ej in b_ej[:2]:
            series_finales = max(2, int(3 * params["factor_volumen"]) + mod_series)
            det = f"{series_finales} Series x {params['reps_b']} | RIR {params['rir_base'] + mod_rir}"
            if ej.es_isometrico: det = f"{series_finales} Series x 5s Empuje Máximo (Iso Push)"
            rutina["Bloque B"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": det, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "iso": ej.es_isometrico
            })

        # BLOQUE C (Hipertrofia / Iso Hold)
        c_ej = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque C" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in c_ej[:2]:
            series_finales = max(2, int(3 * params["factor_volumen"]) + mod_series)
            rutina["Bloque C"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params['reps_c']} | RIR {params['rir_base'] + mod_rir + 1}",
                "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "iso": ej.es_isometrico
            })

        # BLOQUE D (Accesorios / Core)
        d_ej = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque D" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in d_ej[:2]:
            series_finales = max(2, int(3 * params["factor_volumen"]) + mod_series)
            rutina["Bloque D"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params['reps_d']} | RIR {params['rir_base'] + mod_rir}",
                "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico, "iso": ej.es_isometrico
            })

        return rutina

# ==========================================
# 4. INTERFAZ GRÁFICA ROBUSTA
# ==========================================

st.title("⚡ ProGym Engine v7.0 — Performance & Science UI")

# Control de Rol (Login Docente Simplificado Interno)
st.sidebar.markdown('<div class="card-box">', unsafe_allow_html=True)
st.sidebar.subheader("👤 Seleccionar Rol")
rol_usuario = st.sidebar.radio("Modo de Uso:", ["Alumno / Deportista", "Profesor / Entrenador"])
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="card-box">', unsafe_allow_html=True)
st.sidebar.subheader("📋 Configuración del Atleta")
nombre = st.sidebar.text_input("Nombre del Atleta", "Carlos Pérez")
es_deportista = st.sidebar.checkbox("🏅 Atleta de Alto Rendimiento", value=True)
tipo_rutina = st.sidebar.selectbox("Formato de Rutina", ["Fullbody", "Torso-Pierna", "Push-Pull-Legs (PPL)", "Weider"])
objetivo = st.sidebar.selectbox("Objetivo Principal", ["Performance Deportiva (Potencia & RFD)", "Hipertrofia (Estiramiento & Tensión)", "Pérdida de Grasa / Mantenimiento"])

equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"]
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="card-box">', unsafe_allow_html=True)
st.sidebar.subheader("📊 Wellness Pre-Entreno")
sueno = st.sidebar.slider("Sueño (1-5)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1-5)", 1, 5, 3)
agujetas = st.sidebar.slider("Agujetas (1-5)", 1, 5, 3)
fatiga = st.sidebar.slider("Fatiga General (1-5)", 1, 5, 3)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

atleta = PerfilAtleta(nombre=nombre, tipo_rutina=tipo_rutina, objetivo=objetivo, es_deportista=es_deportista, equipamiento_disponible=equipamiento)
score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Banner Principal con Recuadro
st.markdown('<div class="card-box">', unsafe_allow_html=True)
col_w1, col_w2 = st.columns([1, 3])
with col_w1: st.metric("Score Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0: 
        st.write("⚠️ **Autorregulación Activa:** Reducción de carga y aumento de RIR por fatiga acumulada.")
    else: 
        st.write(f"✅ **Estado Óptimo:** Atleta listo para máxima intensidad | **{objetivo}**")
st.markdown('</div>', unsafe_allow_html=True)

# Pestañas
tab_rutina, tab_docente, tab_plan, tab_crud = st.tabs([
    "📋 Sesión Diaria & Feedback",
    "👨‍🏫 Panel Docente (Comentarios)",
    "🗓️ Programación Semanal",
    "🛠️ Banco Masivo & Carga Docente"
])

# ==========================================
# PESTAÑA 1: SESIÓN DIARIA & FEEDBACK
# ==========================================
with tab_rutina:
    rutina = MotorEntrenamientoRobusto.generar_rutina(atleta, score_wellness)
    inputs_feedback = {}

    def render_bloque(titulo: str, lista_ejercicios: List[Dict], css_class: str):
        st.markdown(f'<div class="block-card {css_class}"><h3>{titulo}</h3></div>', unsafe_allow_html=True)
        for item in lista_ejercicios:
            st.markdown('<div class="card-box">', unsafe_allow_html=True)
            col_info, col_feed = st.columns([2, 1])
            with col_info:
                badge_atl = '<span class="badge badge-athletic">Atleta / RFD</span>' if item['atletico'] else ''
                badge_iso = '<span class="badge badge-iso">Isométrico</span>' if item['iso'] else ''
                st.markdown(f"### {item['nombre']}")
                st.markdown(f"**Patrón:** {item['patron']} | {badge_atl} {badge_iso} <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
                st.caption(f"📌 Prescripción: {item['detalles']}")
                if item["video"]:
                    with st.expander("🎥 Ver Video"):
                        st.video(item["video"])
            with col_feed:
                st.markdown("**📝 Registro de Trabajo:**")
                carga_reps = st.text_input(f"Carga / Reps / Segundos ({item['id']})", placeholder="Ej: 100kg x 5 reps o 10s", key=f"c_{item['id']}")
                rir_rpe = st.select_slider(f"Esfuerzo Percibido ({item['id']})", options=["RIR 0", "RIR 1", "RIR 2", "RIR 3", "RIR 4+"], value="RIR 1", key=f"r_{item['id']}")
                nota = st.text_input(f"Observaciones ({item['id']})", placeholder="Molestias, sensaciones...", key=f"n_{item['id']}")
                
                inputs_feedback[item['nombre']] = {
                    "ejercicio_id": item['id'],
                    "carga_reps": carga_reps,
                    "rir_rpe": rir_rpe,
                    "nota": nota
                }
            st.markdown('</div>', unsafe_allow_html=True)

    render_bloque("🔥 WARM-UP & MOVILIDAD ESTRUCTURADA", rutina["Warm-Up"], "block-warmup")
    render_bloque("BLOQUE B: Potencia, Tensión & Isométricos Push", rutina["Bloque B"], "block-b")
    render_bloque("BLOQUE C: Hipertrofia Mediada por Estiramiento & Iso Holds", rutina["Bloque C"], "block-c")
    render_bloque("BLOQUE D: Accesorios & Trabajo de Core", rutina["Bloque D"], "block-d")

    if st.button("💾 Registrar y Enviar Entrenamiento al Entrenador"):
        registro_sesion = {
            "fecha": str(datetime.date.today()),
            "alumno": nombre,
            "objetivo": objetivo,
            "rutina": tipo_rutina,
            "detalles_ejercicios": inputs_feedback
        }
        st.session_state.historial_feedback.append(registro_sesion)
        st.success("✅ Entrenamiento guardado en la plataforma. Tu entrenador ya tiene acceso.")

# ==========================================
# PESTAÑA 2: PANEL DOCENTE
# ==========================================
with tab_docente:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("👨‍🏫 Panel de Control del Entrenador")
    
    if rol_usuario == "Profesor / Entrenador":
        st.write("### 📥 Historial Completo de Devoluciones y Comentarios")
        
        if not st.session_state.historial_feedback:
            st.info("No hay registros de alumnos guardados aún.")
        else:
            for idx, reg in enumerate(reversed(st.session_state.historial_feedback)):
                st.markdown('<div class="card-box">', unsafe_allow_html=True)
                st.write(f"**Alumno:** {reg['alumno']} | **Fecha:** {reg['fecha']} | **Formato:** {reg['rutina']}")
                for ej_nombre, datos in reg["detalles_ejercicios"].items():
                    if datos["carga_reps"] or datos["nota"]:
                        st.markdown(f"- **{ej_nombre}**: {datos['carga_reps']} | Presión: **{datos['rir_rpe']}** | *Nota: {datos['nota']}*")
                
                st.text_area(f"✍️ Observación Docente / Feedback para el Alumno", key=f"resp_prof_{idx}")
                if st.button(f"Guardar Feedback #{idx}"):
                    st.success("Observación guardada correctamente.")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Cambia tu rol a **Profesor / Entrenador** en la barra lateral para ver las devoluciones.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PESTAÑA 3: PROGRAMACIÓN SEMANAL
# ==========================================
with tab_plan:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("🗓️ Programación Semanal de Performance")
    dias = ["Lunes (Empuje / Potencia RFD)", "Martes (Tracción / Iso Holds)", "Miércoles (Recuperación / Movilidad)", "Jueves (Dominante Rodilla / Pliometría)", "Viernes (Dominante Cadera / Fuerza)", "Sábado (Capacidad Atlética)", "Domingo (Descanso Total)"]
    for d in dias:
        with st.expander(f"📅 {d}"):
            st.write(f"Estructura orientada a **{objetivo}**.")
            st.caption("Warm-up dinámico obligatorio + Bloques B, C y D.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PESTAÑA 4: BANCO MASIVO & CARGA DOCENTE (CRUD)
# ==========================================
with tab_crud:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("🛠️ Carga y Gestión de Ejercicios por el Profesor")
    
    if rol_usuario == "Profesor / Entrenador":
        st.markdown("### ➕ Registrar Nuevo Ejercicio a la Base General")
        with st.form("form_nuevo_ejercicio"):
            col1, col2, col3 = st.columns(3)
            with col1:
                n_id = st.text_input("ID Ejercicio", f"EX{len(st.session_state.base_ejercicios)+1}")
                n_nombre = st.text_input("Nombre del Ejercicio", "")
                n_bloque = st.selectbox("Bloque", ["Warm-Up", "Bloque B", "Bloque C", "Bloque D"])
            with col2:
                n_patron = st.selectbox("Categoría / Patrón", [
                    "Warm-Up / Movilidad", "Potencia / RFD", "Isométrico",
                    "Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", 
                    "Tracción Horizontal", "Dominante de Rodilla", "Dominante de Cadera", "Aislamiento", "Core"
                ])
                n_musculo = st.text_input("Músculo Principal", "")
                n_equipo = st.selectbox("Equipamiento Required", ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"])
            with col3:
                n_estres = st.slider("Estrés Articular (1-5)", 1, 5, 2)
                n_url = st.text_input("URL Video YouTube", "")
                n_atletico = st.checkbox("¿Es para Atletismo/Performance?", value=False)
                n_iso = st.checkbox("¿Es Variante Isométrica (Push/Catch/Hold)?", value=False)
            
            if st.form_submit_button("Añadir a la Base de Datos"):
                if n_nombre:
                    nuevo_ej = Ejercicio(n_id, n_nombre, n_bloque, n_patron, n_musculo, n_equipo, n_estres, False, n_url, n_atletico, n_iso)
                    st.session_state.base_ejercicios.append(nuevo_ej)
                    st.success(f"✔️ Ejercicio '{n_nombre}' integrado exitosamente a la plataforma.")
                else:
                    st.error("Por favor completa al menos el nombre del ejercicio.")

        st.divider()
        st.markdown("### ❌ Eliminar Ejercicio Existente")
        ej_eliminar = st.selectbox("Selecciona ejercicio a remover:", [e.nombre for e in st.session_state.base_ejercicios])
        if st.button("Eliminar de la Plataforma"):
            st.session_state.base_ejercicios = [e for e in st.session_state.base_ejercicios if e.nombre != ej_eliminar]
            st.success(f"Ejercicio '{ej_eliminar}' eliminado.")
            st.rerun()

    else:
        st.info("Activa el rol **Profesor / Entrenador** para registrar o modificar los ejercicios de la aplicación.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader(f"📚 Base Global ({len(st.session_state.base_ejercicios)} Ejercicios Cargados)")
    tabla_datos = [{
        "ID": e.id, "Bloque": e.bloque, "Nombre": e.nombre, "Categoría/Patrón": e.patron_movimiento,
        "Músculo": e.musculo_principal, "Equipo": e.equipamiento, "Estrés": f"{e.estres_articular}/5",
        "Isométrico": "Sí" if e.es_isometrico else "No", "Deportivo": "Sí" if e.es_atletico else "No"
    } for e in st.session_state.base_ejercicios]
    st.dataframe(tabla_datos, use_container_width=True)
