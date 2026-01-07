import streamlit as st
import subprocess 
import numpy as np
import math
from ftransfert.common.utils      import nat2dB, rad2deg
from ftransfert.fromquad.quadRLC import Quad 
from ftransfert.bode.plot import bode as bodeplot
from ftransfert.bode.tikz import bode as bodetikz

def generate_valid_quad(nquad, composants, max_tries=20):
    quad = Quad(nquad, composants)
    for _ in range(max_tries):
        quad.random()
        if deux_composants_differents(quad):
            return quad
    return quad  # fallback acceptable


def deux_composants_differents(quad):
    s=set()
    for c in quad.series+quad.shunts: s |= set(c)
    return len(s) > 1

def estimation_bounds(R,L,C,H):
    w=[R/L,1/(R*C),1/(L*C)**0.5]
    xlim=(10**round(math.log10(min(w)/1000)),10**round(math.log10(1000*max(w))))
    g,p=[],[]
    for wi in w:
        pow10_w = 10**round(math.log10(wi/10))
        _,gw,pw=H.eval(pow10_w*1j)
        g.append(nat2dB(gw))
        p.append(rad2deg(pw))
    _,gm,pm=H.eval(1j*(xlim[1]*xlim[0])**0.5)
    g.append(nat2dB(gm))
    p.append(rad2deg(pm))
    _,gmi,pmi=H.eval(1j*xlim[0])
    g.append(nat2dB(gmi))
    p.append(rad2deg(pmi))
    _,gma,pma=H.eval(1j*xlim[1])
    g.append(nat2dB(gma))
    p.append(rad2deg(pma))
    g.sort()
    p.sort()
    print(p)
    g0f,g1f=math.floor(g[0]/10)*10-20,math.ceil(g[-1]/10)*10+40
    p0f,p1f=math.floor(p[0]/90)*90,math.ceil(p[-1]/90)*90
    return xlim,(g0f,g1f),(p0f,p1f) 

# --------------------------------------------------
# Configuration générale de la page
# --------------------------------------------------
st.set_page_config(
    page_title="Diagrammes de Bode – ftransfert",
    layout="wide"
)
st.title("*ftransfert* et *quadRLC* -- Applications")
st.markdown(
    """
    Cette application web (Streamlit) permet d'explorer l'influence des paramètres
    d'un quadripole linéaire sur son diagramme de Bode.
    """
)

st.sidebar.header("Paramètres du système")

nquad = st.sidebar.number_input("Nombre de quadripôles", min_value=1, value=2)
composants = st.sidebar.selectbox("Type de composants", ["RL", "LC", "RC", "RLC"])
if ("nquad" not in st.session_state
    or "composants" not in st.session_state
    or "quad" not in st.session_state
    or st.session_state.nquad != nquad
    or st.session_state.composants != composants):
    quad = generate_valid_quad(nquad, composants)
    st.session_state.quad = quad
    st.session_state.nquad = nquad
    st.session_state.composants = composants


R,L,C=1,1,1

if "R" in composants :
    Rpower = st.sidebar.slider(
        "Résistance R (Ω)",
        min_value=0.0,
        max_value=4.0,
        value=2.0,
        step=0.25
    )
    R=10**Rpower

if "L" in composants :
    Lpower = st.sidebar.slider(
            "Inductance L (H)",
            min_value=-3.0,    
            max_value=0.0,    
            value=-1.0,
            step=0.25,
            )
    L=10**Lpower

if "C" in composants :
    Cpower = st.sidebar.slider(
            "Capacité C (F) ordre de grandeur",
            min_value=-6,
            max_value=0,
            value=-3,
            step=1,
            )
    C=10**Cpower

if st.sidebar.button("Nouveau circuit"):
    quad = generate_valid_quad(nquad, composants)
    st.session_state.quad = quad

quad = st.session_state.quad
H=quad.get_ftransfert_from_RLC(R,C,L)
print(H)
xlim,y1lim,y2lim=estimation_bounds(R,L,C,H)
# --------------------------------------------------
# Affichage des résultats
# --------------------------------------------------
col1, col2 = st.columns([1, 2])
with col1:
    fig = bodeplot(H,xlim=xlim,y1lim=y1lim,y2lim=y2lim,n=1024)
    fig.savefig("bode.png", dpi=150)
    st.image("bode.png",width=500)

with col2:
    st.subheader("Informations système")
    
    with open("quad.tex","w") as f:
        print(quad.standalone(),file=f)
    result = subprocess.run( ["pdflatex","-shell-escape", "quad.tex"], capture_output=True)
    if result.returncode : print("erreur de compilation pdflatex")
    st.image("quad.png",width=500)
    st.latex(f"H(p)= {quad.get_latex()}")

    out=[]
    if "R" in composants : out+=[f"- **R** = {R:.2f} Ω"]
    if "L" in composants : out+=[f"- **L** = {L:.3f} H"]
    if "C" in composants : out+=[f"- **C** = {C:.6f} F"]
    st.markdown("\n".join(out))
    st.latex(rf"{H.latex()}")
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
    if st.button("Exporter en PDF (PGF/Tikz)"):
        basename="example_bodetikz_1"
        bodetikz(H,filename=f"{basename}.tex",xlim=xlim,y1lim=y1lim,y2lim=y2lim)
        result = subprocess.run( ["pdflatex", f"{basename}.tex"], capture_output=True)
        if result.returncode : print("erreur de compilation pdflatex")
        with open(f"{basename}.pdf", "rb") as f:
            st.download_button(
                "Télécharger le pdf TikZ",
                f,
                file_name=f"{basename}.pdf",
                mime="text/pdf"
            )
