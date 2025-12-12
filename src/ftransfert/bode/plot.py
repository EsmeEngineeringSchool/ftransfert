import matplotlib.pyplot as plt
import numpy as np
from ftransfert.common.utils import nat2dB,rad2deg
from ftransfert.common.contour import add_arrow

def bode(FT,**kwargs):
   """
   Plot Bode charts for p= 0 -> +∞ j
   in practice from 0 -> fmax
   """
   dpi=kwargs.get('dpi',100)        # résolution de l'image
   savefig=kwargs.get('savefig',None)
   xlim=kwargs.get('xlim', (1e-2,1e2))
   y1lim=kwargs.get('y1lim', (-30,10))
   y2lim=kwargs.get('y2lim', (-90,0))
   fmax=kwargs.get('fmax', 1e3)
   n=kwargs.get('n',4096)
   labels=kwargs.get('labels',[None])
   color=kwargs.get('color','tab:blue')
   gains=kwargs.get('gains',[])
   gains.insert(0,FT.gain)
   arrow_pcts=kwargs.get('arrow_pcts',[])
   if len(arrow_pcts)>0 : 
       middle=False
   else:
       middle=True
       arrow_pcts=[0.5]
   if isinstance(labels,str):
       labels=[labels]
   if len(gains) > 2 :
       color=None
   # array of pulsations
   w=1j*np.logspace(-np.log10(fmax),np.log10(fmax),n)
   
   if FT.verbeux > 0 :
       print(60*'*')
       print("Bode plot : "+FT.name+'(p)')
       print("Interval des pulsations logarithmiques",fmax)
       print("Nombre de points",n,len(w))
       print(FT)
       print(60*'*'+'\n')
   
   XBode=[]  # Omega
   Y1Bode=[] # GdB(Omega)
   Y2Bode=[] # Phi(Omega)
   for kg,gain in enumerate(gains):
       _,_,module,arg=FT.harmonic_response(w,gain)
       XBode.append(w)
       Y1Bode.append(nat2dB(module))
       Y2Bode.append(rad2deg(arg))
   
   # matlplotlib instructions
   fig = plt.figure(figsize=(6,8),dpi=dpi)
   # Gain chart (UP)
   ax1 = fig.add_subplot(2, 1, 1)
   ax1.tick_params(axis='both',labelsize=16)
   ax1.title.set_text(r'Bode $'+FT.name+'(p)$')
   ax1.title.set_size(24)
   ax1.set(xlim=xlim, ylim=y1lim)
   ax1.xaxis.label.set_text(r'$\omega$ (rad$\cdot$s$^{-1}$)')
   ax1.xaxis.label.set_size(22)
   ax1.yaxis.label.set_text(r'$G_{dB}(\omega)$')
   ax1.yaxis.label.set_size(22)
   ax1.set_xscale('log')
   plt.grid()
   for kg in range(len(gains)):
       line,=plt.plot(XBode[kg].imag,Y1Bode[kg],color=color,label=labels[kg])
       add_arrow(line,pcts=arrow_pcts,middle=middle)
   # Phase chart (DOWN)
   ax2 = fig.add_subplot(2, 1, 2)
   ax2.set(xlim=xlim, ylim=y2lim)
   ax2.tick_params(axis='both',labelsize=16)
   ax2.xaxis.label.set_text(r'$\omega$ (rad$\cdot$s$^{-1}$)')
   ax2.xaxis.label.set_size(22)
   ax2.yaxis.label.set_text(r'$\phi(\omega) (\degree)$')
   ax2.yaxis.label.set_size(22)
   ax2.set_xscale('log')
   plt.grid()
   for kg in range(len(gains)):
       line,=plt.plot(XBode[kg].imag,Y2Bode[kg],color=color,label=labels[kg])
       add_arrow(line,pcts=arrow_pcts,middle=middle)
   plt.tight_layout()
   if savefig:
       plt.savefig(savefig)
   else:
       plt.show()
   return fig 
