# TP5 : d'un notebook à un script en ligne de commande

## Objectif

Transformer le traitement du TP3 (assembler les ventes mensuelles, les joindre aux produits et aux régions, calculer les indicateurs par mois et par région) en un outil autonome :

- un paquet Python `ventes`, avec des fonctions typées réparties en modules ;
- des exceptions propres au projet, avec des messages clairs ;
- des tests automatiques ;
- une commande `ventes`, avec des paramètres, des journaux et un fichier de configuration.

## Livrable

Ce dossier complété : le paquet `src/ventes`, les tests, un fichier `config.yaml`, et une commande `uv run ventes` qui fonctionne de bout en bout, sans erreur, et produit `outputs/indicateurs_mois_region.parquet` et un journal `outputs/ventes.log`.

## Le projet de départ

```text
tp05-script-cli/
  pyproject.toml          description du projet, dépendances, commande ventes
  data/
    brut/                 les fichiers du TP3 : ventes/, produits.csv, regions.csv
    exemples_erreurs/     un fichier de ventes défectueux, pour tester les erreurs
  notebooks/              ton notebook du TP3, à copier ici
  src/ventes/
    erreurs.py            exceptions du projet
    chargement.py         lire et contrôler les fichiers
    indicateurs.py        joindre et calculer
    config.py             lire la configuration
    cli.py                point d'entrée de la commande
  tests/
    test_chargement.py    tests à compléter
    test_indicateurs.py   tests à compléter
    test_config.py        tests à écrire
    test_recette.py       tests de recette fournis : les résultats attendus sur les vraies données
  outputs/                résultats produits par la commande
```

Les fonctions sont déjà déclarées, avec leurs annotations de type et une description de ce qu'elles doivent faire. Leur corps contient `raise NotImplementedError` : c'est à toi de l'écrire.

## Comment vérifier ton travail

Le fichier `tests/test_recette.py` est fourni et ne doit pas être modifié. Il contrôle les résultats attendus sur les vraies données : 9 fichiers et 2182 ventes chargées, 17 ventes hors catalogue, une table de 54 lignes d'indicateurs avec un chiffre d'affaires total de 409 501,59 euros, 307 ventes en juillet et août, une commande qui renvoie le code 0 en cas de succès et 1 avec un fichier défectueux. Ses tests échouent au départ ; à la fin du TP, ils doivent tous passer.

Chaque étape ci-dessous indique aussi le **résultat attendu** des commandes à lancer.

Le TP suit le cours de la matinée : chaque étape se fait après la section du cours correspondante, indiquée en italique.

---

## Étape 0 : préparer l'environnement avec uv

*Après la section 1 du cours : de pip et venv à uv.*

1. Installe uv, puis vérifie-le avec `uv --version` :
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```
2. Dans ce dossier, crée l'environnement et installe les dépendances déclarées dans `pyproject.toml` :
   ```bash
   uv sync
   ```
   uv utilise le Python 3.12 du poste et crée le dossier `.venv`, sans qu'il soit nécessaire de l'activer.
3. Lance les tests :
   ```bash
   uv run pytest
   ```
   Résultat attendu : tous les tests échouent avec `NotImplementedError`, puisque les fonctions ne sont pas encore écrites. La dernière ligne ressemble à :
   ```text
   5 failed, 3 errors in 9.17s
   ```

## Étape 1 : repérer les blocs à extraire

*Après les sections 2 et 3 du cours : structurer un projet data, du notebook au module.*

Copie ton notebook du TP3 dans `notebooks/`. Relis-le et repère les blocs qui correspondent à chaque fonction déclarée dans `src/ventes/`. Pour ouvrir le notebook dans l'environnement du projet :

```bash
uv add --dev jupyterlab
uv run jupyter lab
```

Résultat attendu : pour chaque fonction de `chargement.py` et de `indicateurs.py`, tu sais quelles cellules du notebook elle remplace. Note-le en commentaire dans le notebook.

## Étape 2 : les exceptions

*Après les sections 4 et 5 du cours : annotations de type et exceptions.*

Dans `erreurs.py`, complète `DossierVideError` et écris `ColonnesManquantesError` et `CleNonUniqueError`, en héritant de `VentesError`. Chaque exception produit un message qui permet de comprendre le problème sans lire le code.

Résultat attendu, à vérifier dans un terminal Python (`uv run python`) :

```python
>>> from pathlib import Path
>>> from ventes.erreurs import ColonnesManquantesError, DossierVideError
>>> print(DossierVideError(Path("data/brut/ventes"), "*.csv"))
aucun fichier *.csv dans data/brut/ventes
>>> erreur = ColonnesManquantesError(Path("data/brut/ventes/ventes_2025_10.csv"), {"quantite"})
>>> print(erreur)
ventes_2025_10.csv : colonnes manquantes ['quantite']
>>> erreur.manquantes
{'quantite'}
```

## Étape 3 : le chargement

*Après la section 6 du cours : tester avec pytest.*

Dans `chargement.py`, écris les quatre fonctions. Elles lèvent les exceptions de l'étape 2 quand les données ne sont pas conformes, et écrivent dans le journal (`logger.info`) le nombre de fichiers et de lignes chargés.

Complète `tests/test_chargement.py`, puis vérifie :

```bash
uv run pytest tests/test_chargement.py
uv run pytest tests/test_recette.py -k 2182
```

Résultat attendu : tous les tests de `test_chargement.py` passent, ainsi que le test de recette `test_les_9_fichiers_donnent_2182_ventes`.

## Étape 4 : les indicateurs

Dans `indicateurs.py`, écris `enrichir`, `indicateurs_mois_region` et `filtrer_periode`. `enrichir` écrit un avertissement (`logger.warning`) s'il trouve des produits hors catalogue.

Complète `tests/test_indicateurs.py`, puis vérifie avec `uv run pytest`.

Résultat attendu : tous les tests passent, sauf les deux tests de recette qui appellent la commande (`test_commande_de_bout_en_bout` et `test_commande_avec_un_fichier_defectueux`), puisque `cli.py` n'est pas encore écrit.

## Étape 5 : la configuration

*Après les sections 7 à 9 du cours : argparse, logging et configuration.*

Crée un fichier `config.yaml` à la racine du TP, avec deux sections :

- `donnees` : les chemins `ventes` (le dossier des fichiers mensuels), `produits` et `regions` ;
- `sorties` : les chemins `indicateurs` (le fichier Parquet produit) et `journal` (le fichier de log).

Dans `config.py`, écris `charger_config`, qui lit le fichier avec `yaml.safe_load` et lève `ConfigurationError` si le fichier est absent, s'il n'est pas un YAML valide ou s'il manque une clé. Écris les trois tests décrits dans `tests/test_config.py`.

Résultat attendu :

```bash
uv run pytest tests/test_config.py
```

```text
3 passed
```

## Étape 6 : la commande

Dans `cli.py` :

1. Dans `creer_parser`, déclare avec `argparse` les options `--config` (défaut `config.yaml`), `--sortie`, `--debut`, `--fin` et `--verbose`.
2. Dans `main`, configure les journaux : la console au niveau `INFO` (ou `DEBUG` avec `--verbose`), et un fichier de journal dont le chemin vient de la configuration.
3. Enchaîne le traitement : configuration, chargement, enrichissement, filtre de période, indicateurs, écriture du fichier Parquet.
4. Attrape les `VentesError` : écris l'erreur dans le journal et renvoie `1`. Renvoie `0` si tout s'est bien passé.

La commande `ventes` est déjà déclarée dans `pyproject.toml`, section `[project.scripts]`.

Résultat attendu de `uv run ventes --help` (les textes d'aide peuvent différer selon ta rédaction) :

```text
usage: ventes [-h] [-c CONFIG] [-o SORTIE] [--debut DEBUT] [--fin FIN] [-v]

Consolide les fichiers de ventes mensuels et calcule les indicateurs par mois
et par région.

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        fichier de configuration (défaut : config.yaml)
  -o SORTIE, --sortie SORTIE
                        fichier Parquet de sortie, remplace celui de la
                        configuration
  --debut DEBUT         premier mois à inclure, au format AAAA-MM
  --fin FIN             dernier mois à inclure, au format AAAA-MM
  -v, --verbose         affiche le détail du traitement
```

## Étape 7 : vérifier de bout en bout

```bash
uv run ventes
```

Résultat attendu, aux dates et heures près :

```text
2026-10-14 16:06:30,431 INFO     ventes.chargement : 9 fichiers trouvés dans data/brut/ventes
2026-10-14 16:06:30,442 INFO     ventes.chargement : 2182 ventes chargées
2026-10-14 16:06:30,445 WARNING  ventes.indicateurs : 17 ventes de produits hors catalogue : P17
2026-10-14 16:06:30,464 INFO     ventes : 54 lignes d'indicateurs écrites dans outputs/indicateurs_mois_region.parquet
```

Les mêmes lignes figurent dans `outputs/ventes.log`. Avec une période :

```bash
uv run ventes --debut 2025-07 --fin 2025-08 --sortie outputs/ete.parquet
```

Résultat attendu : la dernière ligne annonce `12 lignes d'indicateurs écrites dans outputs/ete.parquet` (2 mois et 6 régions).

Simule ensuite un fichier défectueux : copie `data/exemples_erreurs/ventes_sans_quantite.csv` dans `data/brut/ventes/` sous le nom `ventes_2025_10.csv`, relance `uv run ventes`, puis affiche le code de sortie avec `echo $?`. Résultat attendu :

```text
2026-10-14 16:06:31,084 INFO     ventes.chargement : 10 fichiers trouvés dans data/brut/ventes
2026-10-14 16:06:31,096 ERROR    ventes : ventes_2025_10.csv : colonnes manquantes ['quantite']
1
```

Un message clair, sans trace technique, et un code de sortie à 1. Supprime ensuite le fichier `ventes_2025_10.csv`.

Lance enfin tous les tests et vérifie la qualité du code :

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
uv run mypy src
```

Résultat attendu : tous les tests passent, recette comprise ; `ruff check` affiche `All checks passed!` et `mypy` affiche `Success: no issues found`.

## Pour aller plus loin

- Dans ton notebook, remplace le code du TP3 par des appels aux fonctions du paquet (`from ventes.chargement import charger_ventes`).
- Ajoute un test de la fonction `main`, en l'appelant avec une liste d'arguments sur un petit jeu de données écrit dans `tmp_path` : `main(["--config", "..."])`.
- Ajoute une option `--format` qui permet d'écrire aussi le résultat en CSV.

## Avant de rendre

- `uv run pytest` : tous les tests passent, y compris ceux de `test_recette.py`.
- `uv run ventes` produit le fichier Parquet et le journal, sans erreur.
- Un fichier défectueux produit un message clair et un code de sortie à 1.
- Aucun chemin n'est écrit en dur dans `src/` : tout passe par la configuration ou les arguments.
