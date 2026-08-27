import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y ESTILOS (CSS)
# ==========================================

st.set_page_config(page_title="ProGym Engine v4.0", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
<style>
    .block-card {
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 6px solid #4CAF50;
        background-color: #1E1E1E;
        color: white;
    }
    .block-warmup { border-left-color: #f1c40f; background-color: #26230f; }
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
# 2. MODELOS DE DATOS Y ESTADO GLOBAL
# ==========================================

@dataclass
class Ejercicio:
    id: str
    nombre: str
    bloque: str  # Warm-Up, Bloque B, Bloque C, Bloque D
    patron_movimiento: str
    musculo_principal: str
    musculos_accesorios: List[str]
    equipamiento: str
    estres_articular: int  # 1 a 5
    url_video: str = ""
    es_atletico: bool = False

# Inicializar Base de Datos Persistente en la Sesión
if "base_ejercicios" not in st.session_state:
    st.session_state.base_ejercicios = [
        # --- WARM-UP & MOVILIDAD OBLIGATORIO ---
        Ejercicio("W1", "Gato-Camello (Cat-Cow)", "Warm-Up", "Movilidad Columna", "Zona Media", [], "Peso Corporal", 1, "https://www.youtube.com/watch?v=kqnua4rHVVA"),
        Ejercicio("W2", "World's Greatest Stretch", "Warm-Up", "Movilidad Cadera", "Cadera/Isquios", ["Core"], "Peso Corporal", 1, "https://www.youtube.com/watch?v=vV1p24vLuh4"),
        Ejercicio("W3", "Dislocaciones de Hombro", "Warm-Up", "Movilidad Hombros", "Manguito Rotador", [], "Banda elástica", 1, "https://www.youtube.com/watch?v=33P5AI27eiU"),
        Ejercicio("W4", "Rotación Torácica Quadrupedal", "Warm-Up", "Movilidad Torácica", "Espalda Alta", [], "Peso Corporal", 1, "https://www.youtube.com/watch?v=d_kXpW_QpNA"),
        Ejercicio("W5", "Saltos Pliométricos al Cajón", "Warm-Up", "Potencia / Pliometría", "Tren Inferior", [], "Peso Corporal", 2, "https://www.youtube.com/watch?v=52r_Ul5k03g", es_atletico=True),

        # --- BLOQUE B: PRINCIPALES ---
        Ejercicio("B1", "Press de Banca con Barra", "Bloque B", "Empuje Horizontal", "Pectoral", ["Tríceps"], "Barra", 4, "https://www.youtube.com/watch?v=rT7DgCr-3pg"),
        Ejercicio("B2", "Sentadilla Trasera con Barra", "Bloque B", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Barra", 5, "https://www.youtube.com/watch?v=ultWZbUMPL8"),
        Ejercicio("B3", "Peso Muerto Convencional", "Bloque B", "Dominante de Cadera", "Isquiosurales", ["Glúteo"], "Barra", 5, "https://www.youtube.com/watch?v=op9kVnSso6Q"),
        Ejercicio("B4", "Press Militar con Barra", "Bloque B", "Empuje Vertical", "Deltoides", ["Tríceps"], "Barra", 4, "https://www.youtube.com/watch?v=2yjwXTZQDDI"),
        Ejercicio("B5", "Dominadas Prona Lastradas", "Bloque B", "Tracción Vertical", "Dorsal", ["Bíceps"], "Peso Corporal", 4, "https://www.youtube.com/watch?v=eGo4IYlbE5g"),
        Ejercicio("B6", "Power Clean", "Bloque B", "Potencia Olímipica", "Cadena Posterior", ["Trapecios"], "Barra", 5, "https://www.youtube.com/watch?v=KwYJTpQ_xg5", es_atletico=True),

        # --- BLOQUE C: SECUNDARIOS ---
        Ejercicio("C1", "Press Inclinado con Mancuernas", "Bloque C", "Empuje Horizontal", "Pectoral", ["Tríceps"], "Mancuernas", 3, "https://www.youtube.com/watch?v=8iPEnn-ltC8"),
        Ejercicio("C2", "Prensa de Piernas 45°", "Bloque C", "Dominante de Rodilla", "Cuádriceps", ["Glúteo"], "Máquina", 2, "https://www.youtube.com/watch?v=IZxyjW7MPJQ"),
        Ejercicio("C3", "Peso Muerto Rumano con Mancuernas", "Bloque C", "Dominante de Cadera", "Isquiosurales", ["Glúteo"], "Mancuernas", 3, "https://www.youtube.com/watch?v=JCXUYuzwNrM"),
        Ejercicio("C4", "Jalón al Pecho Agarre Neutro", "Bloque C", "Tracción Vertical", "Dorsal", ["Bíceps"], "Polea", 2, "https://www.youtube.com/watch?v=CAwf7n6Luuc"),
        Ejercicio("C5", "Zancadas Búlgaras", "Bloque C", "Dominante Unilateral", "Cuádriceps", ["Glúteo"], "Mancuernas", 3, "https://www.youtube.com/watch?v=2C-uNgKwPLE", es_atletico=True),

        # --- BLOQUE D: ACCESORIOS ---
        Ejercicio("D1", "Elevaciones Laterales con Mancuerna", "Bloque D", "Aislamiento", "Deltoides", [], "Mancuernas", 1, "https://www.youtube.com/watch?v=3VcKaXpzqRo"),
        Ejercicio("D2", "Extensiones de Tríceps en Polea", "Bloque D", "Aislamiento", "Tríceps", [], "Polea", 1, "https://www.youtube.com/watch?v=vB5OHsJ3EME"),
        Ejercicio("D3", "Curl de Bíceps Inclinado", "Bloque D", "Aislamiento", "Bíceps", [], "Mancuernas", 1, "https://www.youtube.com/watch?v=soxrZlIl35U"),
        Ejercicio("D4", "Face Pull con Cuerda", "Bloque D", "Salud Articular", "Deltoides", ["Manguito Rotador"], "Polea", 1, "https://www.youtube.com/watch?v=rep-qVOkqgk"),
    ]

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
        elif tipo_rutina == "Torso-Pierna": return ["Empuje Horizontal", "Tracción Vertical", "Empuje Vertical"] if sub_dia == "Torso" else ["Dominante de Rodilla", "Dominante de Cadera", "Dominante Unilateral"]
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
                "detalles": "2 Series x 10 Reps (Dinámico / Movilidad)",
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
# 4. INTERFAZ GRÁFICA DE USUARIO
# ==========================================

st.title("🏋️ ProGym Engine v4.0 — Control Completo")

# Rol Switcher
st.sidebar.header("🔑 Control de Acceso")
rol_usuario = st.sidebar.radio("Rol Actual", ["Alumno / Deportista", "Profesor / Entrenador"])

st.sidebar.divider()
st.sidebar.header("👤 Perfil & Parámetros")
nombre = st.sidebar.text_input("Nombre Usuario", "Carlos Pérez")
es_deportista = st.sidebar.checkbox("🏅 Perfil Deportivo de Alto Rendimiento", value=False)
tipo_rutina = st.sidebar.selectbox("Modalidad de Rutina", ["Fullbody", "Torso-Pierna", "Push-Pull-Legs (PPL)", "Weider"])
objetivo = st.sidebar.selectbox("Objetivo", ["Hipertrofia", "Pérdida de Grasa / Definición", "Rendimiento Deportivo / Performance", "Mantenimiento / Salud"])
especializacion = st.sidebar.selectbox("Especialización Muscular", [None, "Pectoral", "Cuádriceps", "Dorsal", "Deltoides", "Isquiosurales"])

equipamiento = st.sidebar.multiselect(
    "Equipamiento Disponible",
    ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"],
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

# Banner de estado
col_w1, col_w2 = st.columns([1, 3])
with col_w1: st.metric("Score Wellness", f"{score_wellness} / 5.0")
with col_w2:
    if score_wellness < 3.0: st.error("⚠️ **Autorregulación por Fatiga:** Volumen e intensidad ajustados.")
    else: st.success(f"✅ Modo **{rol_usuario}** activo | {objetivo} ({tipo_rutina})")

st.divider()

# Pestañas
tab_rutina, tab_plan, tab_crud, tab_remplazo = st.tabs(["📋 Sesión Diaria & Feedback", "🗓️ Plan Semanal/Mensual", "🛠️ Banco de Ejercicios (Profesor)", "🔄 Sustitución Rápida"])

# PESTAÑA 1: RUTINA & FEEDBACK
with tab_rutina:
    sub_dia = "General"
    if tipo_rutina == "Torso-Pierna": sub_dia = st.radio("Día:", ["Torso", "Pierna"], horizontal=True)
    elif tipo_rutina == "Push-Pull-Legs (PPL)": sub_dia = st.radio("Día:", ["Push (Empuje)", "Pull (Tracción)", "Legs (Pierna)"], horizontal=True)

    rutina = MotorEntrenamiento.generar_rutina_completa(atleta, sub_dia, score_wellness)
    
    # Renderizador de bloques
    def render_bloque(titulo: str, lista_ejercicios: List[Dict], css_class: str):
        st.markdown(f'<div class="block-card {css_class}"><h3>{titulo}</h3></div>', unsafe_allow_html=True)
        for item in lista_ejercicios:
            col_info, col_feed = st.columns([2, 1])
            with col_info:
                st.markdown(f"**{item['nombre']}** — *{item['patron']}* | <span class='badge badge-equip'>{item['equipo']}</span>", unsafe_allow_html=True)
                st.caption(f"📌 {item['detalles']}")
                if item["video"]:
                    with st.expander("🎥 Ver Técnica en Video"):
                        st.video(item["video"])
            with col_feed:
                if rol_usuario == "Alumno / Deportista":
                    st.text_input(f"Carga / Reps Reales ({item['id']})", placeholder="Ej: 80kg x 8", key=f"c_{item['id']}")
                    st.select_slider(f"RIR Percibido ({item['id']})", options=[0, 1, 2, 3, 4, 5], value=1, key=f"r_{item['id']}")
                else:
                    st.info("🔒 Registro reservado para el alumno")
            st.divider()

    render_bloque("🔥 WARM-UP & MOVILIDAD (OBLIGATORIO)", rutina["Warm-Up"], "block-warmup")
    render_bloque("BLOQUE B: Ejercicios Principales / Potencia", rutina["Bloque B"], "block-b")
    render_bloque("BLOQUE C: Ejercicios Secundarios", rutina["Bloque C"], "block-c")
    render_bloque("BLOQUE D: Accesorios & Salud Articular", rutina["Bloque D"], "block-d")

    if rol_usuario == "Alumno / Deportista":
        if st.button("💾 Guardar Feedback de la Sesión", type="primary"):
            st.success("✅ Registro guardado correctamente. Tu entrenador podrá visualizar tus observaciones.")

# PESTAÑA 2: PLAN SEMANAL Y MENSUAL
with tab_plan:
    st.subheader("🗓️ Planificación del Mesociclo (4 Semanas)")
    vista_plan = st.radio("Seleccionar Vista", ["Vista Semanal (Microciclo)", "Vista Mensual (Mesociclo)"], horizontal=True)

    if vista_plan == "Vista Semanal (Microciclo)":
        dias = ["Lunes (Día 1)", "Martes (Día 2)", "Miércoles (Descanso)", "Jueves (Día 3)", "Viernes (Día 4)", "Sábado (Cardio/Activo)", "Domingo (Descanso)"]
        for d in dias:
            with st.expander(f"📅 {d}"):
                st.write(f"Planificación asignada según esquema **{tipo_rutina}**.")
                st.caption("Warm-up obligatorio + 4 ejercicios de carga progresiva.")

    else:
        prog_mensual = [
            {"Semana": "Semana 1", "Fase": "Acumulación / Adaptación", "Volumen": "100%", "Intensidad": "RIR 2-3"},
            {"Semana": "Semana 2", "Fase": "Carga Principal", "Volumen": "110%", "Intensidad": "RIR 1-2"},
            {"Semana": "Semana 3", "Fase": "Pico de Intensidad", "Volumen": "120%", "Intensidad": "RIR 0-1"},
            {"Semana": "Semana 4", "Fase": "Descarga / Autorregulación", "Volumen": "50%", "Intensidad": "RIR 3-4"},
        ]
        st.table(prog_mensual)

# PESTAÑA 3: BANCO DE EJERCICIOS (CRUD PROFESOR)
with tab_crud:
    st.subheader("🛠️ Administración de la Base de Datos de Ejercicios")
    
    if rol_usuario == "Profesor / Entrenador":
        st.markdown("### ➕ Agregar Nuevo Ejercicio")
        with st.form("form_nuevo_ejercicio"):
            col1, col2, col3 = st.columns(3)
            with col1:
                n_id = st.text_input("ID Ejercicio", f"EX{len(st.session_state.base_ejercicios)+1}")
                n_nombre = st.text_input("Nombre Ejercicio", "Press Declinado con Mancuernas")
                n_bloque = st.selectbox("Bloque", ["Warm-Up", "Bloque B", "Bloque C", "Bloque D"])
            with col2:
                n_patron = st.selectbox("Patrón de Movimiento", ["Empuje Horizontal", "Empuje Vertical", "Tracción Vertical", "Tracción Horizontal", "Dominante de Rodilla", "Dominante de Cadera", "Movilidad Cadera", "Movilidad Hombros", "Aislamiento"])
                n_musculo = st.text_input("Músculo Principal", "Pectoral")
                n_equipo = st.selectbox("Equipamiento", ["Barra", "Mancuernas", "Máquina", "Polea", "Peso Corporal", "Banda elástica"])
            with col3:
                n_estres = st.slider("Estrés Articular (1-5)", 1, 5, 2)
                n_url = st.text_input("URL de Video (YouTube)", "https://www.youtube.com/watch?v=...")
                n_atletico = st.checkbox("¿Es para Deportistas?", value=False)
            
            btn_guardar = st.form_submit_button("Guardar Ejercicio")
            if btn_guardar:
                nuevo_ej = Ejercicio(n_id, n_nombre, n_bloque, n_patron, n_musculo, [], n_equipo, n_estres, n_url, n_atletico)
                st.session_state.base_ejercicios.append(nuevo_ej)
                st.success(f"✔️ Ejercicio '{n_nombre}' agregado exitosamente.")

        st.divider()
        st.markdown("### ❌ Eliminar Ejercicio")
        ej_eliminar = st.selectbox("Selecciona ejercicio a eliminar:", [e.nombre for e in st.session_state.base_ejercicios])
        if st.button("Eliminar Ejercicio Seleccionado"):
            st.session_state.base_ejercicios = [e for e in st.session_state.base_ejercicios if e.nombre != ej_eliminar]
            st.success(f"Ejercicio '{ej_eliminar}' eliminado de la base de datos.")

    else:
        st.warning("🔒 Solo el perfil **Profesor / Entrenador** tiene permisos para modificar o agregar ejercicios a la base de datos.")

    # Vista General de la Base
    st.subheader("📚 Catálogo Actual de Ejercicios")
    tabla_datos = [{
        "ID": e.id, "Bloque": e.bloque, "Nombre": e.nombre, "Patrón": e.patron_movimiento,
        "Músculo Principal": e.musculo_principal, "Equipo": e.equipamiento, "Estrés": f"{e.estres_articular}/5", "Video": "Sí" if e.url_video else "No"
    } for e in st.session_state.base_ejercicios]
    st.dataframe(tabla_datos, use_container_width=True)

# PESTAÑA 4: SUSTITUCIÓN RÁPIDA
with tab_remplazo:
    st.subheader("🔄 Sustitución de Ejercicio Ocupado o Con Molestia")
    ej_sel = st.selectbox("Selecciona el ejercicio a cambiar:", [e.nombre for e in st.session_state.base_ejercicios])
    if st.button("Buscar Alternativa Inteligente"):
        obj_ej = next(e for e in st.session_state.base_ejercicios if e.nombre == ej_sel)
        reemplazo = MotorEntrenamiento.sustituir_ejercicio(obj_ej, atleta.equipamiento_disponible)
        if reemplazo:
            st.success(f"✔️ **Sustituto Sugerido:** {reemplazo.nombre}")
            st.write(f"- **Bloque:** {reemplazo.bloque} | **Equipo:** {reemplazo.equipamiento} | **Estrés Articular:** {reemplazo.estres_articular}/5")
            if reemplazo.url_video: st.video(reemplazo.url_video)
        else: st.warning("No hay alternativas disponibles para el equipamiento seleccionado.")
