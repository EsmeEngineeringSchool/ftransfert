import numpy as np
import matplotlib.pyplot as plt
from ftransfert.common.contour import add_arrow
from ftransfert.common.utils import rad2deg,nat2dB,bo2bf 
from ftransfert.common.utils import nf

fmt_gain = '%r dB'
fmt_phase = '%r °'
def nyquist(FT,complet=False,mcircles=False,ncircles=False,**kwargs):
   """
   Plot Nyquist chart for p= -∞ j -> +∞ j
   in practice from :
       -fmax -> fmax if complet
           0 -> fmax if not complet
   """
   dpi=kwargs.get('dpi',100)        # résolution de l'image
   savefig=kwargs.get('savefig',None)
   xlim=kwargs.get('xlim', (-5,5))
   ylim=kwargs.get('ylim', (-5,5))
   fmax=kwargs.get('fmax', 1e3)
   n=kwargs.get('n',4086)
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
   if FT.title!=None:
       FT.title=r'Nyquist $'+FT.name+r'(p)$'
 
   if FT.verbeux > 0 :
       print(60*'*')
       if complet :
           print("Complete Nyquist plot : "+FT.name+'(p)')
           print("Interval des pulsations logarithmiques")
           w=-1j*np.logspace(np.log10(fmax),-np.log10(fmax),n)
           w+=1j*np.logspace(-np.log10(fmax),np.log10(fmax),n)
       else:
           print("Nyquist plot : "+FT.name+'(p)')
           print("Interval des pulsations logarithmiques")
           w=1j*np.logspace(-np.log10(fmax),np.log10(fmax),n)
       print("Nombre de points",n,len(w))
       if middle : 
           print("Arrows in middle")
       else:
           print("Arrows",arrow_pcts)
       print(FT)
       if ncircles and mcircles :
           print(f"Erreur Nyquist plot: N-cercles et les M-cercles\nne peuvent pas être tracés en même temps")
           return
       elif mcircles :
           print("M-cercles")
       elif ncircles :
           print("N-cercles")
       print(60*'*'+'\n')
  
   XNyq=[]
   YNyq=[]
   for kg,gain in enumerate(gains):
       # evaluer F(p) pour p=-infty j -> +infty j
       response=FT.harm_response(w,gain)
       XNyq.append(response[0]) # partie réelle
       YNyq.append(response[1]) # partie imaginaire
   
   # matplotlib instructions
   fig = plt.figure(figsize=(6,5),dpi=dpi)
   ax = fig.add_subplot(1, 1, 1)
   ax.set(xlim=xlim, ylim=ylim)
   ax.tick_params(axis='both',labelsize=16)
   #ax.title.set_text(r'Nyquist $'+FT.name+'(p)$')
   ax.title.set_text(FT.title)
   ax.title.set_size(24)
   ax.xaxis.label.set_text(r'$\mathrm{Re}['+FT.name+'(j\omega)]$')
   ax.xaxis.label.set_size(22)
   ax.yaxis.label.set_text(r'$\mathrm{Im}['+FT.name+'(j\omega)]$')
   ax.yaxis.label.set_size(22)
   # Si on ne trace pas d'abaques on trace une grille
   if not mcircles and not ncircles : 
       plt.grid()
   else:
       # calcul de certaines quantités utiles pour le tracer des abaques
       N=512
       def circle(x,y):
           return 90*4*((x+0.5)**2+y**2)
       re_bo=np.linspace(-4,4,N)
       im_bo=np.linspace(-4,4,N)
       gain_bf=np.zeros((N,N))
       phase_bf=np.zeros((N,N))
       [Re,Im]=np.meshgrid(re_bo,im_bo)
       deg90=circle(Re,Im)
       for i in range(N):
           for j in range(N):
               bf=bo2bf(complex(re_bo[i],im_bo[j]))
               gain_bf[j][i]=nat2dB(np.abs(bf))
               phase_bf[j][i]=rad2deg(np.arcsin(bf.imag/np.abs(bf)))
   # Tracé des M-cercles 
   if mcircles:
       isogain=[-11,-9,-7,-6]
       isogain=ax.contour(re_bo,im_bo, gain_bf, levels=isogain, colors="tab:blue", linewidths=0.8, linestyles="solid")
       isogain.levels = [nf(val) for val in isogain.levels]
       ax.clabel(isogain,isogain.levels,inline=True, inline_spacing=5,fontsize=8,fmt=fmt_gain,colors='tab:blue')
   # Tracé des N-cercles 
   if ncircles :
       isophases=[-56.3,-45,-26.5,0]
       isophase=ax.contour(re_bo, im_bo, phase_bf,isophases,colors="tab:blue",linewidths=0.8,linestyles="solid")
       #iso90=ax.contour(re_bo, im_bo, deg90,[90],colors="tab:blue",linewidths=0.8,linestyles="solid")
       isophase.levels = [nf(val) for val in isophase.levels]
       isophase_loc=[(-0.2,-0.75),(0.1,-0.75),(0.6,-0.75),(0.8,0)]
       #iso90_loc=[(0,-0.5)]
       ax.clabel(isophase, isophase.levels,inline=True,inline_spacing=5,fontsize=8,fmt=fmt_phase,colors='tab:blue',manual=isophase_loc)
       #ax.clabel(isophase, isophase.levels,inline=True,inline_spacing=5,fontsize=8,fmt=fmt_phase,colors='tab:blue')
       #ax.clabel(iso90, iso90.levels,inline=True,inline_spacing=5,fontsize=8,fmt=fmt_phase,colors='tab:blue',manual=iso90_loc)
   for kg in range(len(gains)):
       line,=plt.plot(XNyq[kg],YNyq[kg],color=color,label=labels[kg],linewidth=2)
       add_arrow(line,pcts=arrow_pcts,middle=middle)
   """    
   # si l'on souhaite ajouter des points particulier (pour certaine pulsation)
   # attention la pulsation doit être complexe (i.e jw)
   XNyq=[]
   YNyq=[]
   w=np.array([0.0,1.0,2,3])*1j
   FT.tabLaTeX(ws=w)
   for kg,gain in enumerate(gains):
       # evaluer F(p) pour p=-infty j -> +infty j
       response=FT.harm_response(w,gain)
       XNyq.append(response[0]) # partie réelle
       YNyq.append(response[1]) # partie imaginaire
   for kg in range(len(gains)):
       plt.scatter(XNyq[kg],YNyq[kg],color='tab:red',label=labels[kg],linewidth=2,marker="x",s=120)
   """
   if labels[0]: ax.legend()
   plt.tight_layout()
   if savefig:
       plt.savefig(savefig,dpi=dpi)
   else:
       plt.show()
   plt.close(fig)
