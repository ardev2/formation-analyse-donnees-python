# formation-analyse-donnees-python

Ressources de formation à l'analyse de données avec Python.

## Comment récupérer les TP

Pas de compte GitHub ni de `git clone` nécessaire : clique sur **Code > Download ZIP** en haut de cette page, dézippe l'archive, et travaille en local dans le dossier du TP qui t'intéresse.

## Prérequis

Les postes de la formation sont sous Ubuntu, avec Python 3.12 déjà installé. Le TP0 (`exercices/tp00-verification-environnement`) crée un environnement virtuel, vérifie que Jupyter fonctionne et passe en revue les bases de Python : il se fait au tout début de la première matinée.

## Structure

```
cours/
  01-jour1-matin/
    environnement-pandas.pptx   # présentation (ouvrable dans PowerPoint, Keynote ou Google Slides)
    environnement-pandas.pdf    # la même présentation en PDF
  02-jour1-apres-midi/          selection-nettoyage.pptx et .pdf
  03-jour2-matin/               agregation-dates.pptx et .pdf
  04-jour2-apres-midi/          visualisation.pptx et .pdf, et visualisation-mini.pptx, version courte (15 min de cours)
  05-jour3-matin/               projet-cli.pptx et .pdf
  06-jour3-apres-midi/          uv-projet-final.pptx et .pdf
  07-bonus/                     pour-aller-plus-loin.pptx et .pdf, module bonus si le temps le permet
exercices/
  tp00-verification-environnement/
    tp00.ipynb        # vérification du poste : environnement virtuel, Jupyter, bases de Python
  tp01-environnement-pandas/
    tp01.ipynb        # notebook prérempli : cours + consignes + cellules à compléter
    ressources/       # fichiers de données fournis pour le TP
  tp02-nettoyage/
  tp03-indicateurs/
  tp04-mini-visualisation/    version mini du TP4 (30 min) : quelques graphiques avec chaque bibliothèque
  tp04-tableau-de-bord/
  tp05-script-cli/            projet Python à compléter (uv), consignes dans son README
  tp06-projet-final/          cahier des charges du projet fil rouge
  tpbonus-a-streamlit/        tableau de bord Streamlit
  tpbonus-b-executable/       exécutable PyInstaller
```

Chaque TP est autonome dans son propre dossier sous `exercices/`. Les TP1 à TP4 sont des notebooks Jupyter préremplis (consignes en Markdown, cellules de code à compléter), avec un environnement pip et venv à mettre en place soi-même. Les TP5 et TP6, au jour 3, sont des projets Python gérés avec uv.

Chaque TP est découpé en parties qui suivent les sections du cours : on alterne une courte section de cours et sa mise en pratique. Les questions indiquent souvent le **résultat attendu**, et des cellules de **vérification** contrôlent les réponses avec `assert` : elles affichent `OK` quand la réponse est juste. Pour les graphiques, le résultat attendu est une image, rangée dans le dossier `attendus/` du TP. Le TP5 fournit des tests de recette (`tests/test_recette.py`) qui vérifient les chiffres attendus. Les questions **Pour aller plus loin** sont facultatives.
