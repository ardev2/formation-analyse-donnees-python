# Corrigé du TP bonus B

## Le script de lancement

`lancer_ventes.py`, à placer à la racine du TP5 :

```python
import sys

from ventes.cli import main

sys.exit(main())
```

## Construire

Depuis le dossier du TP5 :

```bash
uv add --dev pyinstaller
uv run pyinstaller --onefile --name ventes lancer_ventes.py
uv run pyinstaller --onedir --name ventes_dossier lancer_ventes.py
```

Ajouter au `.gitignore` :

```text
build/
dist/
*.spec
distribution/
```

## Résultats mesurés sur macOS, avec pandas et pyarrow

| Mode | Taille | Affichage de l'aide |
|---|---|---|
| `--onefile` | 62 Mo | environ 15 s à chaque lancement |
| `--onedir` | 175 Mo | environ 18 s au premier lancement, 0,2 s ensuite |

En `--onefile`, tout le contenu est décompressé dans un dossier temporaire à chaque lancement. En `--onedir`, les fichiers sont déjà en place : seul le premier lancement est ralenti par la vérification du système.

Pour une tâche planifiée qui tourne chaque jour, le mode dossier s'impose. Pour envoyer un outil ponctuel à un collègue, le fichier unique est plus pratique.

## Préparer la distribution

```text
distribution/
  ventes              (ventes.exe sous Windows)
  config.yaml
  data/brut/
    ventes/
    produits.csv
    regions.csv
```

`config.yaml`, avec des chemins relatifs au dossier `distribution/` :

```yaml
donnees:
  ventes: data/brut/ventes
  produits: data/brut/produits.csv
  regions: data/brut/regions.csv

sorties:
  indicateurs: outputs/indicateurs_mois_region.parquet
  journal: outputs/ventes.log
```

Dans un nouveau terminal, sans environnement activé :

```bash
cd distribution
./ventes                 # produit outputs/indicateurs_mois_region.parquet et outputs/ventes.log
./ventes -c absent.yaml  # message clair, code de sortie 1
```
