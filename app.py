import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y ESTILOS (CSS)
# ==========================================

st.set_page_config(page_title="ProGym Engine v3.0", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
<style>
    .block-container-card {
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 6px solid #4CAF50;
        background-color: #1E1E1E;
        color: white;
    }
    .block-a { border-left-color: #3498db; background-color: #0f1b29; }
    .block-b { border-left-color: #e74c3c; background-color: #291010; }
    .block-c { border-left-color: #f39c12; background-color: #291d0f; }
    .block-d { border-left-color: #9b59b6; background-color: #200f29; }

    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        border-radius: 0.25rem;
        margin-right: 5px;
        color: white;
    }
    .badge-stress { background-color: #e67e22; }
    .badge-equip { background-color: #2bc4ad; }
    .badge-athletic { background-color: #8e44ad; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODELOS DE DATOS Y BASE EXPANDIDA
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    bloque: str  # Bloque A (Movilidad/Pliometría), Bloque B (Principales), Bloque C (Secundarios), Bloque D (Accesorios)
    patron_movimiento: str
    musculo_principal: str
    musculos_accesorios: List[str]
    equipamiento: str
    estres_articular: int  # 1 (Bajo) a 5 (Alto)
    es_atletico: bool = False

@dataclass
class PerfilAtleta:
    nombre: str
    tipo_rutina: str
    objetivo: str
    es_deportista: bool = False
    musculo_especializacion: Optional[str] = None
    equipamiento_disponible: List[str] = field(default_factory=list)

    def evaluar_wellness(self, sueno: int, estres: int, agujetas: int, fatiga: int) -> float:
        sueno_norm = min(max(sueno, 1), 5)
        estres_norm = 6 - min(max(estres, 1), 5)
        agujetas_norm = 6 - min(max(agujetas, 1), 5)
        fatiga_norm = 6 - min(max(fatiga, 1), 5)
        return round((sueno_norm + estres_norm + agujetas_norm + fatiga_norm) / 4.0, 2)

BASE_EJERCICIOS: List[Ejercicio] = [
    # --- BLOQUE A: MOVILIDAD, ACTIVACIÓN Y PLIOMETRÍA (DEPORTISTAS) ---
    Ejercicio("A1", "Gato-Camello", "Bloque A", "Movilidad Columna", "Zona Media", [], "Peso Corporal", 1),
    Ejercicio("A2", "Rotación Torácica Quadrupedal", "Bloque A", "Movilidad Torácica", "Espalda Alta", [], "Peso Corporal", 1),
    Ejercicio("A3", "World's Greatest Stretch", "Bloque A", "Movilidad Cadera", "Cadera/Isquios", ["Core"], "Peso Corporal", 1),
    Ejercicio("A4", "Dislocaciones de Hombro", "Bloque A", "Movilidad Hombros", "Manguito Rotador", [], "Banda elástica", 1),
    Ejercicio("A5", "Saltos Pliométricos al Cajón", "Bloque A", "Potencia / Pliometría", "Tren Inferior", ["Core"], "Peso Corporal", 2, es_atletico=True),
    Ejercicio("A6", "Lanzamiento de Balón Medicinal Balístico", "Bloque A", "Potencia / Pliometría", "Tren Superior", ["Core"], "Peso Corporal", 2, es_atletico=True),

    # --- BLOQUE B: EJERCICIOS PRINCIPALES Y DE POTENCIA ---
    Ejercicio("B1", "Press de Banca con Barra", "Bloque B", "Empuje Horizontal", "Pectoral", ["Tríceps", "Deltoides Ant"], "Barra", 4),
    Ejercicio("B2", "Sentadilla Trasera con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Barra", 5),
    Ejercicio("B3", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Isquiosurales", ["Glúteo", "Espalda Baja"], "Barra", 5),
    Ejercicio("B4", "Press Militar con Barra", "Bloque B", "Empuje Vertical", "Deltoides", ["Tríceps"], "Barra", 4),
    Ejercicio("B5", "Dominadas Prona Lastradas", "Bloque B", "Tracción Vertical", "Dorsal", ["Bíceps"], "Peso Corporal", 4),
    Ejercicio("B6", "Power Clean (Cargada de Potencia)", "Bloque B", "Potencia Olímipica", "Cadena Posterior", ["Trapies", "Cuádriceps"], "Barra", 5, es_atletico=True),
    Ejercicio("B7", "Press Landmine Explosivo", "Bloque B", "Empuje Unilateral", "Deltoides", ["Pectoral", "Core"], "Barra", 2, es_atletico=True),

    # --- BLOQUE C: EJERCICIOS SECUNDARIOS ---
    Ejercicio("C1", "Press Inclinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral", ["Tríceps"], "Mancuernas", 3),
    Ejercicio("C2", "Prensa de Piernas 45°", "Bloque C", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Máquina", 2),
    Ejercicio("C3", "Peso Muerto Rumano con Mancuernas", "Bloque C", "Dominante de Cadera", "Isquiosurales", ["Glúteo"], "Mancuernas", 3),
    Ejercicio("C4", "Jalón al Pecho Agarre Neutro", "Bloque C", "Tracción Vertical", "Dorsal", ["Bíceps"], "Polea", 2),
    Ejercicio("C5", "Remo Horizontal con Mancuerna", "Bloque C", "Tracción Horizontal", "Dorsal", ["Romboide", "Bíceps"], "Mancuernas", 2),
    Ejercicio("C6", "Zancadas Búlgaras", "Bloque C", "Dominante Unilateral", "Cuádriceps", ["Glúteo"], "Mancuernas", 3, es_atletico=True),

    # --- BLOQUE D: ACCESORIOS Y AISLAMIENTO ---
    Ejercicio("D1", "Elevaciones Laterales con Mancuerna", "Bloque D", "Aislamiento", "Deltoides", [], "Mancuernas", 1),
    Ejercicio("D2", "Extensiones de Tríceps en Polea Alta", "Bloque D", "Aislamiento", "Tríceps", [], "Polea", 1),
    Ejercicio("D3", "Curl de Bíceps Inclinado", "Bloque D", "Aislamiento", "Bíceps", [], "Mancuernas", 1),
    Ejercicio("D4", "Face Pull con Cuerda", "Bloque D", "Salud Articular", "Deltoides", ["Manguito Rotador"], "Polea", 1),
    Ejercicio("D5", "Rueda Abdominal (Ab Wheel)", "Bloque D", "Core", "Zona Media", [], "Peso Corporal", 3, es_atletico=True),
]

# ==========================================
# 3. MOTOR Y LÓGICA DE NEGOCIO AVANZADA
# ==========================================

class MotorEntrenamiento:

    @staticmethod
    def obtener_parametros_objetivo(objetivo: str) -> Dict[str, str]:
        if objetivo == "Hipertrofia":
            return {"reps_b": "6-10", "reps_c": "8-12", "reps_d": "12-15", "rir_base": 1, "factor_volumen": 1.0}
        elif objetivo == "Pérdida de Grasa / Definición":
            return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "12-15", "rir_base": 1, "factor_volumen": 0.85}
        elif objetivo == "Rendimiento Deportivo / Performance":
            return {"reps_b": "3-5 (Explosivas)", "reps_c": "6-8", "reps_d": "8-10", "rir_base": 2, "factor_volumen": 1.0}
        else:  # Mantenimiento
            return {"reps_b": "8-10", "reps_c": "10-12", "reps_d": "10-12", "rir_base": 2, "factor_volumen": 0.7}

    @staticmethod
    def filtrar_patrones_por_rutina(tipo_rutina: str, sub_dia: str) -> List[str]:
        if tipo_rutina == "Fullbody":
            return ["Empuje Horizontal", "Dominante de Rodilla", "Tracción Vertical", "Dominante de Cadera"]
        elif tipo_rutina == "Torso-Pierna":
            return ["Empuje Horizontal", "Tracción Vertical", "Empuje Vertical", "Tracción Horizontal"] if sub_dia == "Torso" else ["Dominante de Rodilla", "Dominante de Cadera", "Dominante Unilateral"]
        elif tipo_rutina == "Push-Pull-Legs (PPL)":
            if sub_dia == "Push (Empuje)": return ["Empuje Horizontal", "Empuje Vertical"]
            elif sub_dia == "Pull (Tracción)": return ["Tracción Vertical", "Tracción Horizontal"]
            else: return ["Dominante de Rodilla", "Dominante de Cadera"]
        else:  # Weider
            return ["Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", "Dominante de Rodilla"]

    @staticmethod
    def sustituir_ejercicio(ejercicio_actual: Ejercicio, equipamiento_disponible: List[str]) -> Optional[Ejercicio]:
        candidatos = [
            e for e in BASE_EJERCICIOS
            if e.id != ejercicio_actual.id
            and e.bloque == ejercicio_actual.bloque
            and (e.patron_movimiento == ejercicio_actual.patron_movimiento or e.musculo_principal == ejercicio_actual.musculo_principal)
            and e.estres_articular <= ejercicio_actual.estres_articular
            and e.equipamiento in equipamiento_disponible
        ]
        candidatos.sort(key=lambda x: x.estres_articular)
        return candidatos[0] if candidatos else None

    @staticmethod
    def generar_rutina_completa(atleta: PerfilAtleta, sub_dia: str, score_wellness: float) -> Dict[str, List[Dict]]:
        rutina_bloques = {"Bloque A": [], "Bloque B": [], "Bloque C": [], "Bloque D": []}
        params_obj = MotorEntrenamiento.obtener_parametros_objetivo(atleta.objetivo)
        
        mod_series = -1 if score_wellness < 3.0 else 0
        mod_rir = +2 if score_wellness < 3.0 else 0
        patrones_sesion = MotorEntrenamiento.filtrar_patrones_por_rutina(atleta.tipo_rutina, sub_dia)

        # BLOQUE A: Movilidad / Pliometría
        movilidad = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque A" and e.equipamiento in atleta.equipamiento_disponible]
        if atleta.es_deportista:
            movilidad.sort(key=lambda x: not x.es_atletico)
        for ej in movilidad[:2]:
            rutina_bloques["Bloque A"].append({
                "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": "2 Series x 8-10 Reps | RIR 4 (Control dinámico)",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "atletico": ej.es_atletico
            })

        # BLOQUE B: Principales / Potencia
        principales = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque B" and (e.patron_movimiento in patrones_sesion or (atleta.es_deportista and e.es_atletico)) and e.equipamiento in atleta.equipamiento_disponible]
        for ej in principales[:2]:
            series = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque B"].append({
                "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_b']} Reps | RIR {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "atletico": ej.es_atletico
            })

        # BLOQUE C: Secundarios
        secundarios = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque C" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in secundarios[:2]:
            series_finales = max(2, int(3 * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque C"].append({
                "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_c']} Reps | RIR {params_obj['rir_base'] + mod_rir + 1}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "atletico": ej.es_atletico
            })

        # BLOQUE D: Accesorios
        accesorios = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque D" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in accesorios[:2]:
            series_acc = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            series_finales = max(2, int(series_acc * params_obj["factor_volumen"]) + mod_series)
            rutina_bloques["Bloque D"].append({
                "nombre": ej.nombre, "patron": ej.patron_movimiento,
                "detalles": f"{series_finales} Series x {params_obj['reps_d']} Reps | RIR {params_obj['rir_base'] + mod_rir}",
                "estres": ej.estres_articular, "equipo": ej.equipamiento, "atletico": ej.es_atletico
            })

        return rutina_bloques

# ==========================================
# 4. INTERFAZ GRÁFICA DE USUARIO
# ==========================================

st.title("🏋️ ProGym Engine v3.0 — Automatización por Objetivos y Perfil")

# Sidebar
st.sidebar.header("👤 Configuración del Perfil")
nombre = st.sidebar.text_input("Nombre Usuario", "Carlos Pérez")
es_deportista = st.sidebar.checkbox("🏅 Es Deportista de Rendimiento", value=False)

tipo_rutina = st.sidebar.selectbox("Modalidad de Rutina", ["Fullbody", "Torso-Pierna", "Push-Pull-Legs (PPL)", "Weider"])
objetivo = st.sidebar.selectbox("Objetivo del Entrenamiento", ["Hipertrofia", "Pérdida de Grasa / Definición", "Rendimiento Deportivo / Performance", "Mantenimiento / Salud"])
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral", "Cuádriceps", "Dorsal", "Deltoides", "Isquiosurales"])

equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"]
)

st.sidebar.divider()
st.sidebar.header("📊 Wellness Pre-Entreno")
sueno = st.sidebar.slider("Sueño (1 Malo - 5 Excelente)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1 Alto - 5 Muy Bajo)", 1, 5, 3)
agujetas = st.sidebar.slider("Agujetas (1 Altas - 5 Nulas)", 1, 5, 3)
fatiga = st.sidebar.slider("Fatiga General (1 Alta - 5 Nula)", 1, 5, 3)

atleta = PerfilAtleta(
    nombre=nombre, tipo_rutina=tipo_rutina, objetivo=objetivo,
    es_deportista=es_deportista, musculo_especializacion=especializacion, equipamiento_disponible=equipamiento
)
score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Banner superior
col_w1, col_w2 = st.columns([1, 3])
with col_w1:
    st.metric("Puntuación Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0:
        st.error("⚠️ **Autorregulación por Fatiga:** Se reduce volumen (-1 serie) e intensidad (+2 RIR).")
    else:
        st.success(f"✅ **Estado Óptimo:** Generando rutina optimizada para **{objetivo}** ({tipo_rutina}).")

st.divider()

# Pestañas Principales
tab_rutina, tab_remplazo, tab_database = st.tabs(["📋 Rutina Generada", "🔄 Reemplazo Inteligente", "📚 Base de Datos"])

with tab_rutina:
    sub_dia = "General"
    if tipo_rutina == "Torso-Pierna":
        sub_dia = st.radio("Selecciona el día de la sesión:", ["Torso", "Pierna"], horizontal=True)
    elif tipo_rutina == "Push-Pull-Legs (PPL)":
        sub_dia = st.radio("Selecciona el día de la sesión:", ["Push (Empuje)", "Pull (Tracción)", "Legs (Pierna)"], horizontal=True)

    if st.button("⚡ Generar Rutina Automatizada", type="primary"):
        rutina = MotorEntrenamiento.generar_rutina_completa(atleta, sub_dia, score_wellness)
        
        # BLOQUE A
        st.markdown('<div class="block-container-card block-a"><h3>BLOQUE A: Movilidad y Pliometría / Activación</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque A"]:
            badge_atl = '<span class="badge badge-athletic">Deportivo</span>' if item['atletico'] else ''
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | {badge_atl} <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")
        
        # BLOQUE B
        st.markdown('<div class="block-container-card block-b"><h3>BLOQUE B: Ejercicios Principales / Potencia</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque B"]:
            badge_atl = '<span class="badge badge-athletic">Deportivo</span>' if item['atletico'] else ''
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | {badge_atl} <span class='badge badge-stress'>Estrés Articular: {item['estres']}/5</span> | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")

        # BLOQUE C
        st.markdown('<div class="block-container-card block-c"><h3>BLOQUE C: Ejercicios Secundarios</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque C"]:
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")

        # BLOQUE D
        st.markdown('<div class="block-container-card block-d"><h3>BLOQUE D: Accesorios y Salud Articular</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque D"]:
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")

with tab_remplazo:
    st.subheader("Sustitución de Ejercicio Ocupado o Con Molestia")
    ej_seleccionado_nombre = st.selectbox("Selecciona el ejercicio a sustituir:", [e.nombre for e in BASE_EJERCICIOS])
    
    if st.button("Buscar Alternativa Inteligente"):
        obj_ej = next(e for e in BASE_EJERCICIOS if e.nombre == ej_seleccionado_nombre)
        reemplazo = MotorEntrenamiento.sustituir_ejercicio(obj_ej, atleta.equipamiento_disponible)
        
        if reemplazo:
            st.success(f"✔️ **Sustituto Encontrado:** {reemplazo.nombre}")
            st.write(f"- **Bloque:** {reemplazo.bloque}")
            st.write(f"- **Músculo Principal:** {reemplazo.musculo_principal}")
            st.write(f"- **Equipamiento:** {reemplazo.equipamiento}")
            st.write(f"- **Estrés Articular:** {reemplazo.estres_articular}/5")
        else:
            st.warning("No hay alternativas disponibles para ese patrón con el equipamiento seleccionado.")

with tab_database:
    st.subheader("Catálogo Completo de Ejercicios")
    tabla_datos = [
        {
            "Bloque": e.bloque,
            "Nombre": e.nombre,
            "Patrón": e.patron_movimiento,
            "Músculo Principal": e.musculo_principal,
            "Perfil Deportivo": "Sí" if e.es_atletico else "No",
            "Equipamiento": e.equipamiento,
            "Estrés Articular": f"{e.estres_articular}/5"
        }
        for e in BASE_EJERCICIOS
    ]
    st.dataframe(tabla_datos, use_container_width=True)
