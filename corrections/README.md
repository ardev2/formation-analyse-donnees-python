# Corrections

Ce dossier contient tous les corrigés de la formation. Il reproduit l'arborescence du dépôt : chaque fichier se trouve au chemin qu'il aurait à côté de son TP.

```
corrections/
  exercices/
    tp00-verification-environnement/tp00_corrige.ipynb
    tp01-environnement-pandas/tp01_corrige.ipynb
    tp02-nettoyage/tp02_corrige.ipynb
    tp03-indicateurs/tp03_corrige.ipynb
    tp04-mini-visualisation/tp04_mini_corrige.ipynb
    tp04-tableau-de-bord/tp04_corrige.ipynb
    tp05-script-cli/corrige/        solution complète du TP5 (projet uv)
    tp06-projet-final/exemple/      exemple de projet final : rapport-ventes
    tpbonus-a-streamlit/corrige/    application Streamlit complète
    tpbonus-b-executable/corrige/   script de lancement et commandes PyInstaller
    tpbonus-c-pyspark/tpbonus_c_corrige.ipynb
```

Les notebooks corrigés sont déjà exécutés : on peut les lire tels quels.

## Exécuter un corrigé

Les corrigés lisent les données des dossiers de TP (`ressources/`, `data/`). Pour les exécuter, on les copie d'abord à leur place, depuis la racine du dépôt :

```bash
cp -R corrections/exercices/. exercices/
```

Chaque corrigé se lance ensuite comme indiqué dans son README, par exemple :

```bash
cd exercices/tp05-script-cli/corrige
uv sync
uv run pytest
```
