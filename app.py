import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ==========================================
# 1. MODELOS DE DATOS
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    patron_movimiento: str
    musculo_principal: str
    musculos_accesorios: List[str]
    equipamiento: str
    estres_articular: int  # Escala 1 a 5

@dataclass
class PerfilAtleta:
    nombre: str
    es_deportista: bool = False
    musculo_especializacion: Optional[str] = None
    equipamiento_disponible: List[str] = field(
        default_factory=lambda: ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal"]
    )
    historial_carga_diaria: List[float] = field(default_factory=list)

    def evaluar_wellness(self, sueno: int, estres: int, agujetas: int, fatiga: int) -> float:
        sueno_norm = min(max(sueno, 1), 5)
        estres_norm = 6 - min(max(estres, 1), 5)
        agujetas_norm = 6 - min(max(agujetas, 1), 5)
        fatiga_norm = 6 - min(max(fatiga, 1), 5)
        return round((sueno_norm + estres_norm + agujetas_norm + fatiga_norm) / 4.0, 2)

    def calcular_acwr(self) -> float:
        if len(self.historial_carga_diaria) < 28:
            return 1.0
        carga_aguda = sum(self.historial_carga_diaria[-7:]) / 7.0
        carga_cronica = sum(self.historial_carga_diaria[-28:]) / 28.0
        return round(carga_aguda / carga_cronica, 2) if carga_cronica > 0 else 1.0

# ==========================================
# 2. BASE DE DATOS LOCAL
# ==========================================

BASE_EJERCICIOS = [
    Ejercicio("1", "Press de Banca con Barra", "Empuje Horizontal", "Pectoral", ["Tríceps", "Deltoides Ant"], "Barra", 4),
    Ejercicio("2", "Press con Mancuernas Plano", "Empuje Horizontal", "Pectoral", ["Tríceps"], "Mancuernas", 2),
    Ejercicio("3", "Flexiones de Brazo", "Empuje Horizontal", "Pectoral", ["Tríceps"], "Peso Corporal", 1),
    Ejercicio("4", "Sentadilla Trasera", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Barra", 5),
    Ejercicio("5", "Prensa de Piernas 45°", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Máquina", 2),
    Ejercicio("6", "Dominadas Prona", "Tracción Vertical", "Dorsal", ["Bíceps"], "Peso Corporal", 3),
    Ejercicio("7", "Jalón al Pecho", "Tracción Vertical", "Dorsal", ["Bíceps"], "Polea", 2),
    Ejercicio("8", "Peso Muerto Rumano", "Dominante de Cadera", "Isquiosurales", ["Glúteo"], "Barra", 4),
]

# ==========================================
# 3. MOTOR Y LÓGICA DE NEGOCIO
# ==========================================

class MotorEntrenamiento:

    @staticmethod
    def sustituir_ejercicio(ejercicio_actual: Ejercicio, equipamiento_disponible: List[str]) -> Optional[Ejercicio]:
        candidatos = [
            e for e in BASE_EJERCICIOS
            if e.id != ejercicio_actual.id
            and e.patron_movimiento == ejercicio_actual.patron_movimiento
            and e.musculo_principal == ejercicio_actual.musculo_principal
            and e.estres_articular <= ejercicio_actual.estres_articular
            and e.equipamiento in equipamiento_disponible
        ]
        candidatos.sort(key=lambda x: x.estres_articular)
        return candidatos[0] if candidatos else None

    @staticmethod
    def generar_rutina(atleta: PerfilAtleta, patrones: List[str], score_wellness: float) -> List[Dict]:
        sesion = []
        mod_series = -1 if score_wellness < 3.0 else 0
        mod_rir = +2 if score_wellness < 3.0 else 0

        for patron in patrones:
            ejercicio = next(
                (e for e in BASE_EJERCICIOS if e.patron_movimiento == patron and e.equipamiento in atleta.equipamiento_disponible),
                None
            )
            if ejercicio:
                series = 3
                if atleta.musculo_especializacion and ejercicio.musculo_principal == atleta.musculo_especializacion:
                    series += 1

                sesion.append({
                    "Ejercicio": ejercicio.nombre,
                    "Patrón": ejercicio.patron_movimiento,
                    "Músculo Principal": ejercicio.musculo_principal,
                    "Series": max(2, series + mod_series),
                    "Repeticiones": "8-12",
                    "RIR Prescripto": 1 + mod_rir,
                    "Estrés Articular": f"{ejercicio.estres_articular}/5"
                })
        return sesion

# ==========================================
# 4. INTERFAZ WEB STREAMLIT (100% PYTHON)
# ==========================================

st.set_page_config(page_title="Gym Workout Engine", page_icon="🏋️", layout="wide")

st.title("🏋️ Motor de Entrenamiento Autorregulado")
st.markdown("Generación dinámica de rutinas con autorregulación por Wellness y sustitución inteligente.")

# Panel Lateral (Configuración)
st.sidebar.header("📋 Perfil del Atleta")
nombre = st.sidebar.text_input("Nombre del Usuario", "Carlos Pérez")
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral", "Cuádriceps", "Dorsal", "Isquiosurales"])
equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal"],
    default=["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal"]
)

atleta = PerfilAtleta(nombre=nombre, musculo_especializacion=especializacion, equipamiento_disponible=equipamiento)

st.sidebar.header("📊 Check-in Wellness Diarios")
sueno = st.sidebar.slider("Sueño (1 Malo - 5 Óptimo)", 1, 5, 4)
estres = st.sidebar.slider("Estrés (1 Alto - 5 Bajo)", 1, 5, 2)
agujetas = st.sidebar.slider("Agujetas (1 Altas - 5 Nulas)", 1, 5, 2)
fatiga = st.sidebar.slider("Fatiga General (1 Alta - 5 Nula)", 1, 5, 2)

score_wellness = atleta.evaluar_wellness(sueno, estres, agujetas, fatiga)

# Panel Principal
col1, col2 = st.columns(2)
with col1:
    st.metric("Puntuación Wellness de Hoy", f"{score_wellness} / 5.0")
with col2:
    if score_wellness < 3.0:
        st.warning("⚠️ Alerta de Fatiga: La rutina se autorregulará reduciendo 1 serie por ejercicio e incrementando el RIR en +2.")
    else:
        st.success("✅ Estado Óptimo: Se prescribirá volumen e intensidad normal.")

st.divider()

# Sección 1: Generador de Rutinas
st.subheader("🎯 Prescripción de Rutina")
patrones_seleccionados = st.multiselect(
    "Selecciona los Patrones de Movimiento para la Sesión",
    ["Empuje Horizontal", "Dominante de Rodilla", "Tracción Vertical", "Dominante de Cadera"],
    default=["Empuje Horizontal", "Dominante de Rodilla"]
)

if st.button("Generar Rutina Personalizada"):
    rutina = MotorEntrenamiento.generar_rutina(atleta, patrones_seleccionados, score_wellness)
    if rutina:
        st.table(rutina)
    else:
        st.error("No se encontraron ejercicios compatibles con el equipamiento seleccionado.")

st.divider()

# Sección 2: Reemplazo en Tiempo Real
st.subheader("🔁 Sustitución Inteligente de Ejercicio")
ej_seleccionado = st.selectbox("Selecciona un ejercicio ocupado o molesto", [e.nombre for e in BASE_EJERCICIOS])

if st.button("Buscar Reemplazo"):
    obj_ej = next(e for e in BASE_EJERCICIOS if e.nombre == ej_seleccionado)
    reemplazo = MotorEntrenamiento.sustituir_ejercicio(obj_ej, atleta.equipamiento_disponible)
    if reemplazo:
        st.info(f"👉 **Sustituto Recomendado:** {reemplazo.nombre} | **Equipo:** {reemplazo.equipamiento} | **Estrés Articular:** {reemplazo.estres_articular}/5")
    else:
        st.warning("No hay alternativas con menor o igual estrés articular disponibles para el equipamiento seleccionado.")
