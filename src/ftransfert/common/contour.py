import matplotlib.pyplot as plt
import numpy as np
DPI=100

def add_arrow(line, size=16, color=None,middle=False,pcts=[0.01]):
    """
        add an arrow to a line. (adapted from https://stackoverflow.com/questions/
                                 34017866/arrow-on-a-line-plot-with-matplotlib)
        line:       Line2D object
        size:       size of the arrow in fontsize points
        color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    m=(len(xdata) - 1)//2
    if middle :
        line.axes.annotate('',
        xytext=(xdata[m], ydata[m]),
        xy=(xdata[m+1], ydata[m+1]),
        arrowprops=dict(arrowstyle="->", color=color,linewidth=2),
        size=size)
    else:    
        for pct in pcts:
            q1=int(len(xdata)*pct)
            q2=len(xdata)-q1
            line.axes.annotate('',
            xytext=(xdata[q1], ydata[q1]),
            xy=(xdata[q1+1], ydata[q1+1]),
            arrowprops=dict(arrowstyle="->", color=color,linewidth=2),
            size=size)
            line.axes.annotate('',
            xytext=(xdata[q2], ydata[q2]),
            xy=(xdata[q2+1], ydata[q2+1]),
            arrowprops=dict(arrowstyle="->", color=color,linewidth=2),
            size=size)

def plot_contour(C,**kwargs):
    """
        plot contour class with matplotlib
    """
    xlim=kwargs.get('xlim', (-5,5))
    ylim=kwargs.get('ylim', (-5,5))
    fig = plt.figure(figsize=(6,5),dpi=DPI)
    ax = fig.add_subplot(1, 1, 1)
    ax.set(xlim=xlim, ylim=ylim)
    ax.title.set_text(r'contour $\mathcal{C}$')
    ax.title.set_size(24)
    ax.xaxis.label.set_text(r'$\mathrm{Re}[p]$')
    ax.xaxis.label.set_size(20)
    ax.yaxis.label.set_text(r'$\mathrm{Im}[p]$')
    ax.yaxis.label.set_size(20)
    plt.grid()

    for path in C:
        line,=plt.plot([x[0] for x in path],[x[1] for x in path])
        add_arrow(line,middle=True)
    plt.show()

def rectangle(a=(0,0),b=(1,1),npts=128,inverse=False):
    """
        inverse=False     inverse=True
            x ->- b          x -<- b
            |     |          |     |
            ʌ     v          v     ʌ 
            |     |          |     |
            a -<- x          a ->- x
    """
    C=[]
    if inverse :
        C.append([(x,a[1]) for x in np.linspace(a[0],b[0],npts)])
        C.append([(b[0],y) for y in np.linspace(a[1],b[1],npts)])
        C.append([(x,b[1]) for x in np.linspace(b[0],a[0],npts)])
        C.append([(a[0],y) for y in np.linspace(b[1],a[1],npts)])
    else:
        C.append([(a[0],y) for y in np.linspace(a[1],b[1],npts)])
        C.append([(x,b[1]) for x in np.linspace(a[0],b[0],npts)])
        C.append([(b[0],y) for y in np.linspace(b[1],a[1],npts)])
        C.append([(x,a[1]) for x in np.linspace(b[0],a[0],npts)])
    return C

# cercle 
def circle(radius=1.0,center=(0,0),npts=512,segments=4,inverse=False):
    """      
         - < -            - > -  
       /       \        /       \
      |         |      |         |
      v    o    ʌ      ʌ    o    v
      |         |      |         |
       \       /        \       /
         - > -            - < - 
    """
    def xy(inverse,center,radius,npts,i):
        if inverse :
            return (center[0]+radius*np.cos(2*np.pi*i/npts),center[1]+radius*np.sin(2*np.pi*i/npts))
        else :
            return (center[0]+radius*np.cos(2*np.pi*i/npts),center[1]-radius*np.sin(2*np.pi*i/npts))
    C=[]
    n=npts//segments
    for k in range(segments):
        C.append([xy(inverse,center,radius,npts,i) for i in range(k*n,(k+1)*n)])
    return C

if __name__ == "__main__":
    C=rectangle((-1.5,-1),(-0.25,1))
    plot_contour(C,xlim=(-2,1),ylim=(-2,2))
    C=rectangle((-1.5,-1),(-0.25,1),inverse=True)
    plot_contour(C,xlim=(-2,1),ylim=(-2,2))
    C=circle(center=(0,0),radius=0.75)
    plot_contour(C,xlim=(-2,2),ylim=(-1.5,1.5))
    C=circle(center=(0,0),radius=0.75,inverse=True)
    plot_contour(C,xlim=(-2,2),ylim=(-1.5,1.5))
    C=circle(center=(0,0),radius=0.75,inverse=True,segments=16)
    plot_contour(C,xlim=(-2,2),ylim=(-1.5,1.5))
