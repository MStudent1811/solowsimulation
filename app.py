import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configurazione Pagina
st.set_page_config(page_title="Simulatore Crescita Economica", layout="wide")

st.title("📈 Simulatore di Crescita: Esogena vs Endogena")
st.markdown("""
Questa app confronta i due filoni della crescita economica:
- **Prima Fase (Esogena):** L'innovazione arriva dall'esterno.
- **Seconda Fase (Endogena):** L'innovazione è prodotta dal sistema (es. tramite l'istruzione).
""")

# --- SIDEBAR PER PARAMETRI ---
st.sidebar.header("Parametri Comuni")
s = st.sidebar.slider("Saggio di Risparmio (s)", 0.05, 0.50, 0.20, help="Quota di PIL investita in capitale fisico")
n = st.sidebar.slider("Crescita Popolazione (n)", 0.0, 0.05, 0.01)
delta = st.sidebar.slider("Deprezzamento (δ)", 0.01, 0.10, 0.05)
alpha = st.sidebar.slider("Produttività Capitale (α)", 0.1, 0.5, 0.33)

st.sidebar.divider()

# SCELTA DEL MODELLO
tipo_modello = st.sidebar.radio("Seleziona il Modello", ["Esogeno (Solow Standard)", "Endogeno (Teoria dello Sviluppo)"])

if tipo_modello == "Esogeno (Solow Standard)":
    st.sidebar.subheader("Parametri Esogeni")
    g = st.sidebar.slider("Tasso di Innovazione (g)", 0.0, 0.05, 0.02)
    desc = "In questo modello, il progresso tecnologico è un dato esterno."
else:
    st.sidebar.subheader("Parametri Endogeni")
    istruzione = st.sidebar.slider("Investimento in Istruzione/R&S", 0.0, 0.20, 0.05)
    efficienza = st.sidebar.slider("Efficienza del Sistema Innovativo", 0.1, 1.0, 0.4)
    # L'innovazione g diventa endogena: dipende dall'investimento
    g = istruzione * efficienza
    desc = f"L'innovazione (g) è calcolata internamente: g = {g:.3f}"

# --- CALCOLO DELLA DINAMICA ---
T = 100
k = np.zeros(T)
y = np.zeros(T)
k[0] = 1.0  # Capitale iniziale

for t in range(1, T):
    y[t-1] = k[t-1]**alpha
    # Equazione fondamentale: delta_k = s*y - (n + g + delta)*k
    k[t] = k[t-1] + s * y[t-1] - (n + g + delta) * k[t-1]
    # Evitiamo valori negativi per stabilità
    k[t] = max(k[t], 0.1)

y[T-1] = k[T-1]**alpha

# --- VISUALIZZAZIONE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Evoluzione del Capitale (k)")
    fig1, ax1 = plt.subplots()
    ax1.plot(k, color='#1f77b4', linewidth=2)
    ax1.set_xlabel("Tempo")
    ax1.set_ylabel("Capitale per lavoratore")
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

with col2:
    st.subheader("Analisi dello Stato Stazionario")
    fig2, ax2 = plt.subplots()
    k_range = np.linspace(0.1, max(k)*1.5, 100)
    inv_line = s * (k_range**alpha)
    dep_line = (n + g + delta) * k_range
    
    ax2.plot(k_range, inv_line, label="Investimento (s*y)", color='green')
    ax2.plot(k_range, dep_line, label="Rimpiazzo ((n+g+δ)*k)", color='red')
    ax2.set_xlabel("Capitale (k)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

st.info(f"**Analisi:** {desc}")

# --- TABELLA DATI ---
if st.checkbox("Mostra dati numerici"):
    st.write(f"Capitale Finale: {k[-1]:.2f} | Produzione Finale: {y[-1]:.2f}")