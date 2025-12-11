# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines):
    return "".join(lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines):
    return "\n".join(lines)
def beginmathdisplay():
    return "\["
def endmathdisplay():
    return "\]"
# -----------------------------------------------------------------
# retourne \macro{value}
# -----------------------------------------------------------------
def macro(name,value="",options=""):
    out=['\\'f"{name}"]
    if len(options) :
        out+=["["f"{options}""]"]
    if len(value) :
        out+=["{"f"{value}""}"]
    return concatenate(out)
# -----------------------------------------------------------------
# retourne \begin{env}[options]
# -----------------------------------------------------------------
def begin(env,options=""):
    out=["\\begin{"f"{env}""}"]
    if len(options):
        out+=["["f"{options}""]"]
    return concatenate(out)
# -----------------------------------------------------------------
# retourne \end{env}
# -----------------------------------------------------------------
def end(env):
    return "\\end{"f"{env}""}"
# ------------------------------------------------------------------------------
def tabLaTeX(self,**kwargs):
   # Recast levels to new class
   class nf(float):
       def __repr__(self):
           return f'{self:.2f}'
   ws=kwargs.get('ws',None)
   winput=isinstance(ws,np.ndarray)
   wlim=kwargs.get('wlim', (1e-2,1e2))
   n=kwargs.get('n',11)
   # array of pulsations
   if not winput :
       ws=1j*np.logspace(np.log10(wlim[0]),np.log10(wlim[1]),n)
   response=self.harm_response(ws,self.gain)
   print("\\begin{center}")
   print("\\begin{tabular}{ccc}")
   print("\\hline")
   print("$\omega$ (\si{\\radian\per\second}) & Gain (\si{\decibel}) & Phase (\si{\degree})\\\\")
   print("\\hline")
   for w,m,p in zip(ws,response[2],response[3]):
       print(str(nf(abs(w)))+" & "+str(nf(nat2dB(m)))+" & "+str(nf(rad2deg(p)))+"\\\\")
   print("\\hline")
   print("\end{tabular}")
   print("\\end{center}")
