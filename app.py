import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y ESTILOS (NEGRO-AZUL-VERDE)
# ==========================================

st.set_page_config(page_title="ProGym Engine v5.0", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
<style>
    /* Fondo principal y estructura */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Sidebars */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1e293b;
    }

    /* Tarjetas de Bloque de Entrenamiento */
    .block-card {
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        border-left: 6px solid #10b981;
        background-color: #1e293b;
        color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .block-warmup { border-left-color: #10b981; background-color: #064e3b; }
    .block-b { border-left-color: #2563eb; background-color: #1e3a8a; }
    .block-c { border-left-color: #0284c7; background-color: #0c4a6e; }
    .block-d { border-left-color: #059669; background-color: #065f46; }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.3em 0.7em;
        font-size: 78%;
        font-weight: 700;
        border-radius: 0.3rem;
        margin-right: 6px;
        color: #ffffff;
    }
    .badge-stress { background-color: #d97706; }
    .badge-equip { background-color: #2563eb; }
    .badge-athletic { background-color: #10b981; }

    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #10b981 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODELOS DE DATOS Y ESTADO GLOBAL (PERSISTENCIA)
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    bloque: str  # Warm-Up, Bloque B, Bloque C, Bloque D
    patron_movimiento: str
    musculo_principal: str
    equipamiento: str
    estres_articular: int  # 1 a 5
    url_video: str = ""
    es_atletico: bool = False

# Inicializar Base de Datos Persistente en Session State
if "base_ejercicios" not in st.session_state:
    st.session_state.base_ejercicios = [
        # --- WARM-UP & MOVILIDAD OBLIGATORIO (10 Ejercicios) ---
        Ejercicio("W1", "Gato-Camello (Cat-Cow)", "Warm-Up", "Movilidad Columna", "Zona Media", "Peso Corporal", 1, "https://www.youtube.com/watch?v=kqnua4rHVVA"),
        Ejercicio("W2", "World's Greatest Stretch", "Warm-Up", "Movilidad Cadera", "Cadera/Isquios", "Peso Corporal", 1, "https://www.youtube.com/watch?v=vV1p24vLuh4"),
        Ejercicio("W3", "Dislocaciones de Hombro con Banda", "Warm-Up", "Movilidad Hombros", "Manguito Rotador", "Banda elástica", 1, "https://www.youtube.com/watch?v=33P5AI27eiU"),
        Ejercicio("W4", "Rotación Torácica Quadrupedal", "Warm-Up", "Movilidad Torácica", "Espalda Alta", "Peso Corporal", 1, "https://www.youtube.com/watch?v=d_kXpW_QpNA"),
        Ejercicio("W5", "Saltos Pliométricos al Cajón", "Warm-Up", "Potencia / Pliometría", "Tren Inferior", "Peso Corporal", 2, "https://www.youtube.com/watch?v=52r_Ul5k03g", es_atletico=True),
        Ejercicio("W6", "Paseo de Oso (Bear Crawl)", "Warm-Up", "Activación Core", "Core / Hombros", "Peso Corporal", 1, "https://www.youtube.com/watch?v=f-BuhL0_B8A", es_atletico=True),
        Ejercicio("W7", "Movilidad de Tobillo en Pared", "Warm-Up", "Movilidad Tobillo", "Gemelos/Sóleo", "Peso Corporal", 1, ""),
        Ejercicio("W8", "Caminata de Gusano (Inchworm)", "Warm-Up", "Movilidad Cadena Posterior", "Isquios/Core", "Peso Corporal", 1, ""),
        Ejercicio("W9", "Lanzamiento Balón Medicinal Medial", "Warm-Up", "Potencia / Pliometría", "Core/Rotadores", "Balón Medicinal", 2, "", es_atletico=True),
        Ejercicio("W10", "Aductores en Posición Roca", "Warm-Up", "Movilidad Cadera", "Aductores", "Peso Corporal", 1, ""),

        # --- EMPUJE HORIZONTAL & VERTICAL (10 Ejercicios) ---
        Ejercicio("E1", "Press de Banca con Barra", "Bloque B", "Empuje Horizontal", "Pectoral", "Barra", 4, "https://www.youtube.com/watch?v=rT7DgCr-3pg"),
        Ejercicio("E2", "Press Militar con Barra", "Bloque B", "Empuje Vertical", "Deltoides", "Barra", 4, "https://www.youtube.com/watch?v=2yjwXTZQDDI"),
        Ejercicio("E3", "Press Inclinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral Superior", "Mancuernas", 3, "https://www.youtube.com/watch?v=8iPEnn-ltC8"),
        Ejercicio("E4", "Press Arnold con Mancuernas", "Bloque C", "Empuje Vertical", "Deltoides", "Mancuernas", 3, ""),
        Ejercicio("E5", "Fondos en Paralelas Lastrados", "Bloque B", "Empuje Vertical", "Pectoral / Tríceps", "Peso Corporal", 4, ""),
        Ejercicio("E6", "Press Push Press de Potencia", "Bloque B", "Empuje Vertical", "Deltoides / Potencia", "Barra", 5, "", es_atletico=True),
        Ejercicio("E7", "Flexiones de Brazo con Lastre", "Bloque C", "Empuje Horizontal", "Pectoral", "Peso Corporal", 2),
        Ejercicio("E8", "Press Landmine Unilateral", "Bloque C", "Empuje Unilateral", "Deltoides / Pectoral", "Barra", 2, "", es_atletico=True),
        Ejercicio("E9", "Press Declinado con Barra", "Bloque B", "Empuje Horizontal", "Pectoral Inferior", "Barra", 4, ""),
        Ejercicio("E10", "Press de Pecho en Máquina Hammer", "Bloque C", "Empuje Horizontal", "Pectoral", "Máquina", 2, ""),

        # --- TRACCIÓN HORIZONTAL & VERTICAL (10 Ejercicios) ---
        Ejercicio("T1", "Dominadas Prona Lastradas", "Bloque B", "Tracción Vertical", "Dorsal Ancho", "Peso Corporal", 4, "https://www.youtube.com/watch?v=eGo4IYlbE5g"),
        Ejercicio("T2", "Remo con Barra Pendlay", "Bloque B", "Tracción Horizontal", "Dorsal / Romboide", "Barra", 4, ""),
        Ejercicio("T3", "Jalón al Pecho Agarre Neutro", "Bloque C", "Tracción Vertical", "Dorsal", "Polea", 2, "https://www.youtube.com/watch?v=CAwf7n6Luuc"),
        Ejercicio("T4", "Remo Unilateral con Mancuerna", "Bloque C", "Tracción Horizontal", "Dorsal", "Mancuernas", 2, ""),
        Ejercicio("T5", "Remo en Banco Inclinado con Mancuernas", "Bloque C", "Tracción Horizontal", "Romboide", "Mancuernas", 2, ""),
        Ejercicio("T6", "Dominadas Neutras Explosivas", "Bloque B", "Tracción Vertical", "Dorsal", "Peso Corporal", 3, "", es_atletico=True),
        Ejercicio("T7", "Jalón Brazo Recto en Polea", "Bloque D", "Tracción Vertical", "Dorsal Ancho", "Polea", 1, ""),
        Ejercicio("T8", "Remo Gironda en Polea Baja", "Bloque C", "Tracción Horizontal", "Espalda Media", "Polea", 2, ""),
        Ejercicio("T9", "Remo Kroc a Altas Repeticiones", "Bloque C", "Tracción Horizontal", "Dorsal / Agarre", "Mancuernas", 3, "", es_atletico=True),
        Ejercicio("T10", "Face Pull con Cuerda en Polea", "Bloque D", "Salud Articular", "Deltoides Post / Rotadores", "Polea", 1, "https://www.youtube.com/watch?v=rep-qVOkqgk"),

        # --- DOMINANTE DE RODILLA (10 Ejercicios) ---
        Ejercicio("R1", "Sentadilla Trasera con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps", "Barra", 5, "https://www.youtube.com/watch?v=ultWZbUMPL8"),
        Ejercicio("R2", "Sentadilla Frontal con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps / Core", "Barra", 5, "", es_atletico=True),
        Ejercicio("R3", "Prensa de Piernas 45°", "Bloque C", "Dominante de Rodilla", "Cuádriceps", "Máquina", 2, "https://www.youtube.com/watch?v=IZxyjW7MPJQ"),
        Ejercicio("R4", "Zancadas Búlgaras con Mancuernas", "Bloque C", "Dominante Unilateral", "Cuádriceps / Glúteo", "Mancuernas", 3, "", es_atletico=True),
        Ejercicio("R5", "Sentadilla Hack en Máquina", "Bloque B", "Dominante de Rodilla", "Cuádriceps", "Máquina", 3, ""),
        Ejercicio("R6", "Extensiones de Cuádriceps en Sillón", "Bloque D", "Aislamiento", "Cuádriceps", "Máquina", 1, ""),
        Ejercicio("R7", "Sentadilla Goblet con Mancuerna", "Bloque C", "Dominante de Rodilla", "Cuádriceps", "Mancuernas", 2, ""),
        Ejercicio("R8", "Zancadas Caminando con Barra", "Bloque C", "Dominante Unilateral", "Cuádriceps", "Barra", 3, ""),
        Ejercicio("R9", "Paso al Cajón (Step-Up) Explosivo", "Bloque C", "Dominante Unilateral", "Cuádriceps", "Mancuernas", 3, "", es_atletico=True),
        Ejercicio("R10", "Sentadilla Sissy Peso Corporal", "Bloque D", "Aislamiento", "Cuádriceps", "Peso Corporal", 3, ""),

        # --- DOMINANTE DE CADERA & POTENCIA (10 Ejercicios) ---
        Ejercicio("C1", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Isquiosurales / Glúteo", "Barra", 5, "https://www.youtube.com/watch?v=op9kVnSso6Q"),
        Ejercicio("C2", "Peso Muerto Rumano con Mancuernas", "Bloque C", "Dominante de Cadera", "Isquiosurales", "Mancuernas", 3, "https://www.youtube.com/watch?v=JCXUYuzwNrM"),
        Ejercicio("C3", "Hip Thrust con Barra", "Bloque B", "Dominante de Cadera", "Glúteo Mayor", "Barra", 3, ""),
        Ejercicio("C4", "Power Clean (Cargada de Potencia)", "Bloque B", "Potencia Olímipica", "Cadena Posterior", "Barra", 5, "", es_atletico=True),
        Ejercicio("C5", "Curl Femoral Tumbado en Máquina", "Bloque D", "Aislamiento", "Isquiosurales", "Máquina", 1, ""),
        Ejercicio("C6", "Peso Muerto Sumo", "Bloque B", "Dominante de Cadera", "Glúteo / Adusto", "Barra", 4, ""),
        Ejercicio("C7", "Swings con Pesa Rusa (Kettlebell)", "Bloque C", "Potencia Cadera", "Cadena Posterior", "Mancuernas", 2, "", es_atletico=True),
        Ejercicio("C8", "Buenos Días con Barra", "Bloque C", "Dominante de Cadera", "Espalda Baja / Isquios", "Barra", 3, ""),
        Ejercicio("C9", "Curl Nordico de Isquios", "Bloque D", "Aislamiento Excéntrico", "Isquiosurales", "Peso Corporal", 4, "", es_atletico=True),
        Ejercicio("C10", "Extensiones de Cadera en Banco 45°", "Bloque D", "Dominante de Cadera", "Glúteo / Erector", "Peso Corporal", 1, ""),

        # --- AISLAMIENTO & CORE (10 Ejercicios) ---
        Ejercicio("A1", "Elevaciones Laterales con Mancuerna", "Bloque D", "Aislamiento", "Deltoides Lateral", "Mancuernas", 1, "https://www.youtube.com/watch?v=3VcKaXpzqRo"),
        Ejercicio("A2", "Extensiones de Tríceps Polea Alta", "Bloque D", "Aislamiento", "Tríceps", "Polea", 1, "https://www.youtube.com/watch?v=vB5OHsJ3EME"),
        Ejercicio("A3", "Curl de Bíceps Inclinado con Mancuernas", "Bloque D", "Aislamiento", "Bíceps", "Mancuernas", 1, "https://www.youtube.com/watch?v=soxrZlIl35U"),
        Ejercicio("A4", "Rueda Abdominal (Ab Wheel)", "Bloque D", "Core Anti-Extensión", "Zona Media", "Peso Corporal", 3, "", es_atletico=True),
        Ejercicio("A5", "Press Pallof con Banda", "Bloque D", "Core Anti-Rotación", "Zona Media / Oblicuos", "Banda elástica", 1, "", es_atletico=True),
        Ejercicio("A6", "Curl de Bíceps Martillo", "Bloque D", "Aislamiento", "Braquial / Bíceps", "Mancuernas", 1, ""),
        Ejercicio("A7", "Press Francés con Barra Z", "Bloque D", "Aislamiento", "Tríceps", "Barra", 2, ""),
        Ejercicio("A8", "Elevaciones de Talones de Pie", "Bloque D", "Aislamiento", "Gemelos", "Máquina", 1, ""),
        Ejercicio("A9", "Pájaro / Pájaros en Polea", "Bloque D", "Aislamiento", "Deltoides Posterior", "Polea", 1, ""),
        Ejercicio("A10", "Plancha Abdominal Isometrica con Carga", "Bloque D", "Core", "Zona Media", "Peso Corporal", 1, "")
    ]

# Historial de Feedback de Alumnos
if "historial_feedback" not in st.session_state:
    st.session_state.historial_feedback = []

# Autenticación Docente
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
# 3. MOTOR Y LÓGICA DE NEGOCIO
# ==========================================

class MotorEntrenamiento:

    @staticmethod
    def obtener_parametros_objetivo(objetivo: str) -> Dict[str, str]:
        if objetivo == "Hipertrofia": return {"reps_b": "6-10", "reps_c": "8-12", "reps_d": "12-15", "rir_base": 1, "factor_volumen": 1.0}
        elif objetivo == "Pérdida de Grasa / Definición": return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "12-15", "rir_base": 1, "factor_volumen": 0.85}
        elif objetivo == "Rendimiento Deportivo / Performance": return {"reps_b": "3-5 (Explosivas)", "reps_c": "6-8", "reps_d": "8-10", "rir_base": 2, "factor_volumen": 1.0}
        else: return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "10-12", "rir_base": 2, "factor_volumen": 0.7}

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
        candidatos.sort(key=lambda x: x.estres_articular)
        return candidatos[0] if candidatos else None

    @staticmethod
    def generar_rutina_completa(atleta: PerfilAtleta, sub_dia: str, score_wellness: float) -> Dict[str, List[Dict]]:
        rutina_bloques = {"Warm-Up": [], "Bloque B": [], "Bloque C": [], "Bloque D": []}
        params_obj = MotorEntrenamiento.obtener_parametros_objetivo(atleta.objetivo)
        mod_series = -1 if score_wellness < 3.0 else 0
        mod_rir = +2 if score_wellness < 3.0 else 0
        patrones_sesion = MotorEntrenamiento.filtrar_patrones_por_rutina(atleta.tipo_rutina, sub_dia)

        # WARM-UP OBLIGATORIO
        warmup = [e for e in st.session_state.base_ejercicios if e.bloque == "Warm-Up" and e.equipamiento in atleta.equipamiento_disponible]
        if atleta.es_deportista: warmup.sort(key=lambda x: not x.es_atletico)
        for ej in warmup[:3]:
            rutina_bloques["Warm-Up"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": "2 Series x 10 Reps (Movilidad / Activación)",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico
            })

        # BLOQUE B
        principales = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque B" and (e.patron_movimiento in patrones_sesion or (atleta.es_deportista and e.es_atletico)) and e.equipamiento in atleta.equipamiento_disponible]
        for ej in principales[:2]:
            series = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque B"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_b']} Reps | RIR Prescripto: {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico
            })

        # BLOQUE C
        secundarios = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque C" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in secundarios[:2]:
            series_finales = max(2, int(3 * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque C"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_c']} Reps | RIR Prescripto: {params_obj['rir_base'] + mod_rir + 1}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico
            })

        # BLOQUE D
        accesorios = [e for e in st.session_state.base_ejercicios if e.bloque == "Bloque D" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in accesorios[:2]:
            series_acc = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series_acc * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque D"].append({
                "id": ej.id, "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_d']} Reps | RIR Prescripto: {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "video": ej.url_video, "atletico": ej.es_atletico
            })

        return rutina_bloques

# ==========================================
# 4. INTERFAZ GRÁFICA Y CONTROL DE ACCESO
# ==========================================

st.title("🏋️ ProGym Engine v5.0 — Control Total & Feedback")

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
es_deportista = st.sidebar.checkbox("🏅 Perfil Deportivo de Alto Rendimiento", value=False)
tipo_rutina = st.sidebar.selectbox("Modalidad de Rutina", ["Fullbody", "Torso-Pierna", "Push-Pull-Legs (PPL)", "Weider"])
objetivo = st.sidebar.selectbox("Objetivo", ["Hipertrofia", "Pérdida de Grasa / Definición", "Rendimiento Deportivo / Performance", "Mantenimiento / Salud"])
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral", "Cuádriceps", "Dorsal", "Deltoides", "Isquiosurales"])

equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"]
)

st.sidebar.divider()
st.sidebar.header("📊 Wellness Pre-Entreno")
sueno = st.sidebar.slider("Sueño (1 Bad - 5 Top)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1 Alto - 5 Bajo)", 1, 5, 3)
agujetas = st.sidebar.slider("Agujetas (1 Alto - 5 Bajo)", 1, 5, 3)
fatiga = st.sidebar.slider("Fatiga General (1 Alto - 5 Bajo)", 1, 5, 3)

atleta = PerfilAtleta(nombre=nombre, tipo_rutina=tipo_rutina, objetivo=objetivo, es_deportista=es_deportista, musculo_especializacion=especializacion, equipamiento_disponible=equipamiento)
score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Banner Principal
col_w1, col_w2 = st.columns([1, 3])
with col_w1: st.metric("Score Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0: st.error("⚠️ **Autorregulación por Fatiga:** Se reduce volumen (-1 serie) e intensidad (+2 RIR).")
    else: st.success(f"✅ Estado Óptimo | Objetivo: **{objetivo}** | Formato: **{tipo_rutina}**")

st.divider()

# Pestañas de la Aplicación
tab_rutina, tab_docente, tab_plan, tab_crud, tab_remplazo = st.tabs([
    "📋 Sesión Diaria & Feedback",
    "👨‍🏫 Panel Docente (Comentarios)",
    "🗓️ Planificación Semanal/Mensual",
    "🛠️ Banco de Ejercicios (CRUD)",
    "🔄 Sustitución Rápida"
])

# ==========================================
# PESTAÑA 1: SESIÓN DIARIA Y FEEDBACK ALUMNO
# ==========================================
with tab_rutina:
    sub_dia = "General"
    if tipo_rutina == "Torso-Pierna": sub_dia = st.radio("Día:", ["Torso", "Pierna"], horizontal=True)
    elif tipo_rutina == "Push-Pull-Legs (PPL)": sub_dia = st.radio("Día:", ["Push (Empuje)", "Pull (Tracción)", "Legs (Pierna)"], horizontal=True)

    rutina = MotorEntrenamiento.generar_rutina_completa(atleta, sub_dia, score_wellness)
    
    inputs_feedback = {}

    def render_bloque(titulo: str, lista_ejercicios: List[Dict], css_class: str):
        st.markdown(f'<div class="block-card {css_class}"><h3>{titulo}</h3></div>', unsafe_allow_html=True)
        for item in lista_ejercicios:
            col_info, col_feed = st.columns([2, 1])
            with col_info:
                st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
                st.caption(f"📌 {item['detalles']}")
                if item["video"]:
                    with st.expander("🎥 Ver Video Técnico"):
                        st.video(item["video"])
            with col_feed:
                st.markdown("**📝 Registro de Trabajo Real:**")
                carga_reps = st.text_input(f"Carga / Reps ({item['id']})", placeholder="Ej: 80kg x 8", key=f"c_{item['id']}")
                rir_rpe = st.select_slider(f"RIR Percibido ({item['id']})", options=["RIR 0 (Fallo)", "RIR 1", "RIR 2", "RIR 3", "RIR 4+"], value="RIR 1", key=f"r_{item['id']}")
                nota = st.text_input(f"Notas ({item['id']})", placeholder="Molestia, sensación...", key=f"n_{item['id']}")
                
                inputs_feedback[item['nombre']] = {
                    "ejercicio_id": item['id'],
                    "carga_reps": carga_reps,
                    "rir_rpe": rir_rpe,
                    "nota": nota
                }
            st.divider()

    render_bloque("🔥 WARM-UP & MOVILIDAD (OBLIGATORIO)", rutina["Warm-Up"], "block-warmup")
    render_bloque("BLOQUE B: Ejercicios Principales / Potencia", rutina["Bloque B"], "block-b")
    render_bloque("BLOQUE C: Ejercicios Secundarios", rutina["Bloque C"], "block-c")
    render_bloque("BLOQUE D: Accesorios & Salud Articular", rutina["Bloque D"], "block-d")

    if st.button("💾 Enviar Feedback de la Sesión al Profesor", type="primary"):
        registro_sesion = {
            "fecha": str(datetime.date.today()),
            "alumno": nombre,
            "objetivo": objetivo,
            "rutina": tipo_rutina,
            "detalles_ejercicios": inputs_feedback
        }
        st.session_state.historial_feedback.append(registro_sesion)
        st.success("✅ Feedback enviado con éxito. Su profesor ya puede visualizarlo en su panel de control.")

# ==========================================
# PESTAÑA 2: PANEL DOCENTE (VISTA COMPLETA Y COMENTARIOS)
# ==========================================
with tab_docente:
    st.subheader("👨‍🏫 Panel de Control del Entrenador")
    
    if rol_usuario == "Profesor / Entrenador" and st.session_state.profesor_autenticado:
        st.write("### 📥 Historial de Feedback y Comentarios de Alumnos")
        
        if not st.session_state.historial_feedback:
            st.info("Aún no hay registros enviadas por los alumnos en la sesión actual.")
        else:
            for idx, reg in enumerate(reversed(st.session_state.historial_feedback)):
                with st.expander(f"👤 Alumno: {reg['alumno']} | Fecha: {reg['fecha']} | {reg['rutina']} ({reg['objetivo']})"):
                    st.write(f"**Detalles del Registro:**")
                    for ej_nombre, datos in reg["detalles_ejercicios"].items():
                        if datos["carga_reps"] or datos["nota"]:
                            st.markdown(f"- **{ej_nombre}**: {datos['carga_reps']} | Presión: **{datos['rir_rpe']}** | *Observación: {datos['nota']}*")
                    
                    st.text_area(f"✍️ Responder u Ajustar Observación (Profesor)", key=f"resp_prof_{idx}")
                    if st.button(f"Guardar Ajuste #{idx}"):
                        st.success("Ajuste guardado correctamente.")
    else:
        st.warning("🔒 Esta sección es exclusiva para el **Profesor**. Activa el rol de Profesor e ingresa la contraseña en la barra lateral.")

# ==========================================
# PESTAÑA 3: PLANIFICACIÓN SEMANAL / MENSUAL
# ==========================================
with tab_plan:
    st.subheader("🗓️ Planificación del Mesociclo")
    vista_plan = st.radio("Vista de Planificación", ["Vista Semanal (Microciclo)", "Vista Mensual (Mesociclo)"], horizontal=True)

    if vista_plan == "Vista Semanal (Microciclo)":
        st.markdown("### Distribución Semanal")
        dias = ["Lunes (Día 1)", "Martes (Día 2)", "Miércoles (Descanso/Recuperación)", "Jueves (Día 3)", "Viernes (Día 4)", "Sábado (Trabajo Activo/Cardio)", "Domingo (Descanso Total)"]
        for d in dias:
            with st.expander(f"📅 {d}"):
                st.write(f"Plan estructurado según esquema **{tipo_rutina}**.")
                st.caption("Warm-up obligatorio pre-sesión + Bloques B, C y D.")
    else:
        st.markdown("### Programación del Mesociclo (4 Semanas)")
        prog_mensual = [
            {"Semana": "Semana 1", "Fase": "Acumulación / Introducción", "Volumen": "100%", "Intensidad Prescripta": "RIR 2-3"},
            {"Semana": "Semana 2", "Fase": "Carga Principal", "Volumen": "110%", "Intensidad Prescripta": "RIR 1-2"},
            {"Semana": "Semana 3", "Fase": "Pico de Intensidad", "Volumen": "120%", "Intensidad Prescripta": "RIR 0-1"},
            {"Semana": "Semana 4", "Fase": "Descarga / Autorregulación", "Volumen": "50%", "Intensidad Prescripta": "RIR 3-4"},
        ]
        st.table(prog_mensual)

# ==========================================
# PESTAÑA 4: BANCO DE EJERCICIOS (CRUD PROFESOR)
# ==========================================
with tab_crud:
    st.subheader("🛠️ Gestión de Base de Datos de Ejercicios")
    
    if rol_usuario == "Profesor / Entrenador" and st.session_state.profesor_autenticado:
        st.markdown("### ➕ Agregar Nuevo Ejercicio")
        with st.form("form_nuevo_ejercicio"):
            col1, col2, col3 = st.columns(3)
            with col1:
                n_id = st.text_input("ID Ejercicio", f"EX{len(st.session_state.base_ejercicios)+1}")
                n_nombre = st.text_input("Nombre del Ejercicio", "")
                n_bloque = st.selectbox("Bloque", ["Warm-Up", "Bloque B", "Bloque C", "Bloque D"])
            with col2:
                n_patron = st.selectbox("Patrón de Movimiento", ["Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", "Tracción Horizontal", "Dominante de Rodilla", "Dominante de Cadera", "Movilidad Cadera", "Movilidad Hombros", "Aislamiento", "Core"])
                n_musculo = st.text_input("Músculo Principal", "")
                n_equipo = st.selectbox("Equipamiento Required", ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica", "Balón Medicinal"])
            with col3:
                n_estres = st.slider("Estrés Articular (1-5)", 1, 5, 2)
                n_url = st.text_input("URL Video YouTube", "")
                n_atletico = st.checkbox("¿Ejercicio para Deportistas?", value=False)
            
            if st.form_submit_button("Guardar en Base de Datos"):
                if n_nombre:
                    nuevo_ej = Ejercicio(n_id, n_nombre, n_bloque, n_patron, n_musculo, n_equipo, n_estres, n_url, n_atletico)
                    st.session_state.base_ejercicios.append(nuevo_ej)
                    st.success(f"✔️ Ejercicio '{n_nombre}' guardado exitosamente.")
                else:
                    st.error("Ingrese al menos el nombre del ejercicio.")

        st.divider()
        st.markdown("### ❌ Eliminar Ejercicio")
        ej_eliminar = st.selectbox("Selecciona ejercicio a eliminar:", [e.nombre for e in st.session_state.base_ejercicios])
        if st.button("Eliminar Ejercicio Seleccionado"):
            st.session_state.base_ejercicios = [e for e in st.session_state.base_ejercicios if e.nombre != ej_eliminar]
            st.success(f"Ejercicio '{ej_eliminar}' eliminado de la base de datos.")
            st.rerun()

    else:
        st.warning("🔒 El banco de datos editable requiere permisos de **Profesor** (autenticado con clave `1234`).")

    # Tabla Informativa de la Base
    st.subheader(f"📚 Catálogo Completo ({len(st.session_state.base_ejercicios)} Ejercicios Disponibles)")
    tabla_datos = [{
        "ID": e.id, "Bloque": e.bloque, "Nombre": e.nombre, "Patrón": e.patron_movimiento,
        "Músculo": e.musculo_principal, "Equipo": e.equipamiento, "Estrés": f"{e.estres_articular}/5", "Deportivo": "Sí" if e.es_atletico else "No"
    } for e in st.session_state.base_ejercicios]
    st.dataframe(tabla_datos, use_container_width=True)

# ==========================================
# PESTAÑA 5: SUSTITUCIÓN RÁPIDA
# ==========================================
with tab_remplazo:
    st.subheader("🔄 Sustitución Inteligente por Equipamiento / Lesión")
    ej_sel = st.selectbox("Selecciona el ejercicio a cambiar:", [e.nombre for e in st.session_state.base_ejercicios])
    if st.button("Buscar Alternativa Reemplazante"):
        obj_ej = next(e for e in st.session_state.base_ejercicios if e.nombre == ej_sel)
        reemplazo = MotorEntrenamiento.sustituir_ejercicio(obj_ej, atleta.equipamiento_disponible)
        if reemplazo:
            st.success(f"✔️ **Sustituto Sugerido:** {reemplazo.nombre}")
            st.write(f"- **Bloque:** {reemplazo.bloque} | **Patrón:** {reemplazo.patron_movimiento}")
            st.write(f"- **Equipamiento:** {reemplazo.equipamiento} | **Estrés Articular:** {reemplazo.estres_articular}/5")
            if reemplazo.url_video: st.video(reemplazo.url_video)
        else:
            st.warning("No hay alternativas disponibles para ese patrón con el equipamiento seleccionado.")
