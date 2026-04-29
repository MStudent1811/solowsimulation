import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configurazione Pagina
st.set_page_config(page_title="Simulatore Crescita Economica", layout="wide")

st.title("📈 Simulatore di Crescita: Esogena vs Endogena")

# --- SIDEBAR PER PARAMETRI COMUNI ---
st.sidebar.header("Parametri Comuni")
s = st.sidebar.slider("Saggio di Risparmio (s)", 0.01, 0.50, 0.20)
n = st.sidebar.slider("Crescita Popolazione (n)", 0.0, 0.05, 0.01)
delta = st.sidebar.slider("Deprezzamento (δ)", 0.01, 0.10, 0.05)

st.sidebar.divider()

# --- SCELTA DEL MODELLO ---
tipo_modello = st.sidebar.radio("Seleziona il Modello", ["Esogeno (Solow Standard)", "Endogeno (Modello AK)"])

T = 100
k = np.zeros(T)
k[0] = 1.0  # Capitale iniziale

if tipo_modello == "Esogeno (Solow Standard)":
    st.sidebar.subheader("Parametri Solow (Rendimenti Decrescenti)")
    alpha = st.sidebar.slider("Produttività Capitale (α)", 0.1, 0.7, 0.33)
    g = st.sidebar.slider("Tasso di Innovazione Esogena (g)", 0.0, 0.05, 0.02)
    desc = "Modello di Solow: La curva dell'investimento è curva (rendimenti decrescenti). Si arriva sempre a uno Stato Stazionario."
    
    # Dinamica Solow
    for t in range(1, T):
        y_t = k[t-1]**alpha
        k[t] = k[t-1] + s * y_t - (n + g + delta) * k[t-1]

else:
    st.sidebar.subheader("Parametri Endogeni (Conoscenza)")
    istruzione = st.sidebar.slider("Investimento in Istruzione/R&S", 0.0, 0.50, 0.10)
    efficienza = st.sidebar.slider("Efficienza del Sistema", 0.1, 2.0, 1.0)
    
    # Nel modello AK, la produttività A dipende dalla conoscenza accumulata
    A = 1.0 + (istruzione * efficienza)
    desc = "Modello Endogeno (AK): L'istruzione crea conoscenza condivisa. La curva dell'investimento diventa retta: se supera il deprezzamento, la crescita è infinita!"
    
    # Dinamica Endogena (AK)
    for t in range(1, T):
        y_t = A * k[t-1]
        k[t] = k[t-1] + s * y_t - (n + delta) * k[t-1]

# --- VISUALIZZAZIONE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Evoluzione del Capitale (k)")
    fig1, ax1 = plt.subplots()
    ax1.plot(k, color='#1f77b4', linewidth=2)
    ax1.set_xlabel("Tempo")
    ax1.set_ylabel("Capitale")
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

with col2:
    st.subheader("Analisi dell'Equilibrio")
    fig2, ax2 = plt.subplots()
    k_range = np.linspace(0.1, max(k)*1.2 if max(k) < 50 else 50, 100)
    
    # Calcolo delle linee per il grafico a destra in base al modello
    if tipo_modello == "Esogeno (Solow Standard)":
        inv_line = s * (k_range**alpha)
        dep_line = (n + g + delta) * k_range
    else:
        inv_line = s * A * k_range
        dep_line = (n + delta) * k_range
        
    ax2.plot(k_range, inv_line, label="Investimento", color='green')
    ax2.plot(k_range, dep_line, label="Rimpiazzo", color='red')
    ax2.set_xlabel("Capitale (k)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

st.info(f"**Analisi:** {desc}")
