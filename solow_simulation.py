import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider


def simulazione_solow(s=0.2, n=0.02, g=0.02, delta=0.05, alpha=0.3):
    """Simula la dinamica del modello di Solow e mostra grafici interattivi."""
    # Parametri temporali
    T = 100
    k = np.zeros(T)
    y = np.zeros(T)

    # Condizione iniziale (capitale pro-capite iniziale)
    k[0] = 1.0

    # Simulazione dinamica
    for t in range(1, T):
        # Funzione di produzione: y = k^alpha
        y[t - 1] = k[t - 1] ** alpha
        # Equazione di accumulazione: k_dot = s*f(k) - (n + g + delta)*k
        investimento = s * y[t - 1]
        deprezzamento_allargato = (n + g + delta) * k[t - 1]
        k[t] = k[t - 1] + investimento - deprezzamento_allargato

    # Calcolo dello Stato Stazionario teorico (k*)
    k_star = (s / (n + g + delta)) ** (1 / (1 - alpha))

    # Grafico
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(k, label='Capitale per lavoro effettivo (k)')
    plt.axhline(y=k_star, color='r', linestyle='--', label=f'Stato Stazionario: {k_star:.2f}')
    plt.title("Transizione verso lo Stato Stazionario")
    plt.xlabel("Tempo")
    plt.legend()

    plt.subplot(1, 2, 2)
    k_range = np.linspace(0, k_star * 1.5, 100)
    plt.plot(k_range, s * k_range ** alpha, label=r'Risparmio/Investimento ($s \cdot f(k)$)', color='blue')
    plt.plot(k_range, (n + g + delta) * k_range, label=r'Rimpiazzo ($(n+g+\delta) \cdot k$)', color='red')
    plt.title("Modello di Solow: Equilibrio")
    plt.xlabel("Capitale (k)")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    interact(
        simulazione_solow,
        s=FloatSlider(value=0.2, min=0.01, max=0.5, step=0.01, description='Risparmio (s)'),
        n=FloatSlider(value=0.02, min=0.0, max=0.1, step=0.01, description='Popolazione (n)'),
        g=FloatSlider(value=0.02, min=0.0, max=0.1, step=0.01, description='Innovazione (g)'),
        delta=FloatSlider(value=0.05, min=0.01, max=0.2, step=0.01, description='Deprezz. (δ)'),
        alpha=FloatSlider(value=0.3, min=0.1, max=0.7, step=0.05, description='Produttività (α)'),
    )
