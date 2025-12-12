# ========================================================== 
# header du fichier tex avec le chargement des paquets 
# ========================================================== 
article="""\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Fichier généré par bodePGFtikz.py !
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\documentclass{article}
\\usepackage[francais]{babel}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{amsmath}
\\usepackage{amsthm}
\\usepackage{amssymb}
\\usepackage{pgf,tikz}
\\usepackage{pgfplots}
\\usepackage{siunitx}
\\usepackage{geometry}
\\usepackage{mymath}
\\geometry{
paperwidth=21cm,
paperheight=29.7cm,
margin=1cm
}
\\usepackage{tabularx}
\\newcolumntype{K}[1]{>{\centering\\arraybackslash}p{#1}}
\\newcolumntype{M}[1]{>{\centering\\arraybackslash}m{#1}}
\\newcolumntype{N}{@{}m{0pt}@{}}
"""

# quelques variables relatives à LaTeX
begindoc="""\\begin{document}
\\thispagestyle{empty}
"""
begincenter="\\begin{center}\n"
begintikz="\\begin{tikzpicture}[trim axis left]\n"
beginaxis="\\begin{axis}"
axis_braket="]\n"
label_gain="ylabel={Gain (\si{\decibel})},\n"
label_phase="""xlabel={Pulsation (\si{\\radian\per\second})},
ylabel={Phase (\si{degree})},
"""
endcenter="\end{center}\n"
endtikz="\end{tikzpicture}\n"
endaxis="\end{axis}\n"
enddoc="\end{document}\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"

# ==================================================================
#  Ecriture du \begin{tikzpicture} \end{tikzpicture} 
# ==================================================================
def write_tikZ():

    # ---------------------------
    # Infos relatives au système
    # ---------------------------
    intpuls,w,taus,deriv_integ,classe,m,n = calc_print_infos(G,taus,puls,verbose)
    # -------------------------
    # Générer les équations 
    # -------------------------
    eqn_tau, eqn_gain_reel, eqn_gain_reel_dB, eqn_phase_reelle = gen_eqn(G,taus,deriv_integ,classe,m,n)
    # -------------------------
    # Générer les tableaux
    # -------------------------
    tab_tau_w, tab_valeurs_particulieres = gen_tab(taus,puls,intpuls,w,deriv_integ,classe,gpw_particular)

    # -------------------------
    # Plot du gain de Bode
    # -------------------------
    plot_gain_real, plot_gain_asymptotic, plot_gain_particular = \
            gen_gain(G,taus,puls,intpuls,deriv_integ,classe,gpw_particular)  
    # -------------------------
    # Plot de la phase de Bode
    # -------------------------
    plot_phase_real, plot_phase_asymptotic, plot_phase_particular = \
            gen_phase(taus,puls,intpuls,deriv_integ,classe,gpw_particular)  

    # -----------------------------------------------------
    # regroupement des données pour les ecrires en boucle
    # -----------------------------------------------------
    plots_gain=(plot_gain_real,plot_gain_asymptotic,plot_gain_particular)
    plots_phase=(plot_phase_real,plot_phase_asymptotic,plot_phase_particular)
    plots=(plots_gain,plots_phase)
    
    # -------------------------
    # données relatives à pgfplots (LaTeX)
    # -------------------------
    axis = gen_axis(fontsizelabel="large",fontsizetickslabel="normalsize")
    xtick, xticklabels, xint = gen_xtick_and_labels(puls)
    ytick_gain,yint_gain   = gen_ytick_and_labels(gain)
    ytick_phase,yint_phase  = gen_ytick_and_labels(phas)
    
    # -------------------------
    # Fichier de sortie LaTeX
    # -------------------------
    fileoutTeX=fileout+'.tex'
    fileoutTikZ=fileout+'.tikz'
    fTeX=open(fileoutTeX,'w')
    if write_tikz_file : fTikZ=open(fileoutTikZ,'w')
    fTeX.write(article)
    fTeX.write(begindoc)
    fTeX.write(eqn_tau)

    fTeX.write(begincenter)
    # ===============================
    files=[fTeX]
    if write_tikz_file :
        files.append(fTikZ)
    for f in files :
        # -----------------
        #      gain 
        # -----------------
        f.write(begintikz)
        f.write(beginaxis)
        f.write(axis)
        f.write(label_gain)
        f.write(xtick)
        f.write(ytick_gain)
        f.write(xticklabels)
        f.write(ytick_gain)
        f.write(xint)
        f.write(yint_gain)
        f.write(axis_braket)
        for plot in plots[0] :
            for trace in plot :
                f.write(trace)
        f.write(endaxis)
        f.write(endtikz)
        f.write("\n")
        # -----------------
        #      phase 
        # -----------------
        f.write(begintikz)
        f.write(beginaxis)
        f.write(axis)
        f.write(label_phase)
        f.write(xtick)
        f.write(ytick_phase)
        f.write(xticklabels)
        f.write(ytick_phase)
        f.write(xint)
        f.write(yint_phase)
        f.write(axis_braket)
        for plot in plots[1] :
            for trace in plot :
                f.write(trace)
    
        f.write(endaxis)
        f.write(endtikz)
    # ===============================
    fTeX.write(endcenter)

    fTeX.write("\paragraph{Fonctions réelles du gain et du déphasage}\n")
    fTeX.write(eqn_gain_reel)
    fTeX.write(eqn_gain_reel_dB)
    fTeX.write(eqn_phase_reelle)

    fTeX.write("\paragraph{Quelques valeurs particulières (calculées) :}\n")
    fTeX.write(tab_valeurs_particulieres)

    fTeX.write("\paragraph{Commande pour reproduire ce fichier :}\n")
    fTeX.write("\\begin{verbatim}")
    #f.write("bodePGFtikz.py --taus "+str(taus)+" --axis estimation")
    fTeX.write(command_used)
    fTeX.write("\\end{verbatim}")

    fTeX.write(enddoc)
    fTeX.close()
    print("fichier "+fileout+" généré ")





# ==================================================================
# Ecriture du fichier LaTeX à partir d'une fonction de transfert
# définit par 
# ==================================================================
def write_tex_file(gain,phas,puls,G,taus,gpw_particular=[],command_used="",fileout="example",write_tikz_file=False,verbose=True):

    # ---------------------------
    # Infos relatives au système
    # ---------------------------
    intpuls,w,taus,deriv_integ,classe,m,n = calc_print_infos(G,taus,puls,verbose)
    # -------------------------
    # Générer les équations 
    # -------------------------
    eqn_tau, eqn_gain_reel, eqn_gain_reel_dB, eqn_phase_reelle = gen_eqn(G,taus,deriv_integ,classe,m,n)
    # -------------------------
    # Générer les tableaux
    # -------------------------
    tab_tau_w, tab_valeurs_particulieres = gen_tab(taus,puls,intpuls,w,deriv_integ,classe,gpw_particular)

    # -------------------------
    # Plot du gain de Bode
    # -------------------------
    plot_gain_real, plot_gain_asymptotic, plot_gain_particular = \
            gen_gain(G,taus,puls,intpuls,deriv_integ,classe,gpw_particular)  
    # -------------------------
    # Plot de la phase de Bode
    # -------------------------
    plot_phase_real, plot_phase_asymptotic, plot_phase_particular = \
            gen_phase(taus,puls,intpuls,deriv_integ,classe,gpw_particular)  

    # -----------------------------------------------------
    # regroupement des données pour les ecrires en boucle
    # -----------------------------------------------------
    plots_gain=(plot_gain_real,plot_gain_asymptotic,plot_gain_particular)
    plots_phase=(plot_phase_real,plot_phase_asymptotic,plot_phase_particular)
    plots=(plots_gain,plots_phase)
    
    # -------------------------
    # données relatives à pgfplots (LaTeX)
    # -------------------------
    axis = gen_axis(fontsizelabel="large",fontsizetickslabel="normalsize")
    xtick, xticklabels, xint = gen_xtick_and_labels(puls)
    ytick_gain,yint_gain   = gen_ytick_and_labels(gain)
    ytick_phase,yint_phase  = gen_ytick_and_labels(phas)
    
    # -------------------------
    # Fichier de sortie LaTeX
    # -------------------------
    fileoutTeX=fileout+'.tex'
    fileoutTikZ=fileout+'.tikz'
    fTeX=open(fileoutTeX,'w')
    if write_tikz_file : fTikZ=open(fileoutTikZ,'w')
    fTeX.write(article)
    fTeX.write(begindoc)
    fTeX.write(eqn_tau)

    fTeX.write(begincenter)
    # ===============================
    files=[fTeX]
    if write_tikz_file :
        files.append(fTikZ)
    for f in files :
        # -----------------
        #      gain 
        # -----------------
        f.write(begintikz)
        f.write(beginaxis)
        f.write(axis)
        f.write(label_gain)
        f.write(xtick)
        f.write(ytick_gain)
        f.write(xticklabels)
        f.write(ytick_gain)
        f.write(xint)
        f.write(yint_gain)
        f.write(axis_braket)
        for plot in plots[0] :
            for trace in plot :
                f.write(trace)
        f.write(endaxis)
        f.write(endtikz)
        f.write("\n")
        # -----------------
        #      phase 
        # -----------------
        f.write(begintikz)
        f.write(beginaxis)
        f.write(axis)
        f.write(label_phase)
        f.write(xtick)
        f.write(ytick_phase)
        f.write(xticklabels)
        f.write(ytick_phase)
        f.write(xint)
        f.write(yint_phase)
        f.write(axis_braket)
        for plot in plots[1] :
            for trace in plot :
                f.write(trace)
    
        f.write(endaxis)
        f.write(endtikz)
    # ===============================
    fTeX.write(endcenter)

    fTeX.write("\paragraph{Fonctions réelles du gain et du déphasage}\n")
    fTeX.write(eqn_gain_reel)
    fTeX.write(eqn_gain_reel_dB)
    fTeX.write(eqn_phase_reelle)

    fTeX.write("\paragraph{Quelques valeurs particulières (calculées) :}\n")
    fTeX.write(tab_valeurs_particulieres)

    fTeX.write("\paragraph{Commande pour reproduire ce fichier :}\n")
    fTeX.write("\\begin{verbatim}")
    #f.write("bodePGFtikz.py --taus "+str(taus)+" --axis estimation")
    fTeX.write(command_used)
    fTeX.write("\\end{verbatim}")

    fTeX.write(enddoc)
    fTeX.close()
    print("fichier "+fileout+" généré ")


