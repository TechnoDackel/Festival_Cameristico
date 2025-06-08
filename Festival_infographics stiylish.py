import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from PIL import Image
from datetime import datetime
import folium
from streamlit_folium import st_folium

# --- CARICAMENTO ASSETS (LOGO) ---
# Carica il logo principale del festival
try:
    logo_festival = Image.open('Logo_footprint_.png')
except FileNotFoundError:
    # Se il file non viene trovato, usa un placeholder testuale
    logo_festival = "🎶"
    
# Carica il logo di Quarta    
try:
    quarta_logo_base64 = Image.open('quarta.png')
except FileNotFoundError:
    quarta_logo_base64 = None
    

# --- IMPOSTAZIONI PAGINA ---
st.set_page_config(
    page_title="Festival del Capo di Leuca 2025",
    page_icon=logo_festival, # Logo nella tab del browser
    layout="wide",
)

# --- CSS PERSONALIZZATO ADATTIVO ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

/* Reset e impostazioni base */
* {
    box-sizing: border-box;
}

/* Stili base per il corpo */
body {
    font-family: 'Montserrat', sans-serif;
    transition: all 0.3s ease;
}

/* Stili per tema chiaro */
.stApp {
    background-color: #ffffff;
    color: #2c3e50;
}

/* Tema scuro */
@media (prefers-color-scheme: dark) {
    .stApp {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #85c1e9 !important;
    }
    
    .stCaption {
        color: #bdc3c7 !important;
    }
    
    .stInfo {
        background-color: #34495e !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: #f39c12 !important;
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2c3e50 !important;
        color: #ffffff !important;
        border: 1px solid #566573 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #5dade2 !important;
        color: #ffffff !important;
    }
}

/* Tema chiaro */
@media (prefers-color-scheme: light) {
    .stApp {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }
    
    .stMarkdown {
        color: #2c3e50 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #1a5276 !important;
    }
    
    .stCaption {
        color: #34495e !important;
    }
    
    .stInfo {
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #dddddd !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1a5276 !important;
        color: #ffffff !important;
    }
}

/* Fallback per browser che non supportano prefers-color-scheme */
.stApp {
    background-color: #ffffff;
    color: #2c3e50;
}

.stMarkdown {
    color: #2c3e50;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: #1a5276;
    font-weight: 700;
}

/* Titoli */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    color: #1a5276;
}

/* Streamlit tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: #2c3e50;
    border: 1px solid #dddddd;
}

.stTabs [aria-selected="true"] {
    background-color: #1a5276 !important;
    color: white !important;
}

/* Container metriche */
.metric-container {
    background-color: #ffffff;
    border-left: 10px solid #1a5276;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #dddddd;
}

.metric-value {
    font-size: 5rem;
    font-weight: 700;
    color: #1a5276;
    line-height: 1;
}

.metric-label {
    font-size: 1.2rem;
    color: #2c3e50;
}

/* Container per quattro metriche */
.four-metric-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.single-metric {
    background-color: #ffffff;
    border-left: 10px solid #1a5276;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    flex: 1;
    min-width: 200px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #dddddd;
}

.single-metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a5276;
    line-height: 1;
}

.single-metric-label {
    font-size: 1rem;
    color: #2c3e50;
    margin-top: 0.5rem;
}

/* Tema scuro per metriche */
@media (prefers-color-scheme: dark) {
    .metric-container, .single-metric {
        background-color: #34495e !important;
        border-color: #5dade2 !important;
        border-left-color: #5dade2 !important;
    }
    
    .metric-value, .single-metric-value {
        color: #5dade2 !important;
    }
    
    .metric-label, .single-metric-label {
        color: #ffffff !important;
    }
}

/* Responsive per mobile */
@media (max-width: 768px) {
    .four-metric-container {
        flex-direction: column;
    }
    
    .single-metric {
        margin-bottom: 1rem;
        min-width: unset;
    }
    
    .single-metric-value {
        font-size: 2rem;
    }
    
    .metric-value {
        font-size: 3rem;
    }
}

/* Blockquote */
blockquote {
    border-left: 5px solid #1a5276;
    padding-left: 1.5rem;
    margin-left: 0;
    font-style: italic;
    color: #34495e;
    background-color: #f8f9fa;
    padding: 1rem 1.5rem;
    border-radius: 0 5px 5px 0;
}

@media (prefers-color-scheme: dark) {
    blockquote {
        border-left-color: #5dade2;
        color: #bdc3c7;
        background-color: #34495e;
    }
}

/* Tabella stilizzata */
.styled-table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 20px;
    font-size: 0.9em;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff;
}

.styled-table thead tr {
    background-color: #1a5276;
    color: #ffffff;
    text-align: left;
}

.styled-table th, .styled-table td {
    padding: 12px 15px;
    border: 1px solid #dddddd;
    color: #2c3e50;
}

.styled-table thead th {
    color: #ffffff;
}

.styled-table tbody tr {
    border-bottom: 1px solid #dddddd;
    background-color: #ffffff;
}

.styled-table tbody tr:nth-of-type(even) {
    background-color: #f8f9fa;
}

.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #1a5276;
}

/* Tema scuro per tabelle */
@media (prefers-color-scheme: dark) {
    .styled-table {
        background-color: #34495e;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    }
    
    .styled-table thead tr {
        background-color: #5dade2;
        color: #ffffff;
    }
    
    .styled-table th, .styled-table td {
        border-color: #566573;
        color: #ffffff;
    }
    
    .styled-table tbody tr {
        border-color: #566573;
        background-color: #34495e;
    }
    
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #2c3e50;
    }
    
    .styled-table tbody tr:last-of-type {
        border-bottom-color: #5dade2;
    }
}

/* Card sponsor */
.sponsor-card {
    background: #ffffff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin: 0.5rem;
    border: 1px solid #dddddd;
}

.sponsor-card h4 {
    color: #1a5276;
    margin-bottom: 0.5rem;
}

.sponsor-card p {
    color: #34495e;
    margin: 0;
}

@media (prefers-color-scheme: dark) {
    .sponsor-card {
        background-color: #34495e;
        border-color: #566573;
    }
    
    .sponsor-card h4 {
        color: #5dade2;
    }
    
    .sponsor-card p {
        color: #bdc3c7;
    }
}

/* Fix per iframe mappa */
iframe {
    display: block;
    margin-bottom: 0 !important;
    border-radius: 8px;
}

/* Lista non ordinata */
ul, ol {
    color: #2c3e50;
}

ul li, ol li {
    color: #2c3e50;
    margin-bottom: 0.5rem;
}

@media (prefers-color-scheme: dark) {
    ul, ol, ul li, ol li {
        color: #ffffff;
    }
}

/* Small text */
small {
    color: #34495e;
}

@media (prefers-color-scheme: dark) {
    small {
        color: #bdc3c7;
    }
}

/* Stili per i link */
a {
    color: #3498db;
}

a:hover {
    color: #1a5276;
}

@media (prefers-color-scheme: dark) {
    a {
        color: #85c1e9;
    }
    
    a:hover {
        color: #5dade2;
    }
}

/* Footer styling */
.footer-container {
    text-align: center;
    padding: 2rem;
    background: #f8f9fa;
    border-radius: 10px;
    margin-top: 2rem;
    border: 1px solid #dddddd;
}

.footer-container h3 {
    color: #1a5276;
}

.footer-container p {
    color: #2c3e50;
}

@media (prefers-color-scheme: dark) {
    .footer-container {
        background-color: #34495e;
        border-color: #566573;
    }
    
    .footer-container h3 {
        color: #5dade2;
    }
    
    .footer-container p {
        color: #ffffff;
    }
}

/* Separatori */
hr {
    border-color: #dddddd;
    opacity: 0.5;
}

@media (prefers-color-scheme: dark) {
    hr {
        border-color: #566573;
    }
}

/* Media query per schermi molto piccoli */
@media (max-width: 480px) {
    .single-metric-value {
        font-size: 1.8rem;
    }
    
    .single-metric-label {
        font-size: 0.9rem;
    }
    
    .styled-table {
        font-size: 0.8em;
    }
    
    .styled-table th, .styled-table td {
        padding: 8px 10px;
    }
}

/* Assicurati che i grafici Plotly si adattino al tema */
.js-plotly-plot .plotly .modebar {
    background: transparent !important;
}

/* Stile per elementi di Streamlit che potrebbero non rispettare il tema */
.element-container {
    color: inherit;
}

.stDataFrame {
    background-color: transparent;
}

.stDataFrame table {
    background-color: transparent;
}

/* Forza il tema sui componenti specifici */
@media (prefers-color-scheme: dark) {
    .stDataFrame table {
        background-color: #34495e !important;
        color: #ffffff !important;
    }
    
    .stDataFrame th {
        background-color: #5dade2 !important;
        color: #ffffff !important;
    }
    
    .stDataFrame td {
        background-color: #34495e !important;
        color: #ffffff !important;
    }
}

/* --- FOOTER FINALE STILIZZATO --- */
.final-footer {
    text-align: center;
    padding: 2rem;
    margin-top: 2rem;
    background-color: var(--secondary-background-color);
    border-radius: 10px;
}

.final-footer .footer-content {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px; /* Spazio tra testo e logo */
    flex-wrap: wrap; /* Permette di andare a capo su schermi piccoli */
}

.final-footer .footer-text {
    color: var(--text-color);
    opacity: 0.7;
    font-size: 0.9rem;
}

.final-footer .footer-logo {
    max-height: 45px; /* Altezza del logo partner */
    opacity: 0.9;
}

</style>
""", unsafe_allow_html=True)

# --- DATI ---
# Dati storici e previsioni (basati sul documento originale)
data = {
    'Anno': [2023, 2024, 2025],
    'Pubblico in Presenza': [3000, 3200, 3800],
    'Copertura Totale': [0, 1782873, 2200000],  # 2023 non disponibile, 2024: FB 382873 + IG 1.4M
    'Copertura Facebook': [0, 382873, 450000],
    'Copertura Instagram': [0, 1400000, 1750000],
    'Eventi Totali': [30, 18, 34],  # 2023: 21+6+3, 2024: 18, 2025: 24+10
    'Comuni Coinvolti': [17, 11, 16]
}
df_historical = pd.DataFrame(data)

# Coordinate per la mappa (dal documento originale)
locations_2025 = {
    "Alessano": [39.8967, 18.3258],
    "Andrano": [40.0053, 18.3675],
    "Castrignano del Capo": [39.8458, 18.3597],
    "Corsano": [39.9036, 18.3864],
    "Diso": [40.0444, 18.4069],
    "Gagliano del Capo": [39.8347, 18.3683],
    "Lecce": [40.3515, 18.1750],
    "Matino": [40.0367, 18.1206],
    "Morciano di Leuca": [39.8544, 18.3575],
    "Presicce-Acquarica": [39.9097, 18.2653],
    "Salve": [39.9167, 18.3167],
    "Specchia": [39.9656, 18.3053],
    "Taurisano": [39.9678, 18.2294],
    "Taviano": [40.0072, 18.0781],
    "Tricase": [39.9333, 18.3583],
    "Ugento": [39.9167, 18.1667]
}

locations_potential = {
    "Taranto": [40.4762, 17.2297],
    "Bari": [41.1177, 16.8719],
    "Barletta (BAT)": [41.3203, 16.2844]
}

# Lista comuni 2025
comuni_2025 = list(locations_2025.keys())

# --- TITOLO E HEADER ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    # Mostra il logo principale
    if isinstance(logo_festival, Image.Image):
        st.image(logo_festival, width=150)

with col_title:
    st.title("Festival del Capo di Leuca 2025")
    st.markdown("### 20 luglio - 7 settembre 2025")

st.markdown("### Impatto, portata e opportunità di un evento culturale in crescita esponenziale")
st.markdown("---")

# --- SEZIONE 1: PREVISIONI DI IMPATTO 2025 ---
st.header("1. Previsioni di Impatto per il 2025")

# Metriche principali in quattro colonne
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="single-metric">
        <div class="single-metric-value">3.800</div>
        <div class="single-metric-label">👥 Pubblico in Presenza</div>
        <small style="color: #27ae60;">+18.7% vs 2024</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="single-metric">
        <div class="single-metric-value">2.2 Mln</div>
        <div class="single-metric-label">📱 Copertura Digitale</div>
        <small style="color: #27ae60;">+23.4% vs 2024</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="single-metric">
        <div class="single-metric-value">34</div>
        <div class="single-metric-label">🎵 Eventi Totali</div>
        <small>24 concerti + 10 masterclass</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="single-metric">
        <div class="single-metric-value">16</div>
        <div class="single-metric-label">🏘️ Comuni Coinvolti</div>
        <small style="color: #27ae60;">+45% vs 2024</small>
    </div>
    """, unsafe_allow_html=True)

# Spiegazione della copertura
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Cos'è la 'Copertura'?")
    st.markdown("""
    > La copertura (o "reach") è il numero totale di utenti unici che hanno visualizzato un contenuto del festival sui social media.
    """)

with col2:
    st.subheader("Strategia di Crescita")
    st.markdown("""
    Per il 2025 si sta investendo in una campagna social ancora più capillare, con **campagne Instagram ADS geolocalizzate per ogni evento** e strategie di interazione diretta per incentivare la condivisione e la partecipazione del pubblico.
    """)

st.markdown("---")

# --- GRAFICI STORICI ---
st.subheader("Andamento Storico (2023-2025)")

tab1, tab2, tab3 = st.tabs(["📊 Grafico di Crescita", "📱 Copertura per Piattaforma", "📋 Dati Dettagliati"])

with tab1:
    st.markdown("##### **Andamento Pubblico in Presenza**")
    st.markdown("Un aumento costante del pubblico partecipante agli eventi, con una crescita stimata del **+18.75%** per il 2025.")

    fig_audience = px.line(
        df_historical, x='Anno', y='Pubblico in Presenza',
        markers=True, text=df_historical['Pubblico in Presenza'],
        labels={'Pubblico in Presenza': 'Numero di Persone', 'Anno': 'Anno del Festival'}
    )
    fig_audience.update_traces(textposition="top center", line=dict(color='#1a5276', width=4))
    fig_audience.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis_title="Pubblico in Presenza",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig_audience, use_container_width=True)

    st.markdown("##### **Andamento Copertura Social**")
    st.markdown("Una crescita esplosiva della visibilità online, trainata dagli investimenti strategici su Instagram.")

    # Solo per 2024 e 2025 (2023 non disponibile)
    df_copertura = df_historical[df_historical['Anno'] >= 2024].copy()

    fig_reach = px.line(
        df_copertura, x='Anno', y='Copertura Totale',
        markers=True,
        text=df_copertura['Copertura Totale'].apply(lambda x: f"{x/1000000:.1f}M" if x > 1000000 else f"{x/1000:.0f}K"),
        labels={'Copertura Totale': 'Utenti Unici Raggiunti', 'Anno': 'Anno del Festival'}
    )
    fig_reach.update_traces(textposition="top center", line=dict(color='#d35400', width=4))
    fig_reach.update_layout(
        xaxis=dict(tickmode='linear'),
        yaxis_title="Copertura Social (Utenti)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig_reach, use_container_width=True)

with tab2:
    st.markdown("##### **Copertura per Piattaforma Social**")

    # Grafico a barre per Facebook vs Instagram
    fig_platform = go.Figure()

    fig_platform.add_trace(go.Bar(
        name='Facebook',
        x=['2024', '2025 (Prev.)'],
        y=[382873, 450000],
        marker_color='#1877f2',
        text=[f"{382873/1000:.0f}K", f"{450000/1000:.0f}K"],
        textposition='auto'
    ))

    fig_platform.add_trace(go.Bar(
        name='Instagram',
        x=['2024', '2025 (Prev.)'],
        y=[1400000, 1750000],
        marker_color='#E4405F',
        text=['1.4M', '1.75M'],
        textposition='auto'
    ))

    fig_platform.update_layout(
        title='Copertura per Piattaforma Social',
        xaxis_title='Anno',
        yaxis_title='Utenti Raggiunti',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )

    st.plotly_chart(fig_platform, use_container_width=True)

    st.info("📈 **Nota**: Si sta investendo in una campagna più capillare sui social media per massimizzare la reach e l'engagement del pubblico.")

with tab3:
    st.markdown("##### **Riepilogo Dati Storici e Previsionali**")
    st.markdown("I dati del 2023 e 2024 mostrano una forte crescita, che è alla base delle stime per il 2025.")

    # Formattazione controllata per evitare virgole negli anni
    st.dataframe(
        df_historical.style.format({
            "Pubblico in Presenza": "{:,.0f}",
            "Copertura Totale": "{:,.0f}",
            "Copertura Facebook": "{:,.0f}",
            "Copertura Instagram": "{:,.0f}",
            "Eventi Totali": "{:.0f}",
            "Comuni Coinvolti": "{:.0f}"
        }).set_properties(**{'text-align': 'left'}).set_table_styles([
            dict(selector='th', props=[('text-align', 'left')])
        ]),
        use_container_width=True
    )

st.markdown("---")

# --- SEZIONE 2: MAPPA DEGLI EVENTI 2025 ---
st.header("2. Mappa degli Eventi 2025")
st.markdown("il festival 2025 si distribuirà su 16 comuni salentini, creando una rete culturale capillare. Inoltre, per il prossimo futuro prevediamo la flessibilità di organizzare eventi in **altre province pugliesi** su richiesta degli sponsor.")

# Creazione della mappa
m = folium.Map(
    location=[40.35, 18.35], 
    zoom_start=8, 
    tiles=None
)

# Aggiunta di tile più colorata
folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, '
         '&copy; <a href="https://cartodb.com/attributions">CartoDB</a>',
    name='Humanitarian OpenStreetMap',
    control=True
).add_to(m)

# Aggiunta pin rossi (eventi 2025)
for city, coord in locations_2025.items():
    folium.Marker(
        location=coord,
        popup=f"<b>{city}</b>",
        tooltip=city,
        icon=folium.Icon(color="red", icon="music", prefix="fa"),
    ).add_to(m)

# Aggiunta pin blu (località potenziali)
for city, coord in locations_potential.items():
    folium.Marker(
        location=coord,
        popup=f"<b>{city}</b><br>Evento organizzabile",
        tooltip=city,
        icon=folium.Icon(color="blue", icon="star", prefix="fa"),
    ).add_to(m)

# Visualizzazione della mappa in Streamlit
st_folium(m, use_container_width=True, height=500)
st.markdown("""
<ul>
    <li><span style="color:red;">📍</span> <b>Pin Rossi</b>: Comuni che ospiteranno gli eventi del 2025. </li>
    <li><span style="color:blue;">⭐</span> <b>Pin Blu</b>: Province dove è possibile organizzare eventi in partnership.</li>
</ul>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**🔴 Eventi Confermati 2025**: " + ", ".join(comuni_2025))
with col2:
    st.markdown("**🔵 Eventi Possibili**: Si possono organizzare eventi anche a " + ", ".join(locations_potential.keys()))

st.markdown("---")

# --- SEZIONE 3: MAIN SPONSORS ---
st.header("3. Main Sponsors")
st.markdown("Il festival è reso possibile grazie al supporto di partner istituzionali e locali.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        st.image("./Regione_Puglia.jpg", width=200)
    except:
        st.warning("Logo Regione Puglia mancante")

with col2:
    try:
        st.image("./SIAE_logo.png", width=240)
    except:
        st.warning("Logo SIAE mancante")

with col3:
    st.markdown("""
    <div class="sponsor-card">
        <h4>🏘️ Comuni del Salento</h4>
        <p>16 Amministrazioni</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="sponsor-card">
        <h4>🤝 Partner Commerciali</h4>
        <p>Opportunità Aperte</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("#### I 16 Comuni aderenti:")
st.caption("Alessano, Andrano, Castrignano del Capo, Corsano, Diso, Gagliano del Capo, Lecce, Matino, Morciano di Leuca, Presicce-Acquarica, Salve, Specchia, Taurisano, Taviano, Tricase, Ugento")

st.markdown("---")

# --- SEZIONE 4: OPPORTUNITÀ DI SPONSORIZZAZIONE ---
st.header("4. Opportunità di Sponsorizzazione")
st.markdown("Associa il tuo brand a un evento culturale di prestigio, con un pubblico in presenza stimato di **3.800 persone** e una visibilità online di milioni di utenti.")

with st.container():
    st.subheader("Pacchetti di Sponsorizzazione")

    # Tabella HTML per styling personalizzato
    sponsorship_html = """
    <table class="styled-table">
        <thead>
            <tr>
                <th>Tipologia di Evento</th>
                <th>1 Evento</th>
                <th>3 Eventi</th>
                <th>5 Eventi</th>
                <th>22 Eventi<br><small>(12 Concerti + 10 Masterclass)</small></th>
                <th>🌟 MAIN SPONSORSHIP<br><small style="font-weight:normal;">(Tutti gli eventi + esclusive)</small></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Concerto</b></td>
                <td>600 €</td>
                <td>1.500 €</td>
                <td>2.500 €</td>
                <td rowspan="2" style="text-align:center; vertical-align:middle; background-color:var(--bg-secondary);"><b>5.000 €</b></td>
                <td rowspan="2" style="text-align:center; vertical-align:middle; background-color:var(--bg-secondary);"><b>10.000 €</b></td>
           </tr>
            <tr>
                <td><b>Masterclass</b></td>
                <td>500 €</td>
                <td>1.200 €</td>
                <td>2.000 €</td>
            </tr>
        </tbody>
    </table>
    """
    st.markdown(sponsorship_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🌟 Esclusive per MAIN SPONSOR")
    st.markdown("""
    Un pacchetto completo per la massima visibilità, che include tutti i 34 eventi (24 concerti e 10 masterclass) e i seguenti benefici:

    - 🏪 **Stand fisico personalizzato** in tutti i 16 comuni
    - 🎬 Presenza nel **teaser video ufficiale** proiettato prima di ogni concerto
    - 📺 **Spot video dedicato** (30–60 secondi) all'inizio di ogni evento
    - 📱 **Campagna social dedicata** con contenuti e link diretto allo sponsor
    - 🎨 **Logo su tutto il materiale ufficiale** (social, stampa, locandine, video)
    - 🎤 **Menzione ufficiale pubblica** in apertura e chiusura degli eventi
    - 📰 **Priorità su tutte le uscite stampa** e i contenuti online
    - 📅 Organizzazione di eventi della campagna 2026 in **località di interesse dello sponsor**
    - 📸 **Cornice con logo sponsor** per foto durante gli eventi
    """)

# --- SEZIONE 5: AZIONI PROMOZIONALI ---
st.header("5. Azioni Promozionali Attive")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Campagna Instagram ADS
    - Geolocalizzata per ogni evento
    - Target mirato sul pubblico interessato
    - Ottimizzazione continua delle performance
    """)

with col2:
    st.markdown("""
    ### 🎁 Codici Sconto Interattivi
    - Rilasciati dopo interazione diretta
    - Incentivano follow e condivisioni
    - Trackable per ROI measurement
    """)

# --- FOOTER ---

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
</div>
""", unsafe_allow_html=True)

# Contenuti del footer posizionati dopo il div vuoto per centrarli
col_footer1, col_footer2, col_footer3 = st.columns([1,2,1])
with col_footer2:
    st.markdown("""
    <div style="text-align: center; padding-top: 1rem;">
        <h3>Festival del Capo di Leuca 2025</h3>
        <p><strong>20 luglio - 7 settembre 2025</strong></p>
        <p>Un'esperienza musicale unica nel cuore della Puglia</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER FINALE  ---
st.markdown("---")

col_left, col_mid, col_right = st.columns([2, 3, 1])

with col_left:
    st.caption("Made with ❤️ by Bernardo Sbarro, powered by the finest coffee ☕")
    try:
        # Assicurati che il file 'quarta.jpg' sia nella stessa cartella
        st.image("quarta.png", width=75)
    except FileNotFoundError:
        st.caption("_(Logo Quarta Caffè mancante)_")
