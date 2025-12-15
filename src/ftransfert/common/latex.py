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
def macro(name,value="",options="",semicolon=False):
    out=['\\'f"{name}"]
    if len(options) :
        out+=["["f"{options}""]"]
    if len(value) :
        out+=["{"f"{value}""}"]
    if semicolon : out[-1]+=";"
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
