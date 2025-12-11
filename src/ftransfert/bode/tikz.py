from common.latex import beginmathdisplay,endmathdisplay,macro,begin,end
from common.string_ import newlines

def bode(FT):
    # latex header
    out=[macro("documentclass","article","tikz")]
    out+=[macro("usepackage","amsmath")]
    out+=[macro("usepackage","circuitikz")]
    out+=[begin("document")]
    out+=[beginmathdisplay()]
    out+=[FT.latex("p")]
    out+=[endmathdisplay()]
    out+=[macro("paragraph","Fonctions réelles du gain et du déphasage")]
    out+=[FT.latex("module")]
    out+=[FT.latex("moduledB")]
    out+=[FT.latex("argument")]
    out+=[macro("paragraph","Quelques valeurs particulières calculées")]
    out+=[end("document")]
    return newlines(out)

#import sys
#import numpy as np
#import random as rd
#import math as m 
#
#def round_sig(x, sig=2):
#    return round(x, sig-int(m.floor(m.log10(abs(x))))-1)
#
## ========================================================== 
## header du fichier tex avec le chargement des paquets 
## ========================================================== 
#article="""\
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%  Fichier généré par bodePGFtikz.py !
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#\\documentclass{article}
#\\usepackage[francais]{babel}
#\\usepackage[utf8]{inputenc}
#\\usepackage[T1]{fontenc}
#\\usepackage{lmodern}
#\\usepackage{amsmath}
#\\usepackage{amsthm}
#\\usepackage{amssymb}
#\\usepackage{pgf,tikz}
#\\usepackage{pgfplots}
#\\usepackage{siunitx}
#\\usepackage{geometry}
#\\usepackage{mymath}
#\\geometry{
#paperwidth=21cm,
#paperheight=29.7cm,
#margin=1cm
#}
#\\usepackage{tabularx}
#\\newcolumntype{K}[1]{>{\centering\\arraybackslash}p{#1}}
#\\newcolumntype{M}[1]{>{\centering\\arraybackslash}m{#1}}
#\\newcolumntype{N}{@{}m{0pt}@{}}
#"""
#
## quelques variables relatives à LaTeX
#begindoc="""\\begin{document}
#\\thispagestyle{empty}
#"""
#begincenter="\\begin{center}\n"
#begintikz="\\begin{tikzpicture}[trim axis left]\n"
#beginaxis="\\begin{axis}"
#axis_braket="]\n"
#label_gain="ylabel={Gain (\si{\decibel})},\n"
#label_phase="""xlabel={Pulsation (\si{\\radian\per\second})},
#ylabel={Phase (\si{degree})},
#"""
#endcenter="\end{center}\n"
#endtikz="\end{tikzpicture}\n"
#endaxis="\end{axis}\n"
#enddoc="\end{document}\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
#
## ========================================================== 
## Radian -> Degree
## ========================================================== 
#def degrees(rad):
#    return (180.0*rad)/np.pi
#
## ========================================================== 
## Calcul numérique des gains et phases de la 
## fonction de transfert définie par le tuple taus
## en sortie valeur minimale et maximale du gain et 
## de la phase permettant d'estimer l'intervalle 
## des axes X et Y
## ========================================================== 
#def numerical_H(puls,G,taus,omegas,deriv_integ,classe):
#
#    gain_min= 100000.0
#    gain_max=-100000.0
#
#    phas_min= 1000000.0
#    phas_max=-1000000.0
#    wmin=puls[0]
#    wmax=puls[1]
#
#    for w in np.arange(wmin,wmax,0.25):
#        gain=20*np.log10(G)
#        if deriv_integ :
#            phas=classe*90
#        else:
#            phas=0.0
#        w10=10**w
#        for tau in taus:
#            if tau[1] != 0 :
#                gain+=10*tau[1]*np.log10(1+tau[0]*tau[0]*w10*w10)
#                phas+=degrees(tau[1]*np.arctan2(tau[0]*w10,1))
#            else:
#                gain+=20*tau[0]*np.log10(w10)
#        #print(w,gain,phase)
#        if gain  < gain_min : gain_min = gain
#        if gain  > gain_max : gain_max = gain
#        if phas  < phas_min : phas_min = phas
#        if phas  > phas_max : phas_max = phas
#
#    gain_int=gain_max-gain_min
#    phas_int=phas_max-phas_min
#    gain_min-=gain_int*0.15
#    gain_max+=gain_int*0.15
#    phas_min-=phas_int*0.15
#    phas_max+=phas_int*0.15
#
#    gpw_particular=[]
#    for w in omegas :
#        gain=20*np.log10(G)
#        if deriv_integ :
#            phas=classe*90
#        else:
#            phas=0.0
#        w10=float(10**w)
#        for tau in taus:
#            if tau[1] != 0 :
#                gain+=10*tau[1]*np.log10(1+tau[0]*tau[0]*w10*w10)
#                phas+=degrees(tau[1]*np.arctan2(tau[0]*w10,1))
#            else:
#                gain+=20*tau[0]*np.log10(w10)
#        gpw_particular.append((gain,phas,w))
#
##    for gpw in gpw_particular:
##        print(gpw)
#
#    return np.floor(gain_min),np.ceil(gain_max),np.floor(phas_min),np.ceil(phas_max),gpw_particular
#
## ========================================================== 
## Quelques informations relatives au système 
## en fonction des valeurs de la liste taus 
## ========================================================== 
#def calc_print_infos(gain_statique,taus,puls,verbose=True):
#
#    # tri décroissant des temps tau_i pour obtenir les pulsations dans l'ordre
#    taus.sort(reverse=True)
#    # ------------------------------------------
#    # intervalle des pulsations
#    # intpuls=[(start,w1),(w1,w2),...,(wn,end)]
#    # ------------------------------------------
#    new_taus=[]
#    w=[]
#    w.append(puls[0])
#    deriv_integ=False # Le système possède-t-il un intégrateur/dérivateur
#    classe=None
#    num_ordre=0
#    den_ordre=0
#    for tau in taus:
#        if tau[1] != 0 and tau[1] > 0 : num_ordre+=abs(tau[1])
#        if tau[1] != 0 and tau[1] < 0 : den_ordre+=abs(tau[1])
#        if tau[1] != 0 :
#            #w.append(int(np.log10(1/tau[0])))
#            w.append(np.log10(1/tau[0]))
#            new_taus.append(tau)
#        else:
#            deriv_integ=True
#            classe=tau[0]
#            tau_deriv=tau
#
#    if not classe:
#        classe=0
#    elif classe < 0 :
#        den_ordre+=classe
#    elif classe > 0 :
#        num_ordre+=classe
#
#    w.append(puls[1])
#    w.sort()
#    intpuls=[]
#    for k,ww in enumerate(w[:-1]):
#        intpuls.append((ww,w[k+1]))
#
#    new_taus.sort(reverse=True)
#    if deriv_integ : new_taus.append(tau_deriv) # réarangement de la liste tau
#
#    omegas=w.copy()
#    if len(omegas) > 2 :
#        omegas.pop(0)
#        omegas.pop()
#    if omegas[-1] < puls[1] : 
#        omegas.append(omegas[-1]+1)
#    if omegas[0] > puls[0] :
#        omegas.insert(0,omegas[0]-1)
#
#    # ---------------------------
#    # Print infos !
#    # ---------------------------
#    if verbose :
#        print(52*'-')
#        print(8*" "+"Infos")
#        print(52*'-')
#        print("Système       :")
#        print("Gain statique                  : ",gain_statique)
#        if classe != 0 :
#            print("classe  (derivateur)           = ",classe) if classe > 0 else \
#            print("classe  (intégrateur)          = ",classe)
#        else:
#            print("classe                         = ",classe) 
#        print("ordre global  (n)              = ",den_ordre)
#        print("zeros         (m)              = ",num_ordre)
#        if num_ordre != den_ordre :
#            print("m > n (non causal)") if num_ordre > den_ordre else print("m < n (causal)")
#        else:
#            print("m = n (non causal)") 
#        print()
#        print("Sous-systèmes                  : ")
#        print("tau/ordre                      : ",new_taus)
#        print("intervalles pulsations         : ",intpuls)
#        print("valeurs particulières (calcul) : ",omegas)
#        print()
#    
#    return intpuls,omegas,new_taus,deriv_integ,classe,num_ordre,den_ordre
#
#
## ========================================================== 
##   propriétés des axes de pgfplots
## ========================================================== 
#def gen_axis(width=0.9,height=0.25,fontsizelabel="normalsize", \
#            fontsizetickslabel="small",color="black!40"):
#    axis="""
#[ticklabel style = {font=\\"""+fontsizetickslabel+"""},
#width="""+str(width)+"""\\textwidth,
#height="""+str(height)+"""\\textheight,
#grid=both,
#major grid style={"""+color+"""},
#label style={font=\\"""+fontsizelabel+"""},
#xmode=log,ymode=normal,"""
#    return axis
#
#
## ========================================================== 
##   intervale, ticks et labels pour l'axe X
## ========================================================== 
#def gen_xtick_and_labels(puls):
#    xtick=""
#    xtick+="xtick={"
#    for i in range(puls[0],puls[1]+1):
#        xtick+="1e"+str(i)+','
#    xtick=xtick[:-1]
#    xtick+="},\n"
#    xticklabels=""
#    xticklabels+="xticklabels={"
#    for i in range(puls[0],puls[1]+1):
#        xticklabels+="$10^{"+str(i)+'}$,'
#    xticklabels=xticklabels[:-1]
#    xticklabels+="},\n"
#    xint="xmin=1e"+str(puls[0])+",xmax=1e"+str(puls[1])+",\n"
#    return xtick,xticklabels,xint
#
## ========================================================== 
##   intervale, ticks et labels pour l'axe Y 
## ========================================================== 
#def gen_ytick_and_labels(data):
#    #print(data)
#    delta=(data[1]-data[0])/data[2]
#    ytick=""
#    ytick+="ytick={"
#    for i in range(data[2]+1):
#        y=data[0]+delta*i
#        ytick+=str(y)+','
#    ytick=ytick[:-1]
#    ytick+="},\n"
#    yint="ymin="+str(data[0])+",ymax="+str(data[1])+"\n"
#    return ytick,yint
#
#
## ========================================================== 
##    gain reel et asymptotique pour les taus données
## ========================================================== 
#def gen_gain(G,taus,puls,intpuls,deriv_integ,classe,gpw_particular):
#    
#    # -------------------------------
#    #      Bode réel (gain)
#    # -------------------------------
#    string="\\addplot[ultra thick, blue,domain=1e"+str(puls[0])+":1e"+str(puls[1])+", samples=201] {"
#    string+=str(int(20*np.log10(G)))
#    for tau in taus:
#        if tau[1] != 0 :
#            kk=(10*tau[1])
#            tausq=tau[0]**2
#            if tau[1] > 0 :
#                string+="+"+str(int(kk))+"*log10(1+"+str(tausq)+"*x*x)"
#            else:
#                string+=str(int(kk))+"*log10(1+"+str(tausq)+"*x*x)"
#        else:
#            kk=20*tau[0]
#            string+="+"+str(int(kk))+"*log10(x)"
#    string+='};\n'
#    plot_gain_real=[string]
#    # -------------------------------
#    #      Bode asymptotique (gain)
#    # -------------------------------
#
#    string=""
#    # gain statique en dB
#    pente_gain = 0.0
#    if deriv_integ :
#        pente_gain+=20*classe
#
#    gain_start=20*np.log10(G)
#    gain_next=gain_start
#    for k,tau in enumerate(taus):
#        if tau[1] != 0 :
#            string+="\\addplot[line width=2pt,red,dashed,"+\
#            "domain="+str(10**(intpuls[k][0]))+":"+str(10**(intpuls[k][1]))+",samples=51] {"+ \
#            str(gain_next)+'+'+str(pente_gain)+"*log10(x)};\n"
#            gain_next+=intpuls[k][1]*pente_gain
#            pente_gain+=tau[1]*20
#            gain_next-=intpuls[k][1]*pente_gain
#            #"domain=1e"+str(intpuls[k][0])+":1e"+str(intpuls[k][1])+",samples=51] {"+ \
##            "domain="+str(10**(intpuls[k][0]))+":"+str(10**(intpuls[k][1]))+",samples=51] {"+ \
#
#    string+="\\addplot[line width=2pt,red,dashed,"+\
#             "domain="+str(10**(intpuls[-1][0]))+":"+str(10**(intpuls[-1][1]))+",samples=51] {"+ \
#             str(gain_next)+'+'+str(pente_gain)+"*log10(x)};\n"
#    plot_gain_asymptotic=[string]
##             "domain="+str(10**(intpuls[-1][0]))+":"+str(10**(intpuls[-1][1]))+",samples=51] {"+ \
#
#    # ------------------------------------
#    # Bode pour qqs valeurs particulières (gain)
#    # ------------------------------------
#    string=""
#    for gpw in gpw_particular:
#        w=10**gpw[2]
#        string+="\draw[draw=none,fill=blue] (axis cs:"+str(w)+","+str(gpw[0])+") circle (2pt);\n"
#
#    plot_gain_particular=[string]
#
#
#    return plot_gain_real, plot_gain_asymptotic, plot_gain_particular
#
## ========================================================== 
##    phase reelle et asymptotique pour les taus données
## ========================================================== 
#def gen_phase(taus,puls,intpuls,deriv_integ,classe,gpw_particular):
#
#    # -------------------------------
#    #      Bode réel (phase)
#    # -------------------------------
#    string="\\addplot[ultra thick, blue,domain=1e"+str(puls[0])+":1e"+str(puls[1])+", samples=201] {"
#    for tau in taus:
#        if tau[1] != 0 :
#            if tau[1] > 0 :
#                string+="+"+str(tau[1])+"*atan2("+str(tau[0])+"*x,1)"
#            else:
#                string+=str(tau[1])+"*atan2("+str(tau[0])+"*x,1)"
#        else:
#            string+=str(tau[0]*90) if tau[0] < 0 else '+'+str(tau[0]*90)
#    string+='};\n'
#    plot_phase_real=[string]
#    # -------------------------------
#    #      Bode asymptotique (phase)
#    # -------------------------------
#    string=""
#    # --------------------------------------------
#    # phase global (integrateur/dérivateur ou non)
#    # --------------------------------------------
#    phase=0.0
#    if deriv_integ :
#        phase+=classe*90
#    phase_old=phase
#
#    for k,tau in enumerate(taus):
#        if tau[1] != 0 :
#            phase_old=phase
#            phase+=tau[1]*90.0
#            string+="\\addplot[line width=2pt,red,dashed,domain="+ \
#                str(10**(intpuls[k][0]))+":"+str(10**(intpuls[k][1]))+",samples=51] {"+str(phase_old)+"};\n"
#            string+="\\draw[line width=2pt,red,dashed] (axis cs:"+str(10**(intpuls[k][1]))+","+str(phase_old)+\
#                                                ")  -- (axis cs:"+str(10**(intpuls[k][1]))+","+str(phase)+");\n"
#    string+="\\addplot[line width=2pt,red,dashed,domain="+ \
#             str(10**(intpuls[-1][0]))+":"+str(10**(intpuls[-1][1]))+",samples=51] {"+str(phase)+"};\n"
#
#    plot_phase_asymptotic=[string]
#
#    # ------------------------------------
#    # Bode pour qqs valeurs particulières (gain)
#    # ------------------------------------
#    string=""
#    for gpw in gpw_particular:
#        w=10**gpw[2]
#        string+="\draw[draw=none,fill=blue] (axis cs:"+str(w)+","+str(gpw[1])+") circle (2pt);\n"
#
#    plot_phase_particular=[string]
#
#    return plot_phase_real, plot_phase_asymptotic, plot_phase_particular
#
## ========================================================== 
##  Générer les tableaux LaTeX des données
## ========================================================== 
#def gen_tab(taus,puls,intpuls,w,deriv_integ,classe,gpw_particular):
#   
#    hline="\\hline\n"
#    tab_tau_w=""
#    tab_valeurs_particulieres="""
#\\begin{center}
#\\resizebox{0.6\\textwidth}{!}{%
#"""
#
#    tabu_line="\\begin{tabular}{|M{3.0cm}"
#    puls_line="Pulsation (\si{\\radian\per\second})"
#    gain_line="Gain (\si{\decibel})"
#    phas_line="Déphasage (\si{\degree})"
#
#    for gpw in gpw_particular:
#        tabu_line+="|M{1.5cm}"
#        if int(gpw[2]) == gpw[2] :
#            puls_line+="&$10^{"+str(int(gpw[2]))+"}$"
#        else:
#            puls_line+="&"+str(round_sig(10**(gpw[2]),1))
#
#        gain_line+="&"+str(int(round(gpw[0])))
#        phas_line+="&"+str(int(round(gpw[1])))
#
#    tabu_line+="|N}\n"
#    puls_line+="& \\\[1em] \n"
#    gain_line+="& \\\[1em] \n"
#    phas_line+="& \\\[1em] \n"
#
#    tab_valeurs_particulieres+=tabu_line+hline
#    tab_valeurs_particulieres+=puls_line+hline
#    tab_valeurs_particulieres+=gain_line+hline
#    tab_valeurs_particulieres+=phas_line
#
#    #Pulsation (\si{\\radian\per\second}) & $10^{-3}$ & $\omega_1=10^{-2}$ & $\omega_2=10^{-1}$ & $\omega_3=1$ & 10 & \\\\[1em]
#    #\hline
#    #Gain (\si{\decibel})            &    20 &    17 &     3 &    -3 &   -20 & \\\\[1em]
#    #\hline
#    #Déphasage (\si{\degree})   &    -5 &   -40 &   -45 &   -50 &   -85 & \\\\[1em]
#
#    tab_valeurs_particulieres+="""
#    \hline
#\end{tabular}%
#}
#\end{center}
#"""
#
#    return tab_tau_w, tab_valeurs_particulieres
#
#
## ========================================================== 
## Ecrire l'équation sous format LaTeX 
## de la fonction de transfert en fonction des
## données en entrée
## ========================================================== 
#def gen_eqn(G,taus,deriv_integ,classe,m,n) :
#
#    # --------------
#    #     H(p) 
#    # --------------
#    eqn_tau  = "$$\\boldsymbol{"
#    if n != 0 :
#        eqn_tau += "H(p)=\\dfrac"
#        num="{"
#        den="{"
#        if G!=1:
#            num="{"+str(G)
#    else:
#        eqn_tau += "H(p)="
#        num=""
#        den=""
#
#    if deriv_integ :
#        if classe < 0 :
#            if classe == -1 :
#                den+="p"
#            else:
#                den+="p^{"+str(abs(classe))+"}"
#        else:
#            if classe == 1 :
#                num+="p"
#            else:
#                num+="p^{"+str(abs(classe))+"}"
#
#    for tau in taus:
#        if tau[1] != 0:
#            if tau[1] == -1:
#                if tau[0] != 1 :
#                    den +="("+str(tau[0])+"p+1)"
#                else :
#                    den +="(p+1)" if len(taus)>1 else "p+1"
#            elif tau[1] < 0 :
#                if tau[0] != 1 :
#                    den +="("+str(tau[0])+"p+1)^{"+str(abs(tau[1]))+"}"
#                else :
#                    den +="(p+1)^{"+str(abs(tau[1]))+"}"
#            elif tau[1] == 1:
#                if tau[0] != 1 :
#                    num +="("+str(tau[0])+"p+1)"
#                else :
#                    num +="(p+1)" if len(taus)>1 else "p+1"
#            elif tau[1] > 0 :
#                if tau[0] != 1 :
#                    num +="("+str(tau[0])+"p+1)^{"+str(abs(tau[1]))+"}"
#                else :
#                    num +="(p+1)^{"+str(abs(tau[1]))+"}"
#
#    if num == "{" :
#        num="{"+str(G)
#    if den == "{" :
#        den=""
#    
#    if n != 0 :
#        num += "}"
#        den += "}"
#    eqn_tau +=num+den
#    eqn_tau += "}$$\n"
#
#    # --------------
#    #     G(w)  
#    # --------------
#    eqn_gain_reel="$$G(\omega)=|H(\jw)|="
#    eqn_gain_reel+="\dfrac"
#
#    if G != 1 :
#        num="{"+str(G)
#    else:
#        num="{"
#    den="{"
#
#    if deriv_integ : 
#        if classe < 0 :
#            if classe == -1 :
#                den+="\omega"
#            else:
#                den+="\omega^{"+str(abs(classe))+"}"
#        else:
#            if classe == 1 :
#                num+="\omega"
#            else:
#                num+="\omega^{"+str(abs(classe))+"}"
#
#    for k,tau in enumerate(taus):
#        if tau[1] !=0 :
#            if tau[1] == -1:
#                den +="\sqrt{1+\\tau_"+str(k+1)+"^2\omega^2}"
#            elif tau[1] == -2 :
#                den +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)"
#            elif tau[1] < -2 :
#                if abs(tau[1])%2 == 0: 
#                    den +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)^{"+str(int(abs(tau[1])/2))+"}"
#                else:
#                    den +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)^{\\frac{"+str(abs(tau[1]))+"}{2}}"
#            elif tau[1] == 1:
#                num +="\sqrt{1+\\tau_"+str(k+1)+"^2\omega^2}"
#            elif tau[1] == 2:
#                num +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)"
#            elif tau[1] >  2 :
#                if tau[1]%2 == 0: 
#                    num +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)^{"+str(int(tau[1]/2))+"}"
#                else:
#                    num +="\\left(1+\\tau_"+str(k+1)+"^2\omega^2\\right)^{\\frac{"+str(abs(tau[1]))+"}{2}}"
#
#    num+=""
#    den+=""
#    num+="}"
#    den+="}"
#    if num == "{}" : num="{1}"
#    eqn_gain_reel+=num+den
#
#    eqn_gain_reel+="$$\n"
#    
#    # --------------
#    #    G_dB(w)
#    # --------------
#    eqn_gain_reel_dB="$$G_{dB}(\omega)="
#    logG=20*np.log10(G)
#    if G != 1 :
#        eqn_gain_reel_dB+=str(int(logG))
#    if deriv_integ : 
#        kk=classe*20
#        if classe > 0 and G != 1:
#            eqn_gain_reel_dB+="+"+str(int(kk))+"\log\omega"
#        else:
#            eqn_gain_reel_dB+=str(int(kk))+"\log\omega"
#
#    for k,tau in enumerate(taus):
#        if tau[1] != 0 :
#            kk=tau[1]*10
#            if kk > 0 :
#                eqn_gain_reel_dB+="+"+str(int(kk))+"\log{(1+\\tau_"+str(k+1)+"^2\omega^2)}"
#            else:
#                eqn_gain_reel_dB+=str(int(kk))+"\log{(1+\\tau_"+str(k+1)+"^2\omega^2)}"
#    eqn_gain_reel_dB+="$$\n"
#
#    # --------------
#    #    phi(w)
#    # --------------
#    eqn_phase_reel="$$\phi(\omega)=\\arg{H(\jw)}="
#    if deriv_integ :
#        eqn_phase_reel+=str(int(classe*90))
#
#    for k,tau in enumerate(taus) :
#        if tau[1] != 0 :
#            if abs(tau[1]) != 1 :
#                if tau[1] > 0 :
#                    eqn_phase_reel+="+"+str(int(tau[1]))+"\\arctan{\\tau_"+str(k+1)+"\omega}"
#                else:
#                    eqn_phase_reel+=str(int(tau[1]))+"\\arctan{\\tau_"+str(k+1)+"\omega}"
#            else:
#                if tau[1] > 0 :
#                    eqn_phase_reel+="+\\arctan{\\tau_"+str(k+1)+"\omega}"
#                else:
#                    eqn_phase_reel+="-\\arctan{\\tau_"+str(k+1)+"\omega}"
#
#    eqn_phase_reel+="$$\n"
#    
#    return eqn_tau,eqn_gain_reel,eqn_gain_reel_dB,eqn_phase_reel
#
## ==================================================================
## Ecriture du fichier LaTeX à partir d'une fonction de transfert
## définit par 
## ==================================================================
#def write_tex_file(gain,phas,puls,G,taus,gpw_particular=[],command_used="",fileout="example",write_tikz_file=False,verbose=True):
#
#    # ---------------------------
#    # Infos relatives au système
#    # ---------------------------
#    intpuls,w,taus,deriv_integ,classe,m,n = calc_print_infos(G,taus,puls,verbose)
#    # -------------------------
#    # Générer les équations 
#    # -------------------------
#    eqn_tau, eqn_gain_reel, eqn_gain_reel_dB, eqn_phase_reelle = gen_eqn(G,taus,deriv_integ,classe,m,n)
#    # -------------------------
#    # Générer les tableaux
#    # -------------------------
#    tab_tau_w, tab_valeurs_particulieres = gen_tab(taus,puls,intpuls,w,deriv_integ,classe,gpw_particular)
#
#    # -------------------------
#    # Plot du gain de Bode
#    # -------------------------
#    plot_gain_real, plot_gain_asymptotic, plot_gain_particular = \
#            gen_gain(G,taus,puls,intpuls,deriv_integ,classe,gpw_particular)  
#    # -------------------------
#    # Plot de la phase de Bode
#    # -------------------------
#    plot_phase_real, plot_phase_asymptotic, plot_phase_particular = \
#            gen_phase(taus,puls,intpuls,deriv_integ,classe,gpw_particular)  
#
#    # -----------------------------------------------------
#    # regroupement des données pour les ecrires en boucle
#    # -----------------------------------------------------
#    plots_gain=(plot_gain_real,plot_gain_asymptotic,plot_gain_particular)
#    plots_phase=(plot_phase_real,plot_phase_asymptotic,plot_phase_particular)
#    plots=(plots_gain,plots_phase)
#    
#    # -------------------------
#    # données relatives à pgfplots (LaTeX)
#    # -------------------------
#    axis                     = gen_axis(fontsizelabel="large",fontsizetickslabel="normalsize")
#    xtick, xticklabels, xint = gen_xtick_and_labels(puls)
#    ytick_gain,yint_gain     = gen_ytick_and_labels(gain)
#    ytick_phase,yint_phase   = gen_ytick_and_labels(phas)
#    
#    # -------------------------
#    # Fichier de sortie LaTeX
#    # -------------------------
#    fileoutTeX=fileout+'.tex'
#    fileoutTikZ=fileout+'.tikz'
#    fTeX=open(fileoutTeX,'w')
#    if write_tikz_file : fTikZ=open(fileoutTikZ,'w')
#    fTeX.write(article)
#    fTeX.write(begindoc)
#    fTeX.write(eqn_tau)
#
#    fTeX.write(begincenter)
#    # ===============================
#    files=[fTeX]
#    if write_tikz_file :
#        files.append(fTikZ)
#    for f in files :
#        # -----------------
#        #      gain 
#        # -----------------
#        f.write(begintikz)
#        f.write(beginaxis)
#        f.write(axis)
#        f.write(label_gain)
#        f.write(xtick)
#        f.write(ytick_gain)
#        f.write(xticklabels)
#        f.write(ytick_gain)
#        f.write(xint)
#        f.write(yint_gain)
#        f.write(axis_braket)
#        for plot in plots[0] :
#            for trace in plot :
#                f.write(trace)
#        f.write(endaxis)
#        f.write(endtikz)
#        f.write("\n")
#        # -----------------
#        #      phase 
#        # -----------------
#        f.write(begintikz)
#        f.write(beginaxis)
#        f.write(axis)
#        f.write(label_phase)
#        f.write(xtick)
#        f.write(ytick_phase)
#        f.write(xticklabels)
#        f.write(ytick_phase)
#        f.write(xint)
#        f.write(yint_phase)
#        f.write(axis_braket)
#        for plot in plots[1] :
#            for trace in plot :
#                f.write(trace)
#    
#        f.write(endaxis)
#        f.write(endtikz)
#    # ===============================
#    fTeX.write(endcenter)
#
#    fTeX.write("\paragraph{Fonctions réelles du gain et du déphasage}\n")
#    fTeX.write(eqn_gain_reel)
#    fTeX.write(eqn_gain_reel_dB)
#    fTeX.write(eqn_phase_reelle)
#
#    fTeX.write("\paragraph{Quelques valeurs particulières (calculées) :}\n")
#    fTeX.write(tab_valeurs_particulieres)
#
#    fTeX.write("\paragraph{Commande pour reproduire ce fichier :}\n")
#    fTeX.write("\\begin{verbatim}")
#    #f.write("bodePGFtikz.py --taus "+str(taus)+" --axis estimation")
#    fTeX.write(command_used)
#    fTeX.write("\\end{verbatim}")
#
#    fTeX.write(enddoc)
#    fTeX.close()
#    print("fichier "+fileout+" généré ")
#
#
#if __name__=="__main__":
#
#    print( \
#"""====================================================
# bodePGFtikz.py :
# script pour générer des diagrammes de Bode 
# avec pgfplots/TikZ/LaTeX
#====================================================
# auteur : fmv
# date   : juillet 2019
# lieu   : ESME Sudria Lille
#====================================================""")
#
#    # ====================================================
#    # Définition de la fonction de transfert
#    # ====================================================
#    # taus : (temps,ordre) 
#    # ordre < 0 au dénominateur (=> n)
#    # ordre > 0 au numérateur   (=> m)
#    # si ordre ==0 
#    #       temps < 0  intégrateur
#    #       temps > 0  dérivateur
#    # todo : second ordre complexe conjugué.
#    # ====================================================
#    # exemple : 
#    # G=10 
#    #
#    # taus=[(t1,2), (t2,-1), (t3,-1), (t4,-1) , (a,0) ]
#    #        
#    #                  10   (t1*p+1)^2
#    # H(p)= p^a  ---------------------------
#    #              (t2*p+1) (t3*p+1) (t4*p+1)
#    #
#    # a positif ou négatif
#    # ====================================================
#
#    simple_test = False 
#
#    if simple_test : 
#    # 1 test 
#        tests=[((-80,60,7),(-180,0,6),(-4,5),100,[(1,2),(100,-1),(10,-1),(0.01,-1)],"test1.tex")]
#
#    # 3 tests
##        tests=[((-80,60,7),(-180,0,6),(-4,5),100,[(1,2),(100,-1),(10,-1),(0.01,-1)],"test1.tex"),
##               ((20,90,7),(-90,90,6),(-4,5),1,[(10,1),(0.1,1),(0.001,-2),(-1,0)],"test2.tex"), 
##               ((-90,-20,7),(-90,90,6),(-4,5),1,[(10,-1),(0.1,-1),(0.001,2),(1,0)],"test3.tex")] 
#        k=0
#        for test in tests :
#            k+=1
#            gain_axis=test[0]
#            phas_axis=test[1]
#            puls_axis=test[2]
#            gain_static=test[3]
#            taus=test[4]
#            test_filename=test[5]
#
#            # main function !
#            write_tex_file(gain_axis,phas_axis,puls_axis,gain_static,taus,gpw_particular,fileout=test_filename)
#
#    random_tests = True 
#    if random_tests :
#        puls_axis=(-8,8)
#
#        k=0
#        while k<100:
#
#            # contrainte : 1 seul dérivateur/intégrateur par système (of course)
#            deriv=False
#            # contrainte de "causalité" sur les ordres m et n
#            m=1
#            n=0
#            while m > n or n == 0 :
#                gain_static=10**(rd.randint(0,3))
#                taus=[]
#                rd1=rd.randint(puls_axis[0]+1,0)
#                rd2=rd.randint(1,puls_axis[1]-1)
#                rd3=rd.randint(1,4)
#                tau_all=[10**(x) for x in range(rd1,rd2,rd3)]
#                rd.shuffle(tau_all)
#                while len(tau_all)>=1 : #for kk in range(rd.randint(1,9)):
#                    tau=tau_all.pop()
#                    ordre=rd.randint(-3,4)
#                    while ordre == 0 and deriv :
#                        ordre=rd.randint(-4,4)
#                    if ordre == 0 and not deriv :
#                        tau=rd.randint(-4,4)
#                        while tau == 0:
#                            tau=rd.randint(-4,4)
#                        deriv=True
#                    taus.append((tau,ordre))
#                intpuls,omegas,taus,deriv_integ,classe,m,n = calc_print_infos(gain_static,taus,puls_axis,verbose=True) 
#
#            test_filename="test_v3_"+str(k)+".tex"
#            gain_min,gain_max,phase_min,phase_max,gpw_particular = numerical_H(puls_axis,gain_static,taus,omegas,deriv_integ,classe)
#            gain_axis=(gain_min,gain_max,8)
#            phas_axis=(phase_min,phase_max,8)
#            write_tex_file(gain_axis,phas_axis,puls_axis,gain_static,taus,gpw_particular,fileout=test_filename,verbose=False)
#            k+=1
#
#    if False: 
#        # get range numeracaly
#        test=((0,20,8),(0,90,6),(-7,7),1,[(1,-1),(10,1)],"example.tex")
#        gain_axis=test[0]
#        phas_axis=test[1]
#        puls_axis=test[2]
#        gain_static=test[3]
#        taus=test[4]
#        test_filename=test[5]
#    
#        write_tex_file(gain_axis,phas_axis,puls_axis,gain_static,taus,fileout=test_filename)
#    
#        print(numerical_H(puls_axis,gain_static,taus,deriv_integ,classe))
#
