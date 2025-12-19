import sys
import numpy as np
import math
from ftransfert.common.latex import beginmathdisplay,endmathdisplay,macro,begin,end,draw,tick,ticklabels
from ftransfert.common.string_ import newlines

# ---------------------------------------------------------------
# options des axes du pgfplot/tikz
# ---------------------------------------------------------------
def options_axis(xint,yint,xtick=True,xlabel="",ylabel="",ystep=20):
    xmin,xmax=xint
    ymin,ymax=yint
    out=["ticklabel style = {font=\\normalsize},"]
    out+=["width=0.9\\textwidth,"]
    out+=["height=0.25\\textheight,"]
    out+=["grid=both,"]
    out+=["major grid style={black!40},"]
    out+=["label style={font=\large},"]
    out+=["xmode=log,ymode=normal,"]
    out+=["xlabel={"f"{xlabel}""},"]
    out+=["ylabel={"f"{ylabel}""},"]
    if xtick :
        out+=[f"xtick={tick(xmin,xmax,sequence='geometric')},"]
    out+=[f"ytick={tick(ymin,ymax,sequence='arithmetic',raison=ystep)},"]
    out+=[f"xticklabels={ticklabels(xmin,xmax)},"]
    out+=[f"yticklabels={ticklabels(ymin,ymax,sequence='not_geometric',raison=ystep)},"]
    out+=[f"xmin={xmin},xmax={xmax},"]
    out+=[f"ymin={ymin},ymax={ymax}"]
    return newlines(out)

# générations des relations de gain et de phases asymptotiques
def asymptotics_relations(FT):
    gain_relations,phase_relations=[],[]
    i,d=FT.classe
    allinterval=f"{20*np.log10(FT.gain)}"
    if i : allinterval+=f"-{20*i}*log10(x)"
    if d : allinterval+=f"+{20*d}*log10(x)"
    gain_relations.append(allinterval)
    phase_relations.append((d-i)*90)
    for k,w in enumerate(FT.w_i):
        gain_relations.append(gain_relations[-1]+f"+({20*w[1]})*log10(x/{w[0]})")
        phase_relations.append(phase_relations[-1]+w[1]*90)
    return gain_relations,phase_relations
    
# figure bode gain 
def gaintikz(FT,w_intervals,gain_axis,gain_relations,gain_exact):
    xmin,xmax=w_intervals[0][0],w_intervals[-1][-1]
    ymin,ymax,gain_step=gain_axis

    out=[begin("tikzpicture",options="trim axis left")]
    out+=[begin("axis",options=options_axis((xmin,xmax),\
                                            (ymin,ymax),\
                                             xtick=False,
                                             ylabel="Gain (\si{\decibel})",
                                             ystep=gain_step))]
    out+=[macro("addplot",options=f"ultra thick, blue,domain={xmin}:{xmax},samples=256",value=gain_exact,semicolon=True)]
    for gain_relation,(w1,w2) in zip(gain_relations,w_intervals):
        out+=[macro("addplot",options=f"line width=2pt,red,dashed,domain={w1}:{w2}, samples=16",value=gain_relation,semicolon=True)]
    out+=[end("axis")]
    out+=[end("tikzpicture")]
    return newlines(out) 

# figure bode phase 
def phasetikz(FT,w_intervals,phase_axis,phase_relations,phase_exact):
    xmin,xmax=w_intervals[0][0],w_intervals[-1][-1]
    ymin,ymax,phase_step=phase_axis

    out=[begin("tikzpicture",options="trim axis left")]
    out+=[begin("axis",options=options_axis((xmin,xmax),\
                                            (ymin,ymax),\
                                             xlabel="Pulsation (\si{\\radian\per\second})",\
                                             ylabel="Phase (\si{degree})",\
                                             ystep=phase_step))]
    out+=[macro("addplot",\
                options=f"ultra thick, blue,domain={xmin}:{xmax},samples=256",\
                value=phase_exact,\
                semicolon=True)]
    for k,(phase_relation,(w1,w2)) in enumerate(zip(phase_relations,w_intervals)):
        out+=[macro("addplot",\
                    options=f"line width=2pt,red,dashed,domain={w1}:{w2},samples=16",\
                    value=str(phase_relation),\
                    semicolon=True)]
        if k <= len(phase_relations)-2 :
            out+=[draw(options="line width=2pt,red,dashed",\
                       pt1=f"axis cs:{w_intervals[k][1]},{phase_relations[k]}",\
                       pt2=f"axis cs:{w_intervals[k+1][0]},{phase_relations[k+1]}")]
    out+=[end("axis")]
    out+=[end("tikzpicture")]
    return newlines(out) 


def bode(FT,filename,latex_document=True,**kwargs):
    gain_relations,phase_relations=asymptotics_relations(FT)
    xlim=kwargs.get('xlim',(1e-2,1e2))
    y1lim=kwargs.get('y1lim',(-40,40))
    y2lim=kwargs.get('y2lim',(-90,90))
    gain_axis=(*y1lim,math.ceil((y1lim[1]-y1lim[0])//10))
    phase_axis=(*y2lim,(y2lim[1]-y2lim[0])//10)
    omegas=[]
    omegas.append(xlim[0])
    omegas+=[w for w,m in FT.w_i]
    omegas.append(xlim[1])
    w_intervals=[]
    for k in range(len(omegas)-1):
        w_intervals.append((omegas[k],omegas[k+1]))

    # ------------------------------------------
    # LaTeX Header
    # ------------------------------------------
    out=[]
    if latex_document :
        out+=[macro("documentclass","article")]
        out+=[macro("usepackage","geometry")]
        out+=[macro("geometry","paperwidth=21cm,\npaperheight=29.7cm,\nmargin=1cm")]
        out+=[macro("usepackage","amsmath")]
        out+=[macro("usepackage","mathfmv")]
        out+=[macro("usepackage","siunitx")]
        out+=[macro("usepackage","pgf")]
        out+=[macro("usepackage","tikz")]
        out+=[macro("usepackage","pgfplots")]
        out+=[macro("pgfplotsset","compat=1.18")]
        out+=[begin("document")]
    # Affichage de la fonction de transfert H(p)
    out+=[beginmathdisplay()]
    out+=[FT.latex("p")]
    out+=[endmathdisplay()]
    out+=[begin("center")]
    # Diagramme de Bode (Gain |H(jw)|dB)
    gain_exact=FT.addplot("moduledB")
    out+=[gaintikz(FT,w_intervals,gain_axis,gain_relations,gain_exact)]
    out+=[""]
    # Diagramme de Bode (Phase deg)
    phase_exact=FT.addplot("argument")
    out+=[phasetikz(FT,w_intervals,phase_axis,phase_relations,phase_exact)]
    out+=[end("center")]
    # Affichage des fonctions réelles 
    out+=[macro("paragraph","Fonctions réelles du gain et du déphasage")]
    out+=[beginmathdisplay()]
    out+=[FT.latex("module")]
    out+=[endmathdisplay()]
    out+=[beginmathdisplay()]
    out+=[FT.latex("moduledB")]
    out+=[endmathdisplay()]
    out+=[beginmathdisplay()]
    out+=[FT.latex("argument")]
    out+=[endmathdisplay()]
    # Tableau des valeurs particulières 
    out+=[macro("paragraph","Quelques valeurs particulières calculées")]
    out+=[FT.tablatex(wlim=xlim)]
    if latex_document :
        out+=[end("document")]
    if filename :
        with open(filename,"w") as f:
            print(newlines(out),file=f)
    else:
        return newlines(out)

