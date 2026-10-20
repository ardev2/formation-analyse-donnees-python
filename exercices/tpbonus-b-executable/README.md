# TP bonus B : empaqueter le script en exécutable

## Objectif

Reprendre la commande `ventes` du TP5 et l'empaqueter avec PyInstaller pour obtenir un exécutable autonome.

## Livrable

Un exécutable qui fonctionne sur ta machine sans environnement Python installé, livré dans un dossier `distribution/` avec son fichier de configuration.

## Prérequis

Le TP5 terminé : dans son dossier, `uv run ventes` fonctionne. Toutes les commandes ci-dessous se lancent depuis le dossier du TP5.

Rappel : l'exécutable est propre au système sur lequel il est construit. Construit sous Windows, il donne un `.exe` pour Windows ; sous macOS, un binaire pour macOS.

---

## Étape 1 : le script de lancement

PyInstaller part d'un script, pas d'une commande déclarée dans `pyproject.toml`. Crée à la racine du TP5 un fichier `lancer_ventes.py` qui importe la fonction `main` de `ventes.cli`, l'appelle, et termine le programme avec son code de sortie (`sys.exit`).

Vérifie qu'il fonctionne :

```bash
uv run python lancer_ventes.py --help
```

## Étape 2 : un exécutable en un seul fichier

```bash
uv add --dev pyinstaller
uv run pyinstaller --onefile --name ventes lancer_ventes.py
```

La construction prend une à deux minutes. L'exécutable se trouve dans `dist/`. Ajoute `build/`, `dist/` et `*.spec` au `.gitignore`.

Lance-le :

```bash
./dist/ventes --help          # macOS, Linux
dist\ventes.exe --help        # Windows
./dist/ventes
```

Quelle est la taille du fichier ? Combien de temps met-il à afficher l'aide ?

## Étape 3 : un exécutable en dossier

```bash
uv run pyinstaller --onedir --name ventes_dossier lancer_ventes.py
```

Compare la taille du dossier `dist/ventes_dossier/` et le temps de démarrage, au premier lancement puis aux suivants. Quel mode choisirais-tu pour un traitement lancé chaque jour par une tâche planifiée ? Pour un fichier à envoyer à un collègue ?

## Étape 4 : préparer la distribution

L'exécutable contient le code, mais ni la configuration ni les données.

1. Crée un dossier `distribution/` et copie dedans l'exécutable (ou le dossier), un `config.yaml` et un dossier `data/brut/` avec les données.
2. Adapte les chemins de `config.yaml` pour qu'ils soient relatifs au dossier `distribution/`.
3. Ouvre un **nouveau terminal**, sans environnement activé et sans passer par `uv`, place-toi dans `distribution/` et lance l'exécutable.
4. Vérifie que `outputs/indicateurs_mois_region.parquet` et le journal sont bien produits, et qu'une configuration absente donne un message clair et un code de sortie à 1.

## Pour aller plus loin

- Ajoute une icône avec l'option `--icon`.
- Si tu as fait l'interface tkinter du cours, empaquette-la avec `--windowed`, pour qu'aucun terminal ne s'ouvre.
- Compare avec `uv tool install .`, qui installe la commande `ventes` pour les utilisateurs qui ont uv.

## Avant de rendre

- L'exécutable fonctionne depuis un terminal sans Python ni uv.
- Le dossier `distribution/` contient tout ce qu'il faut pour le lancer.
- Tu sais expliquer la différence entre `--onefile` et `--onedir`.
