import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Analizador de Encuestas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analizador de Encuestas")

# =====================================
# CARGA DE DATOS
# =====================================

archivo = st.file_uploader(
    "Cargar otro archivo CSV (opcional)",
    type=["csv"]
)

try:

    if archivo is not None:
        df = pd.read_csv(
            archivo,
            header=None,
            encoding="latin1"
        )
        st.success("Archivo cargado por el usuario")

    else:
        df = pd.read_csv(
            "PDJS.csv",
            header=None,
            encoding="latin1"
        )
        st.info("Mostrando archivo predeterminado: PDJS.csv")

except Exception as e:

    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# =====================================
# ANÁLISIS
# =====================================

numero = 1

for col in range(0, df.shape[1], 3):

    try:

        pregunta = str(df.iloc[0, col])

        if pd.isna(df.iloc[0, col]):
            continue

        respuestas = []

        for fila in range(2, len(df)):

            respuesta = df.iloc[fila, col]

            if col + 1 >= df.shape[1]:
                continue

            frecuencia = df.iloc[fila, col + 1]

            if pd.isna(respuesta):
                continue

            if pd.isna(frecuencia):
                continue

            respuestas.append([
                str(respuesta),
                float(frecuencia)
            ])

        if len(respuestas) == 0:
            continue

        tabla = pd.DataFrame(
            respuestas,
            columns=[
                "Respuesta",
                "Frecuencia"
            ]
        )

        total = tabla["Frecuencia"].sum()

        tabla["Porcentaje"] = (
            tabla["Frecuencia"] /
            total * 100
        ).round(2)

        st.divider()

        st.subheader(f"Pregunta {numero}")
        st.markdown(f"**{pregunta}**")

        # ======================
        # MÉTRICAS
        # ======================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total",
            int(total)
        )

        c2.metric(
            "Máximo",
            int(tabla["Frecuencia"].max())
        )

        c3.metric(
            "Mínimo",
            int(tabla["Frecuencia"].min())
        )

        c4.metric(
            "Promedio",
            round(
                tabla["Frecuencia"].mean(),
                2
            )
        )

        # ======================
        # TABLA
        # ======================

        st.dataframe(
            tabla,
            use_container_width=True
        )

        # ======================
        # GRÁFICAS
        # ======================

        col1, col2 = st.columns(2)

        with col1:

            fig1, ax1 = plt.subplots(
                figsize=(8, 4)
            )

            tabla_barra = tabla.sort_values(
                by="Frecuencia",
                ascending=False
            )

            ax1.bar(
                tabla_barra["Respuesta"],
                tabla_barra["Frecuencia"]
            )

            ax1.set_title("Frecuencias")

            plt.xticks(
                rotation=45,
                ha="right"
            )

            st.pyplot(fig1)

        with col2:

            fig2, ax2 = plt.subplots(
                figsize=(6, 6)
            )

            ax2.pie(
                tabla["Frecuencia"],
                labels=tabla["Respuesta"],
                autopct="%1.1f%%"
            )

            ax2.set_title("Distribución")

            st.pyplot(fig2)

        # ======================
        # DESCARGA
        # ======================

        csv = tabla.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label=f"⬇ Descargar Pregunta {numero}",
            data=csv,
            file_name=f"Pregunta_{numero}.csv",
            mime="text/csv"
        )

        numero += 1

    except Exception as e:

        st.error(
            f"Error procesando la pregunta {numero}: {e}"
        )