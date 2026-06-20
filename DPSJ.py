
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Analizador de Encuestas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analizador de Encuestas")
st.write("Carga un archivo CSV para generar estadísticas y gráficas automáticamente.")

# =====================================
# CARGAR ARCHIVO
# =====================================

archivo = st.file_uploader(
    "Selecciona un archivo CSV",
    type=["csv"]
)

# =====================================
# PROCESAMIENTO
# =====================================

if archivo is not None:

    try:

        df = pd.read_csv(
            archivo,
            header=None,
            encoding="latin1"
        )

        st.success(
            f"Archivo cargado correctamente ({df.shape[0]} filas x {df.shape[1]} columnas)"
        )

        numero = 1

        for col in range(0, df.shape[1], 3):

            try:

                pregunta = str(df.iloc[0, col])

                if pregunta == "nan":
                    continue

                respuestas = []

                for fila in range(2, len(df)):

                    respuesta = df.iloc[fila, col]

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

                # ==========================
                # MÉTRICAS
                # ==========================

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "Total",
                    int(total)
                )

                c2.metric(
                    "Mayor",
                    int(tabla["Frecuencia"].max())
                )

                c3.metric(
                    "Menor",
                    int(tabla["Frecuencia"].min())
                )

                c4.metric(
                    "Promedio",
                    round(
                        tabla["Frecuencia"].mean(),
                        2
                    )
                )

                # ==========================
                # TABLA
                # ==========================

                st.dataframe(
                    tabla,
                    use_container_width=True
                )

                # ==========================
                # GRÁFICAS
                # ==========================

                col1, col2 = st.columns(2)

                # BARRAS
                with col1:

                    tabla_barra = tabla.sort_values(
                        by="Frecuencia",
                        ascending=False
                    )

                    fig1, ax1 = plt.subplots(
                        figsize=(10, 5)
                    )

                    barras = ax1.bar(
                        tabla_barra["Respuesta"],
                        tabla_barra["Frecuencia"]
                    )

                    ax1.set_title(pregunta)

                    plt.xticks(
                        rotation=45,
                        ha="right"
                    )

                    for barra in barras:

                        altura = barra.get_height()

                        ax1.text(
                            barra.get_x()
                            + barra.get_width() / 2,
                            altura,
                            int(altura),
                            ha="center"
                        )

                    st.pyplot(fig1)

                # PASTEL
                with col2:

                    fig2, ax2 = plt.subplots(
                        figsize=(6, 6)
                    )

                    ax2.pie(
                        tabla["Frecuencia"],
                        labels=tabla["Respuesta"],
                        autopct="%1.1f%%"
                    )

                    ax2.set_title(
                        "Distribución"
                    )

                    st.pyplot(fig2)

                # ==========================
                # DESCARGAR TABLA
                # ==========================

                csv = tabla.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label=f"⬇ Descargar resultados Pregunta {numero}",
                    data=csv,
                    file_name=f"Pregunta_{numero}.csv",
                    mime="text/csv"
                )

                numero += 1

            except Exception as e:

                st.error(
                    f"Error en la pregunta {numero}: {e}"
                )

    except Exception as e:

        st.error(
            f"No fue posible leer el archivo: {e}"
)