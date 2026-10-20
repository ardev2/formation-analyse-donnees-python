# TP6 : projet fil rouge

## Objectif

Créer, de zéro et avec uv, un projet Python complet et reproductible qui réunit tout ce qui a été vu pendant la formation :

- un paquet Python structuré, avec ses dépendances déclarées dans `pyproject.toml` ;
- un notebook d'analyse qui s'appuie sur les données des jours précédents et importe le code du paquet ;
- une commande qui produit un rapport ou un graphique final.

## Livrable

Un projet autonome et reproductible : une autre personne doit pouvoir le récupérer, lancer `uv sync`, puis obtenir le même résultat avec une seule commande. Le projet est présenté au groupe en fin de formation, en 5 minutes par participant ou par binôme.

## Les données

Le dossier `ressources/` contient les données du TP3 : les ventes mensuelles de janvier à septembre 2025, le catalogue des produits et le référentiel des régions avec leurs objectifs.

## Les chiffres de contrôle

Ton projet part des mêmes données que les TP3 et TP5 : ses résultats doivent retrouver les mêmes chiffres. Vérifie-les dans ton notebook et dans un test de recette.

| Contrôle | Résultat attendu |
|---|---|
| fichiers de ventes lus | 9 |
| ventes chargées | 2182 |
| ventes de produits hors catalogue | 17, toutes du produit `P17` |
| chiffre d'affaires total, janvier à septembre | 409 501,59 euros |
| lignes de la table mois par région | 54 (9 mois, 6 régions) |
| couples mois et région où l'objectif est atteint | 25 sur 54 |
| région au plus fort chiffre d'affaires | Île-de-France, 127 936,94 euros |
| catégorie au plus fort chiffre d'affaires | Informatique, 185 274,68 euros |
| mois le plus fort, le plus faible | septembre (58 073,80 euros), août (27 273,63 euros) |
| montant moyen et médian d'une commande | 187,67 euros et 104,70 euros |

## Cahier des charges

### 1. Le projet

- Créé avec `uv init --package`, avec un nom qui dit ce qu'il fait.
- Dépendances ajoutées avec `uv add`, outils de développement avec `uv add --dev` (au minimum pytest, ruff et jupyterlab).
- La structure vue ce matin : `data/brut`, `notebooks`, `src/<paquet>`, `tests`, `outputs`, un `config.yaml`.
- Le fichier `uv.lock` fait partie du livrable.

### 2. Le code

- Tu peux repartir de ton paquet du TP5 : copie ses modules dans ton nouveau projet et adapte les imports.
- Un nouveau module produit la sortie finale, au choix :
  - un **rapport HTML** avec des chiffres clés, des graphiques et un tableau ;
  - un ou plusieurs **graphiques** enregistrés en PNG ou en HTML interactif ;
  - un **fichier Excel** de restitution, avec une feuille par vue.
- Les fonctions sont typées, les erreurs sur les données lèvent des exceptions du projet.
- Aucun chemin en dur dans `src/` : tout passe par `config.yaml` ou par les arguments de la commande.

### 3. La commande

- Déclarée dans `[project.scripts]`, lancée avec `uv run <commande>`.
- Au moins une option utile, par exemple une période (`--debut`, `--fin`) ou un fichier de configuration.
- Un journal dans la console et dans un fichier.
- Un code de sortie à 0 en cas de succès, à 1 en cas d'erreur.

### 4. Le notebook

- `notebooks/01_analyse.ipynb`, qui importe les fonctions du paquet au lieu de recopier le code.
- Trois à cinq graphiques ou tableaux, chacun suivi d'un commentaire qui dit ce qu'il faut en retenir.
- Une conclusion avec deux ou trois constats ou recommandations.
- Il s'exécute sans erreur de haut en bas.

### 5. Les tests

- Au moins trois tests, dont un qui vérifie qu'une erreur attendue est bien levée.
- `uv run pytest` passe.

### 6. Les finitions

- Un `README.md` qui explique ce que fait le projet, comment l'installer, comment l'utiliser, quelles données il attend et comment il est organisé.
- Un `.gitignore` qui exclut au moins `.venv/`, `__pycache__/`, `outputs/` et `.env`.
- `uv run ruff check .` ne signale rien.

## Idées de sujet

Toutes partent des mêmes données. Choisis celle qui t'intéresse, ou propose la tienne :

- **Le rapport mensuel de la direction commerciale** : chiffres clés, évolution, régions, alertes sur les objectifs non atteints.
- **Le suivi des objectifs** : taux de réalisation par région, proposition d'objectifs saisonnalisés à partir de l'historique.
- **L'analyse du catalogue** : produits qui portent le chiffre d'affaires, produits en perte de vitesse, produits hors catalogue.
- **La fidélité** : comparaison des clients fidèles et des autres, panier moyen, catégories achetées.

## Étapes conseillées

1. Créer le projet, ajouter les dépendances, recopier les données dans `data/brut`. Cette étape se fait pendant le cours, juste après la présentation du fichier `pyproject.toml`.
2. Faire fonctionner le chargement et les indicateurs, en reprenant le TP5.
3. Explorer dans le notebook, choisir les trois ou quatre messages principaux.
4. Écrire le module qui produit la sortie finale, puis la commande.
5. Écrire les tests, le README, vérifier ruff.
6. Faire le test du collègue : copier le projet dans un dossier vide, sans `.venv` ni `outputs`, puis `uv sync`, `uv run pytest` et la commande.
7. Préparer la présentation.

## Vérifier le projet

Depuis une copie vierge du projet, chaque commande doit donner le résultat attendu :

| Commande | Résultat attendu |
|---|---|
| `uv sync --locked` | l'environnement est créé, sans erreur : `uv.lock` est à jour par rapport à `pyproject.toml` |
| `uv run pytest` | une dernière ligne du type `5 passed`, sans `failed` ni `error` |
| `uv run ruff check .` | `All checks passed!` |
| `uv run <commande> --help` | l'aide de la commande, avec ses options |
| `uv run <commande>` | le rapport ou les graphiques dans `outputs/`, un journal, et un code de sortie à 0 (`echo $?`) |
| `uv run <commande> --config absent.yaml` | un message d'erreur clair, sans trace technique, et un code de sortie à 1 |
| `uv run jupyter lab`, puis *Restart Kernel and Run All Cells* sur le notebook | aucune erreur, des chiffres identiques à ceux du tableau de contrôle |

## La présentation : 5 minutes

1. **Le besoin** (30 secondes) : à quelle question répond le projet, pour qui.
2. **La démonstration** (2 minutes) : lancer la commande, montrer le résultat.
3. **Ce que disent les données** (1 minute 30) : deux ou trois constats tirés du notebook.
4. **Sous le capot** (1 minute) : la structure du projet, un choix technique dont tu es content, une difficulté rencontrée.

## Grille de vérification

- [ ] `uv sync` puis la commande fonctionnent depuis une copie vierge du projet.
- [ ] `pyproject.toml` et `uv.lock` sont présents, les outils de développement sont dans le groupe `dev`.
- [ ] La structure `data/brut`, `notebooks`, `src`, `tests`, `outputs` est respectée.
- [ ] Le code est typé, sans chemin en dur, avec des exceptions du projet.
- [ ] La commande a au moins une option, un journal et un code de sortie.
- [ ] Le notebook importe le paquet et s'exécute de haut en bas.
- [ ] Au moins trois tests passent.
- [ ] Le README permet à quelqu'un d'autre d'utiliser le projet sans poser de question.
- [ ] `uv run ruff check .` ne signale rien.
