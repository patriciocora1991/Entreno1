import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y ESTILOS (CSS)
# ==========================================

st.set_page_config(page_title="ProGym Engine", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
<style>
    /* Tarjetas de Bloques */
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

    /* Badges de atributos */
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
    .badge-target { background-color: #27ae60; }

    /* Métricas destacadas */
    .metric-box {
        background-color: #262730;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MODELOS DE DATOS Y BASE EXPANDIDA
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    bloque: str  # Bloque A, Bloque B, Bloque C, Bloque D
    patron_movimiento: str
    musculo_principal: str
    musculos_accesorios: List[str]
    equipamiento: str
    estres_articular: int  # 1 (Bajo) a 5 (Alto)

@dataclass
class PerfilAtleta:
    nombre: str
    es_deportista: bool = False
    musculo_especializacion: Optional[str] = None
    equipamiento_disponible: List[str] = field(default_factory=list)

    def evaluar_wellness(self, sueno: int, estres: int, agujetas: int, fatiga: int) -> float:
        sueno_norm = min(max(sueno, 1), 5)
        estres_norm = 6 - min(max(estres, 1), 5)
        agujetas_norm = 6 - min(max(agujetas, 1), 5)
        fatiga_norm = 6 - min(max(fatiga, 1), 5)
        return round((sueno_norm + estres_norm + agujetas_norm + fatiga_norm) / 4.0, 2)

# Base de datos ampliada categorizada por bloques
BASE_EJERCICIOS: List[Ejercicio] = [
    # --- BLOQUE A: MOVILIDAD Y ACTIVACIÓN ---
    Ejercicio("A1", "Gato-Camello", "Bloque A", "Movilidad Columna", "Zona Media", [], "Peso Corporal", 1),
    Ejercicio("A2", "Rotación Torácica Quadrupedal", "Bloque A", "Movilidad Torácica", "Espalda Alta", [], "Peso Corporal", 1),
    Ejercicio("A3", "World's Greatest Stretch", "Bloque A", "Movilidad Cadera", "Cadera/Isquios", ["Core"], "Peso Corporal", 1),
    Ejercicio("A4", "Dislocaciones de Hombro", "Bloque A", "Movilidad Hombros", "Manguito Rotador", [], "Banda elástica", 1),
    Ejercicio("A5", "90/90 de Cadera", "Bloque A", "Movilidad Cadera", "Glúteo/Aductores", [], "Peso Corporal", 1),

    # --- BLOQUE B: EJERCICIOS PRINCIPALES ---
    Ejercicio("B1", "Press de Banca con Barra", "Bloque B", "Empuje Horizontal", "Pectoral", ["Tríceps", "Deltoides Ant"], "Barra", 4),
    Ejercicio("B2", "Sentadilla Trasera con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Barra", 5),
    Ejercicio("B3", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Isquiosurales", ["Glúteo", "Espalda Baja"], "Barra", 5),
    Ejercicio("B4", "Press Militar con Barra", "Bloque B", "Empuje Vertical", "Deltoides", ["Tríceps"], "Barra", 4),
    Ejercicio("B5", "Dominadas Prona Lastradas", "Bloque B", "Tracción Vertical", "Dorsal", ["Bíceps"], "Peso Corporal", 4),

    # --- BLOQUE C: EJERCICIOS SECUNDARIOS ---
    Ejercicio("C1", "Press Inclinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral Superior", ["Tríceps"], "Mancuernas", 3),
    Ejercicio("C2", "Prensa de Piernas 45°", "Bloque C", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Máquina", 2),
    Ejercicio("C3", "Peso Muerto Rumano con Mancuernas", "Bloque C", "Dominante de Cadera", "Isquiosurales", ["Glúteo"], "Mancuernas", 3),
    Ejercicio("C4", "Jalón al Pecho Agarre Neutro", "Bloque C", "Tracción Vertical", "Dorsal", ["Bíceps"], "Polea", 2),
    Ejercicio("C5", "Remo Horizontal con Mancuerna a 1 Brazo", "Bloque C", "Tracción Horizontal", "Dorsal", ["Romboide", "Bíceps"], "Mancuernas", 2),
    Ejercicio("C6", "Zancadas Búlgaras", "Bloque C", "Dominante Unilateral", "Cuádriceps", ["Glúteo"], "Mancuernas", 3),

    # --- BLOQUE D: ACCESORIOS Y AISLAMIENTO ---
    Ejercicio("D1", "Elevaciones Laterales con Mancuerna", "Bloque D", "Aislamiento", "Deltoides Lateral", [], "Mancuernas", 1),
    Ejercicio("D2", "Extensiones de Tríceps en Polea Alta", "Bloque D", "Aislamiento", "Tríceps", [], "Polea", 1),
    Ejercicio("D3", "Curl de Bíceps en Banco Inclinado", "Bloque D", "Aislamiento", "Bíceps", [], "Mancuernas", 1),
    Ejercicio("D4", "Face Pull con Cuerda", "Bloque D", "Salud Articular", "Deltoides Post", ["Manguito Rotador"], "Polea", 1),
    Ejercicio("D5", "Curl Femoral Tumbado", "Bloque D", "Aislamiento", "Isquiosurales", [], "Máquina", 2),
    Ejercicio("D6", "Rueda Abdominal (Ab Wheel)", "Bloque D", "Core", "Abdomen", ["Zona Media"], "Peso Corporal", 3),
]

# ==========================================
# 3. MOTOR DE GENERACIÓN AUTOMATIZADA
# ==========================================

class MotorEntrenamiento:

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
    def generar_rutina_completa(atleta: PerfilAtleta, patrones_seleccionados: List[str], score_wellness: float) -> Dict[str, List[Dict]]:
        rutina_bloques = {"Bloque A": [], "Bloque B": [], "Bloque C": [], "Bloque D": []}
        
        # Ajustes por fatiga (Wellness)
        factor_fatiga = score_wellness < 3.0
        mod_series = -1 if factor_fatiga else 0
        mod_rir = +2 if factor_fatiga else 0

        # BLOQUE A: Movilidad (2 ejercicios fijos adaptados a la sesión)
        movilidad_disponible = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque A" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in movilidad_disponible[:2]:
            rutina_bloques["Bloque A"].append({
                "id": ej.id,
                "nombre": ej.nombre,
                "patron": ej.patron_movimiento,
                "detalles": "2 Series x 10-12 Repeticiones | RIR 4 (Control dinámico)",
                "estres": ej.estres_articular,
                "equipo": ej.equipamiento
            })

        # BLOQUE B: Ejercicios Principales (Seguridad y máxima carga)
        principales = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque B" and e.patron_movimiento in patrones_seleccionados and e.equipamiento in atleta.equipamiento_disponible]
        for ej in principales:
            series = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            rutina_bloques["Bloque B"].append({
                "id": ej.id,
                "nombre": ej.nombre,
                "patron": ej.patron_movimiento,
                "detalles": f"{max(2, series + mod_series)} Series x 5-8 Reps | RIR {1 + mod_rir}",
                "estres": ej.estres_articular,
                "equipo": ej.equipamiento
            })

        # BLOQUE C: Ejercicios Secundarios
        secundarios = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque C" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in secundarios[:2]:
            rutina_bloques["Bloque C"].append({
                "id": ej.id,
                "nombre": ej.nombre,
                "patron": ej.patron_movimiento,
                "detalles": f"{max(2, 3 + mod_series)} Series x 8-12 Reps | RIR {2 + mod_rir}",
                "estres": ej.estres_articular,
                "equipo": ej.equipamiento
            })

        # BLOQUE D: Accesorios / Aislamiento / Salud Articular
        accesorios = [e for e in BASE_EJERCICIOS if e.bloque == "Bloque D" and e.equipamiento in atleta.equipamiento_disponible]
        for ej in accesorios[:2]:
            series_acc = 4 if atleta.musculo_especializacion and ej.musculo_principal == atleta.musculo_especializacion else 3
            rutina_bloques["Bloque D"].append({
                "id": ej.id,
                "nombre": ej.nombre,
                "patron": ej.patron_movimiento,
                "detalles": f"{max(2, series_acc + mod_series)} Series x 12-15 Reps | RIR {1 + mod_rir}",
                "estres": ej.estres_articular,
                "equipo": ej.equipamiento
            })

        return rutina_bloques

# ==========================================
# 4. INTERFAZ GRÁFICA DE USUARIO
# ==========================================

st.title("🏋️ ProGym Engine — Sistema Estructurado por Bloques")

# Sidebar
st.sidebar.header("👤 Perfil & Parámetros")
nombre = st.sidebar.text_input("Deportista / Cliente", "Carlos Pérez")
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral", "Cuádriceps", "Dorsal", "Deltoides", "Isquiosurales"])
equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"]
)

st.sidebar.divider()
st.sidebar.header("📊 Wellness Diario (Pre-Entreno)")
sueno = st.sidebar.slider("Sueño (1 Malo - 5 Excelente)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1 Alto - 5 Muy Bajo)", 1, 5, 3)
agujetas = st.sidebar.slider("Agujetas (1 Altas - 5 Nulas)", 1, 5, 3)
fatiga = st.sidebar.slider("Fatiga General (1 Alta - 5 Nula)", 1, 5, 3)

atleta = PerfilAtleta(nombre=nombre, musculo_especializacion=especializacion, equipamiento_disponible=equipamiento)
score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Banner de estado Wellness
col_w1, col_w2 = st.columns([1, 3])
with col_w1:
    st.metric("Puntuación Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0:
        st.error("⚠️ **Alerta de Fatiga:** Volumen reducido (-1 serie) e intensidad ajustada (+2 RIR) en todos los bloques.")
    else:
        st.success("✅ **Estado Óptimo:** Prescripción completa autorregulado sin restricciones.")

st.divider()

# Pestañas de la Aplicación
tab_rutina, tab_remplazo, tab_database = st.tabs(["📋 Rutina en Bloques", "🔄 Reemplazo Inteligente", "📚 Base de Datos"])

with tab_rutina:
    patrones_objetivo = st.multiselect(
        "Selecciona los patrones principales para la sesión:",
        ["Empuje Horizontal", "Dominante de Rodilla", "Dominante de Cadera", "Empuje Vertical", "Tracción Vertical"],
        default=["Empuje Horizontal", "Dominante de Rodilla"]
    )

    if st.button("⚡ Generar Plan por Bloques", type="primary"):
        rutina = MotorEntrenamiento.generar_rutina_completa(atleta, patrones_objetivo, score_wellness)
        
        # BLOQUE A
        st.markdown('<div class="block-container-card block-a"><h3>BLOQUE A: Movilidad y Activación Articular</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque A"]:
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")
        
        # BLOQUE B
        st.markdown('<div class="block-container-card block-b"><h3>BLOQUE B: Ejercicios Principales (Multiarticulares Pesados)</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque B"]:
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-stress'>Estrés Articular: {item['estres']}/5</span> | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")

        # BLOQUE C
        st.markdown('<div class="block-container-card block-c"><h3>BLOQUE C: Ejercicios Secundarios (Complementarios)</h3></div>', unsafe_allow_html=True)
        for item in rutina["Bloque C"]:
            st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
            st.caption(f"📌 Prescripción: {item['detalles']}")

        # BLOQUE D
        st.markdown('<div class="block-container-card block-d"><h3>BLOQUE D: Accesorios y Aislamiento Muscular</h3></div>', unsafe_allow_html=True)
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
            st.write(f"- **Estrés Articular:** {reemplazo.estres_articular}/5 (vs. {obj_ej.estres_articular}/5 original)")
        else:
            st.warning("No hay alternativas disponibles en la base de datos para ese patrón y equipamiento disponible.")

with tab_database:
    st.subheader("Catálogo de Ejercicios Cargados")
    tabla_datos = [
        {
            "Bloque": e.bloque,
            "Nombre": e.nombre,
            "Patrón": e.patron_movimiento,
            "Músculo Principal": e.musculo_principal,
            "Equipamiento": e.equipamiento,
            "Estrés Articular": f"{e.estres_articular}/5"
        }
        for e in BASE_EJERCICIOS
    ]
    st.dataframe(tabla_datos, use_container_width=True)
