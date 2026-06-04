import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mapa GPS",
    layout="wide"
)

st.title("Mapa de Rota GPS")

st.write("Carregue o arquivo LOGGPS.CSV gerado pelo Arduino.")

arquivo = st.file_uploader(
    "Selecione o CSV",
    type=["csv"]
)

# =========================================================
# FUNÇÃO CARREGAR CSV
# =========================================================

def carregar_csv(arquivo):

    df = pd.read_csv(
        arquivo,
        sep=";"
    )

    df.columns = df.columns.str.strip()

    # Remove SEM_FIX

    if "Latitude" in df.columns:
        df = df[df["Latitude"] != "SEM_FIX"]

    if "Longitude" in df.columns:
        df = df[df["Longitude"] != "SEM_FIX"]

    # Converte coordenadas

    df["Latitude"] = pd.to_numeric(
        df["Latitude"],
        errors="coerce"
    )

    df["Longitude"] = pd.to_numeric(
        df["Longitude"],
        errors="coerce"
    )

    # Remove inválidos

    df = df.dropna(
        subset=["Latitude", "Longitude"]
    )

    return df

# =========================================================
# PROCESSAMENTO
# =========================================================

if arquivo is not None:

    df = carregar_csv(arquivo)

    if df.empty:
        st.warning("Nenhuma coordenada válida encontrada.")
        st.stop()

    st.success(f"{len(df)} coordenadas carregadas.")

    # =====================================================
    # CENTRO DO MAPA
    # =====================================================

    centro_lat = df["Latitude"].mean()
    centro_lon = df["Longitude"].mean()

    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=15,
        tiles="OpenStreetMap"
    )

    # =====================================================
    # PONTOS
    # =====================================================

    pontos = list(
        zip(
            df["Latitude"],
            df["Longitude"]
        )
    )

    # =====================================================
    # LINHA DA ROTA
    # =====================================================

    folium.PolyLine(
        pontos,
        weight=5,
        opacity=0.8,
        tooltip="Rota percorrida"
    ).add_to(mapa)

    # =====================================================
    # MARCADOR INÍCIO
    # =====================================================

    folium.Marker(
        pontos[0],
        popup="Início da rota",
        tooltip="Início"
    ).add_to(mapa)

    # =====================================================
    # MARCADOR FIM
    # =====================================================

    folium.Marker(
        pontos[-1],
        popup="Fim da rota",
        tooltip="Fim"
    ).add_to(mapa)

    # =====================================================
    # MARCADORES DOS PONTOS
    # =====================================================

    for _, row in df.iterrows():

        popup = f"""
        <b>Data:</b> {row.get('Data', '')}<br>
        <b>Hora:</b> {row.get('Hora', '')}<br>
        <b>Latitude:</b> {row.get('Latitude', '')}<br>
        <b>Longitude:</b> {row.get('Longitude', '')}
        """

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=3,
            popup=popup,
            fill=True
        ).add_to(mapa)

    # =====================================================
    # EXIBE MAPA
    # =====================================================

    st.subheader("Mapa da rota")

    st_folium(
        mapa,
        width=None,
        height=650
    )

    # =====================================================
    # TABELA LINKS
    # =====================================================

    st.subheader("Links Google Maps")

    html = """
    <table style="
        width:100%;
        border-collapse: collapse;
        font-family: Arial;
    ">
    <tr style="background-color:#dddddd;">
        <th style="padding:8px;">Data</th>
        <th style="padding:8px;">Hora</th>
        <th style="padding:8px;">Latitude</th>
        <th style="padding:8px;">Longitude</th>
        <th style="padding:8px;">Mapa</th>
        <th style="padding:8px;">Copiar</th>
    </tr>
    """

    for _, row in df.iterrows():

        link = row.get("GoogleMaps", "")

        html += f"""
        <tr>
            <td style="padding:8px;">{row.get("Data","")}</td>
            <td style="padding:8px;">{row.get("Hora","")}</td>
            <td style="padding:8px;">{row.get("Latitude","")}</td>
            <td style="padding:8px;">{row.get("Longitude","")}</td>

            <td style="padding:8px;">
                <a href="{link}" target="_blank">
                    Abrir mapa
                </a>
            </td>

            <td style="padding:8px;">
                <button
                    onclick="navigator.clipboard.writeText('{link}')">
                    Copiar link
                </button>
            </td>
        </tr>
        """

    html += "</table>"

    components.html(
        html,
        height=400,
        scrolling=True
    )

    # =====================================================
    # DATAFRAME
    # =====================================================

    st.subheader("Dados carregados")

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("Aguardando upload do arquivo CSV.")
