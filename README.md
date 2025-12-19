# Ftransfert - Bibliothèque d'Analyse des Fonctions de Transfert

Une bibliothèque Python pour l'analyse et la visualisation des fonctions de transfert 
en automatique et traitement du signal. Cette bibliothèque fournit des outils 
complets pour travailler avec les fonctions de transfert dans les domaines 
temporel et fréquentiel, avec support des diagrammes de Bode, tracés de contours et génération de documentation LaTeX.

## Fonctionnalités

### Fonctionnalités principales

- **Représentation des Fonctions de Transfert** : 
    - Zéros et pôles (représentation racines)
    - Coefficients polynomiaux (numérateur/dénominateur)
    - Fonctions lambda pour des définitions personnalisées

- **Analyse de la Réponse Fréquentielle** :
  - Calcul de la réponse harmonique
  - Calcul du module et de la phase
  - Détection automatique des intégrateurs et dérivateurs
  - Identification des pulsations de rupture

- **Outils de Visualisation** :
  - Diagrammes de Bode (gain et phase)
  - Tracés basés sur Matplotlib avec style personnalisable
  - Flèches directionnelles sur les contours
  - Support de la comparaison de plusieurs gains

### Représentations mathématiques

- **Sortie LaTeX** : Générer des équations prêtes pour publication :
  - Fonction de transfert H(p)
  - Gain en dB : G_dB(ω)
  - Module : |H(jω)|
  - Phase : φ(ω)

- **Support PGF/TikZ** : Créer des tracés de haute qualité pour documents LaTeX avec :
  - Approximations asymptotiques (lignes rouges en pointillés)
  - Courbes de réponse exactes (lignes bleues continues)
  - Mise à l'échelle et étiquetage automatiques des axes
  - Dimensions de tracé personnalisables

### Intégration de contours

- **Contours géométriques** :
  - Contours rectangulaires (sens horaire/anti-horaire)
  - Contours circulaires avec segments ajustables
  - Points d'échantillonnage personnalisables
  - Flèches directionnelles pour visualisation du chemin

## Installation

```bash
# Cloner le dépôt
git clone <url-du-dépôt>
cd ftransfert

# Installer les dépendances
pip install numpy matplotlib sympy
```

## Démarrage rapide

### Définir une fonction de transfert

```python
from ftransfert import Ftransfert

# Utilisation de zéros et pôles
zeros = [(0, 0), (-2, 1)]  # paires (réel, imaginaire)
poles = [(0, 0), (-5, 0), (-3, -4)]
H = Ftransfert(zeros=zeros, poles=poles, gain=10, name="H")

# Utilisation de coefficients polynomiaux
num = [1, 2, 1]  # p² + 2p + 1
den = [1, 5, 6]  # p² + 5p + 6
H = Ftransfert(num=num, den=den, gain=1, name="H")
```

### Générer un diagramme de Bode

```python
from ftransfert.plot import bode

# Créer un diagramme de Bode
bode(H, xlim=(1e-2, 1e2), y1lim=(-40, 20), y2lim=(-180, 0))
```

### Exporter vers LaTeX/TikZ

```python
from ftransfert.tikz import bode as bode_tikz

# Générer un document LaTeX avec diagrammes de Bode
bode_tikz(H, filename="sortie.tex", 
          xlim=(1e-2, 1e2), 
          y1lim=(-40, 40), 
          y2lim=(-90, 90))
```

### Créer des tracés de contours

```python
from ftransfert.contour import rectangle, circle, plot_contour

# Contour rectangulaire
C = rectangle(a=(-1.5, -1), b=(0.25, 1), npts=128)
plot_contour(C, xlim=(-2, 1), ylim=(-2, 2))

# Contour circulaire
C = circle(center=(0, 0), radius=0.75, segments=8)
plot_contour(C, xlim=(-2, 2), ylim=(-2, 2))
```

## Classes et méthodes principales

### Classe `Ftransfert`

**Paramètres d'initialisation** :
- `zeros` : Liste de zéros sous forme de tuples (réel, imaginaire)
- `poles` : Liste de pôles sous forme de tuples (réel, imaginaire)
- `num` : Coefficients du polynôme numérateur
- `den` : Coefficients du polynôme dénominateur
- `gain` : Gain du système (défaut : 1)
- `name` : Nom de la fonction (défaut : "F")

**Méthodes principales** :
- `eval(p, gain)` : Évaluer H(p) au point complexe p
- `harmonic_response(w, gain)` : Calculer la réponse fréquentielle
- `latex(key)` : Générer la représentation LaTeX
- `info()` : Afficher les informations de la fonction de transfert
- `tablatex(**kwargs)` : Générer un tableau LaTeX de valeurs

### Fonctions utilitaires

**Conversions d'unités** (`utils.py`) :
- `rad2deg(rad)` : Radians vers degrés
- `deg2rad(deg)` : Degrés vers radians
- `nat2dB(g)` : Gain naturel vers décibels
- `dB2nat(dB)` : Décibels vers gain naturel

**Formatage de chaînes** (`string_.py`) :
- `strroot(roots, latex)` : Formater les racines en chaîne
- `strpoly(poly, latex)` : Formater le polynôme en chaîne

## Fonctionnalités avancées

### Analyse asymptotique

La bibliothèque calcule automatiquement :
- Les pulsations de rupture (ω_i)
- Les approximations asymptotiques du gain et de la phase
- La multiplicité des pôles et zéros
- Le gain statique

### Dépliage de phase

Support du dépliage de phase type MATLAB avec suivi de la surface de Riemann pour une représentation continue de la phase sur plusieurs périodes de 2π.

### Tracés personnalisés

Options de personnalisation étendues :
- Paramètres DPI
- Limites d'axes personnalisées
- Placement des flèches sur les courbes
- Schémas de couleurs
- Superposition de plusieurs fonctions de transfert

## Structure des fichiers

```
ftransfert/
├── common/
│   ├── Ftransfert.py    # Classe principale de fonction de transfert
│   ├── plot.py          # Fonctions de tracé Matplotlib
│   ├── tikz.py          # Génération LaTeX/TikZ
│   ├── contour.py       # Outils d'intégration de contours
│   ├── utils.py         # Fonctions utilitaires
│   ├── string_.py       # Formatage de chaînes
│   └── latex.py         # Assistants LaTeX
```

## Prérequis

- Python 3.10+
- NumPy
- Matplotlib
- SymPy

## Exemples d'utilisation

### Afficher les informations d'une fonction de transfert

```python
H = Ftransfert(zeros=[(-2, 0)], poles=[(-5, 0), (-3, -4)], gain=10)
H.info()
```

Sortie :
```
----------------------------------------------------
        Ftransfert Infos
----------------------------------------------------
Système       (type:roots)
Gain                          : 10
Gain (static)                 : 0.667
nombre d'intégrateurs (i)     = 0
nombre de dérivateurs (d)     = 0
poles         (n)             = 2 [(-5+0j), (-3-4j)]
zeros         (m)             = 1 [(-2+0j)]
m <= n (causal)

Sous-systèmes                 : 
pulsations, multiplicité      : (2.00, 1), (5.00, -1), (5.00, -1)
```

### Générer une table LaTeX de valeurs

```python
print(H.tablatex(wlim=(0.1, 100), n=5))
```

### Représentation mathématique

```python
# Afficher la fonction de transfert
print(H)

# Obtenir la représentation LaTeX
print(H.latex("p"))
print(H.latex("moduledB"))
print(H.latex("argument"))
```

## Cas d'usage typiques

### Étude d'un système du premier ordre

```python
# Système : H(p) = K / (1 + τp)
tau = 0.1  # constante de temps
K = 5      # gain statique
poles = [(-1/tau, 0)]
H = Ftransfert(zeros=[], poles=poles, gain=K, name="H")

# Tracer le diagramme de Bode
bode(H, xlim=(1e-1, 1e3), y1lim=(-20, 20), y2lim=(-90, 0))
```

### Étude d'un système du second ordre

```python
# Système : H(p) = ω₀² / (p² + 2ξω₀p + ω₀²)
w0 = 10    # pulsation propre
xi = 0.3   # coefficient d'amortissement

num = [w0**2]
den = [1, 2*xi*w0, w0**2]
H = Ftransfert(num=num, den=den, gain=1, name="H")

H.info()
bode(H, xlim=(1, 1e3))
```

### Comparaison de plusieurs gains

```python
H = Ftransfert(zeros=[(-2, 0)], poles=[(-5, 0)], gain=1)

# Tracer pour différents gains
bode(H, gains=[0.1, 1, 10], 
     labels=['K=0.1', 'K=1', 'K=10'],
     xlim=(0.1, 100))
```

## Notes importantes

- Il s'agit d'une version "Born Again" d'un module de 2019-2020, complètement réécrit pour corriger les bugs et améliorer les fonctionnalités
- La bibliothèque supporte trois types de définition de fonctions de transfert : "roots", "polys" et "functions"
- Les tracés TikZ/PGF sont optimisés pour l'intégration dans des documents LaTeX scientifiques
- Le dépliage de phase utilise un algorithme personnalisé de suivi de surface de Riemann

## Auteur

fmv (2025)

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou des pull requests.
