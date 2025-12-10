import numpy as np
import matplotlib.pyplot as plt
from ftransfert.common.utils import rad2deg,nat2dB,bo2bf 
from ftransfert.common.contour import add_arrow
# ------------------------------------------------------------------------------
def black_nichols(FT,plot=True,nichols=False,**kwargs):
   """
   Plot Black (Nichols) chart for p= 0 -> +∞ j
   in practice from 0 -> fmax
   """
   dpi=kwargs.get('dpi',100)        # résolution de l'image
   savefig=kwargs.get('savefig',None)
   xlim=kwargs.get('xlim', (-270,0))
   ylim=kwargs.get('ylim', (-40,40))
   fmax=kwargs.get('fmax', 1e3)
   n=kwargs.get('n',4096)
   labels=kwargs.get('labels',[None])
   color=kwargs.get('color','tab:blue')
   arrow_pcts=kwargs.get('arrow_pcts',[])
   if len(arrow_pcts)>0 : 
       middle=False
   else:
       middle=True
       arrow_pcts=[0.5]
   gains=kwargs.get('gains',[])
   gains.insert(0,FT.gain)
   if isinstance(labels,str):
       labels=[labels]
   if len(gains) > 2 :
       color=None
   print(60*'*')
   print("Black plot : "+FT.name+'(p)')
   print("Interval des pulsations logarithmiques")
   w=1j*np.logspace(-np.log10(fmax),np.log10(fmax),n)
   print("Nombre de points",n,len(w))
   print(FT)
   print(60*'*'+'\n')
   XBlack=[]
   YBlack=[]
   for kg,gain in enumerate(gains):
       # evaluer F(p) pour p= 0 -> +infty j
       response=FT.harm_response(w,gain)
       XBlack.append(rad2deg(response[3]))
       YBlack.append(nat2dB(response[2]))
   if not plot : return XBlack,YBlack
 
   # Black-Nichols
   if nichols :
       isomodules=[x for x in np.arange(xlim[0],-3)]
       isomodules+=[x for x in np.arange(-3.5,-1.5,0.5)]
       isomodules+=[x for x in np.arange(-1.8,-0.8,0.2)]
       isomodules+=[x for x in np.arange(-0.9,1.1,0.1)]
       isomodules+=[x for x in np.arange(1.5,3.5,0.5)]
       isomodules+=[4,5,6,8,10,12]
       isophases=[x for x in np.arange(-210,-40,10)]
       isophases+=[x for x in np.arange(-45,-15,5)]
       isophases+=[x for x in np.arange(-18,-8,2)]
       isophases+=[x for x in np.arange(-9,-2,1)]
       isophases+=[x for x in np.arange(-2.5,0,0.5)]
       isophases+=[x for x in np.arange(-0.4,0,0.1)]
       isophases+=[x for x in np.arange(0,0.5,0.1)]
       isophases+=[x for x in np.arange(0.5,3,0.5)]
       isophases+=[x for x in np.arange(3,11,1)]
       isophases+=[x for x in np.arange(12,22,2)]
       isophases+=[x for x in np.arange(25,55,5)]
       isophases+=[x for x in np.arange(60,240,10)]

       N=256
       phi=np.linspace(xlim[0],xlim[1],N)
       GdB=np.linspace(ylim[0],ylim[1],N)
       GdBbf=np.zeros((N,N))
       phibf=np.zeros((N,N))
       for i in range(N):
           for j in range(N):
               g=dB2nat(GdB[i])
               p=deg2rad(phi[j])
               h=g*np.exp(1j*p)
               z=bo2bf(complex(h.real,h.imag))
               GdBbf[i][j]=nat2dB(np.abs(z))
               phibf[i][j]=rad2deg(np.arctan2(z.imag,z.real))

   # matplotlib instructions
   fig = plt.figure(figsize=(8,6),dpi=dpi)
   ax = fig.add_subplot(1, 1, 1)
   ax.set(xlim=xlim, ylim=ylim)
   ax.tick_params(axis='both',labelsize=16)
   ax.title.set_text(r'Black $'+FT.name+'(p)$')
   ax.title.set_size(24)
   ax.xaxis.label.set_text(r'$\phi(\omega) (\degree)$')
   ax.xaxis.label.set_size(22)
   ax.yaxis.label.set_text(r'$G_{dB}(\omega)$')
   ax.yaxis.label.set_size(22)
   # Tracé de l'abaque de Black-Nichols
   if nichols:
       isom=ax.contour(phi, GdB,GdBbf,levels=isomodules,linewidths=0.3,colors="tab:gray",linestyles="solid")
       isop=ax.contour(phi, GdB,phibf,levels=isophases,linewidths=0.3,colors="tab:gray",linestyles="solid")
       # Recast levels to new class
       class nf(float):
           def __repr__(FT):
               s = f'{FT:.1f}'
               return f'{FT:.0f}' if s[-1] == '0' else s
       isom.levels = [nf(val) for val in isom.levels]
       isop.levels = [nf(val) for val in isop.levels]
       isop_loc_all=[(-260,10),(-260,11),(-260,12),(-260,13),(-260,15),(-260,16),(-260,17),(-260,18),(-260,19),
               (-260,21),(-260,23),(-260,25),(-260,27),(-260,30),(-260,32),
               (-100,10),(-100,11),(-100,12),(-100,13),(-100,15),(-100,16),(-100,17),(-100,18),(-100,19),
               (-100,21),(-100,23),(-100,25),(-100,27),(-100,28),(-100,32),
               (-20,-32),(-30,-32),(-40,-32),(-50,-32),
               (-60,-32),(-70,-32),(-80,-32),(-90,-32),
               (-100,-32),(-110,-32),(-120,-32),(-130,-32),
               (-140,-32),(-150,-32),(-160,-32),(-170,-32),
               (-190,-32),(-200,-32),(-210,-32),(-220,-32),
               (-230,-32),(-240,-32),(-250,-32),(-260,-32),
               (-270,-32),(-280,-32),(-290,-32),(-300,-32),
               (-310,-32),(-320,-32),(-330,-32),(-340,-32)]
       isom_loc_all = [(-5,-21),(-5,-19),(-5,-17),
                   (-5,-15),(-5,-12),(-5,-10),
                   (-5,-7),(-5,-5),(-5,-3),(-5,-1),
                   (-5,0),(-5,2),(-5,4),(-5,6),
                   (-5,8),(-5,10),(-5,12),(-5,13),(-5,15),(-5,18),
                   (-175,3),(-175,4),(-175,6),(-175,7),(-175,8),(-175,10),
                   (-175,12),(-175,14),(-175,16),(-175,19),(-175,21),(-175,23),(-175,27)]
       isop_loc=[]
       for p in isop_loc_all:
           if (p[0]>xlim[0] and p[0]<xlim[1]) and (p[1]>ylim[0] and p[1]<ylim[1]):
                  isop_loc.append(p)
       isom_loc=[]
       for m in isom_loc_all:
           if (m[0]>xlim[0] and m[0]<xlim[1]) and (m[1]>ylim[0] and m[1]<ylim[1]):
                  isom_loc.append(m)
       ax.clabel(isop, isop.levels,inline=True,inline_spacing=-3, fontsize=8,fmt=fmt_phase,manual=isop_loc)
       ax.clabel(isom, isom.levels,inline=True,inline_spacing=-3, fontsize=8,fmt=fmt_gain,manual=isom_loc)
   else:
       plt.grid()
   for kg in range(len(gains)):
       line,=plt.plot(XBlack[kg],YBlack[kg],color=color,label=labels[kg])
       add_arrow(line,pcts=arrow_pcts,middle=middle)
   XBlack=[]
   YBlack=[]   
   w=np.array([0.0,1.0,2,3])*1j
   #FT.tabLaTeX(ws=w)  
   for kg,gain in enumerate(gains):     
       # evaluer F(p) pour p=-infty j -> +infty j 
       response=FT.harm_response(w,gain)   
       XBlack.append(rad2deg(response[3]))
       YBlack.append(nat2dB(response[2]))
   for kg in range(len(gains)):
       plt.scatter(XBlack[kg],YBlack[kg],color='tab:red',label=labels[kg],linewidth=2,marker="x",s=120)
   if labels[0]: ax.legend()
   if savefig:
       plt.savefig(savefig)
   else:
       plt.show()
   return fig,line
