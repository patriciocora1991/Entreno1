import streamlit as st

# Configuración de pantalla
st.set_page_config(page_title="Planificador de Alumnos", layout="wide")

# Base de datos estructurada
rutina = {
    "Semana 1": {
        "Día 1": [
            {
                "nombre": "Press de Banca con Barra",
                "series": 4,
                "reps": "10-12",
                "notas": "Codos a 45° del cuerpo. Bajada controlada.",
                "video": "https://www.youtube.com/watch?v=gRVjAtPip0E"
            },
            {
                "nombre": "Extensión de Tríceps en Polea",
                "series": 3,
                "reps": "12-15",
                "notas": "Mantener codos pegados al torso.",
                "video": "https://www.youtube.com/watch?v=vB5OHsJ3EME"
            }
        ],
        "Día 2": [
            {
                "nombre": "Dominadas Asistidas / Jalón",
                "series": 4,
                "reps": "8-10",
                "notas": "Retraer escápulas antes de tirar.",
                "video": "https://www.youtube.com/watch?v=CAwf7n6Luuc"
            }
        ],
        "Día 3": [
            {
                "nombre": "Sentadilla Trasera",
                "series": 4,
                "reps": "8",
                "notas": "Romper el paralelo de forma segura.",
                "video": "https://www.youtube.com/watch?v=ultWZbUMPL8"
            }
        ]
    },
    "Semana 2": {
        "Día 1": [
            {
                "nombre": "Press Inclinado con Mancuernas",
                "series": 4,
                "reps": "8-10",
                "notas": "Aumentar peso respecto a la Semana 1.",
                "video": "https://www.youtube.com/watch?v=8iPEnn-ltC8"
            }
        ]
    }
}

# Panel lateral de control
st.sidebar.title("Panel de Control")
semana_sel = st.sidebar.selectbox("Seleccionar Semana", list(rutina.keys()))
vista = st.sidebar.radio("Modo de Vista", ["Vista Diaria (con Videos)", "Esquema Semanal Completo"])

st.title(f"Planificación: {semana_sel}")

# VISTA 1: Navegación de Días y Videos
if vista == "Vista Diaria (con Videos)":
    dias_disponibles = list(rutina[semana_sel].keys())
    
    # Navegación sin bloqueos entre cualquier día
    dia_sel = st.radio("Seleccionar Día:", dias_disponibles, horizontal=True)
    st.divider()

    ejercicios = rutina[semana_sel][dia_sel]
    
    for ex in ejercicios:
        col_info, col_video = st.columns([1, 1])
        
        with col_info:
            st.subheader(ex["nombre"])
            st.markdown(f"**Series:** {ex['series']} | **Repeticiones:** {ex['reps']}")
            st.info(f"**Indicaciones:** {ex['notas']}")
            
        with col_video:
            # Renderiza el reproductor de video directamente desde Python
            st.video(ex["video"])
            
        st.divider()

# VISTA 2: Esquema Semanal General para Optimización
else:
    st.subheader("Vista Panorámica de la Semana")
    dias = rutina[semana_sel]
    columnas = st.columns(len(dias))
    
    for idx, (nombre_dia, lista_ejercicios) in enumerate(dias.items()):
        with columnas[idx]:
            st.markdown(f"### {nombre_dia}")
            for ex in lista_ejercicios:
                st.markdown(f"• **{ex['nombre']}**  \n*{ex['series']} series x {ex['reps']} reps*")
            st.divider()
