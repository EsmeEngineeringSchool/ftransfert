import streamlit as st
import numpy as np
from ftransfert.common.Ftransfert import Ftransfert

# --------------------------------------------------
# Configuration générale de la page
# --------------------------------------------------

st.set_page_config(
    page_title="Diagrammes de Bode – ftransfert",
    layout="wide"
)

st.title("Diagrammes de Bode interactifs")
st.markdown(
    """
    Cette application permet d'explorer l'influence des paramètres
    d'un système linéaire sur son diagramme de Bode.
    """
)

# --------------------------------------------------
# Barre latérale : paramètres physiques
# --------------------------------------------------

st.sidebar.header("Paramètres du système")

R = st.sidebar.slider(
    "Résistance R (Ω)",
    min_value=1.0,
    max_value=1000.0,
    value=100.0,
    step=1.0
)

L = st.sidebar.slider(
    "Inductance L (H)",
    min_value=1e-3,
    max_value=1.0,
    value=0.1,
    format="%.3f"
)

C = st.sidebar.slider(
    "Capacité C (F)",
    min_value=1e-6,
    max_value=1e-1,
    value=1e-3,
    format="%.6f"
)

st.sidebar.markdown("---")

omega_min = st.sidebar.number_input(
    "ω min (rad/s)",
    value=1e-2,
    format="%.2e"
)

omega_max = st.sidebar.number_input(
    "ω max (rad/s)",
    value=1e5,
    format="%.2e"
)

n_points = st.sidebar.slider(
    "Nombre de points",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

# --------------------------------------------------
# Calcul
# --------------------------------------------------

omega = np.logspace(
    np.log10(omega_min),
    np.log10(omega_max),
    n_points
)

# Exemple : fonction de transfert RLC (à adapter à ton API exacte)
H = Ftransfert.from_RLC(R=R, L=L, C=C)

# --------------------------------------------------
# Affichage des résultats
# --------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Diagramme de Bode")

    fig = H.bode_plot(omega=omega)
    st.pyplot(fig)

with col2:
    st.subheader("Informations système")

    st.latex(r"H(p) = \frac{1}{LCp^2 + RCp + 1}")

    st.markdown(f"""
    - **R** = {R:.2f} Ω  
    - **L** = {L:.3f} H  
    - **C** = {C:.6f} F  
    """)

# --------------------------------------------------
# Export
# --------------------------------------------------

st.markdown("---")
st.subheader("Export")

col3, col4 = st.columns(2)

with col3:
    if st.button("Exporter en PNG"):
        fig.savefig("bode.png", dpi=300)
        with open("bode.png", "rb") as f:
            st.download_button(
                "Télécharger bode.png",
                f,
                file_name="bode.png",
                mime="image/png"
            )

with col4:
    if hasattr(H, "bode_tikz"):
        tikz_code = H.bode_tikz(omega=omega)
        st.download_button(
            "Télécharger le code TikZ",
            tikz_code,
            file_name="bode.tex",
            mime="text/plain"
        )

# --------------------------------------------------
# Pied de page pédagogique
# --------------------------------------------------

st.markdown(
    """
    ---
    **Objectif pédagogique :**  
    Comprendre l'influence des paramètres physiques sur la réponse fréquentielle
    d'un système linéaire.
    """
)
