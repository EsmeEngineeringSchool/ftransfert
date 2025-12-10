def strc(root):
    # retourne si possible la chaine de la
    # valeure absolue du int de la partie
    # réelle et imaginaire d'un complexe
    r=str(int(abs(c.real)))
    if abs(c.imag) == 1.0 :
        return r,''
    else :
        return r,str(int(abs(c.imag)))
def strroot(roots):
    #retourne une chaine de caractères
    # de toute les racines (poles et zeros)
    out=''
    for root in roots:
        r,i=strc(root)
        if root.real<0:
            out+='(p+'+r
        else:
            out+='(p-'+r
        if root.imag<0 :
            out+='+'+i+'j'
        elif root.imag>0:
            out+='-'+i+'j'
        out+=')'
    return out


print(strc(1+1j))
print(strroot([complex(5,2)]))
