# rapport-ventes

Produit le rapport des ventes de la boutique : chiffres clés, évolution mensuelle, répartition par région, suivi des objectifs et alertes sur les régions en retard.

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Utilisation

```bash
uv run rapport-ventes
uv run rapport-ventes --debut 2025-07 --fin 2025-08
uv run rapport-ventes --config autre_config.yaml --verbose
```

La commande écrit dans `outputs/` :

- `rapport.html`, le rapport à ouvrir dans un navigateur ou à envoyer par mail ;
- `indicateurs_mois_region.parquet`, la table des indicateurs par mois et par région ;
- `rapport.log`, le journal de l'exécution.

Elle renvoie le code 0 en cas de succès et 1 en cas d'erreur sur les données ou la configuration.

## Données

Les fichiers attendus, dont les chemins sont définis dans `config.yaml` :

| Fichier | Contenu |
|---|---|
| `data/brut/ventes/ventes_AAAA_MM.csv` | une ligne par commande : `id_commande`, `date`, `code_region`, `id_produit`, `quantite`, `prix_unitaire`, `client_fidele` |
| `data/brut/produits.csv` | le catalogue : `id_produit`, `produit`, `categorie`, `prix_catalogue` |
| `data/brut/regions.csv` | les régions : `code_region`, `region`, `objectif_mensuel` |

Pour un nouveau mois, il suffit de déposer son fichier dans `data/brut/ventes/` et de relancer la commande.

## Configuration

`config.yaml` définit les chemins des données et des sorties, le titre du rapport et le seuil d'alerte (0.8 : une région est signalée si elle réalise moins de 80 % de son objectif le dernier mois).

## Structure

```text
config.yaml
data/brut/              données reçues, jamais modifiées
notebooks/
  01_analyse.ipynb      analyse commentée, qui importe le paquet
src/rapport_ventes/
  chargement.py         lecture et contrôle des fichiers
  indicateurs.py        jointures et indicateurs
  graphiques.py         graphiques matplotlib
  rapport.py            construction du rapport HTML
  config.py             lecture de la configuration
  erreurs.py            exceptions du projet
  cli.py                commande rapport-ventes
tests/                  tests pytest, dont test_recette.py : les chiffres de contrôle du cahier des charges
outputs/                fichiers produits, non versionnés
```

## Développement

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
uv run jupyter lab
```
