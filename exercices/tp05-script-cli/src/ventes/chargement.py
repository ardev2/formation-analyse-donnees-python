import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

COLONNES_VENTES = {"id_commande", "date", "code_region", "id_produit", "quantite", "prix_unitaire", "client_fidele"}


def lister_fichiers(dossier: Path, pattern: str = "*.csv") -> list[Path]:
    """Renvoie la liste triée des fichiers du dossier correspondant au pattern.

    Lève DossierVideError si aucun fichier ne correspond.
    """
    raise NotImplementedError


def charger_fichier_ventes(fichier: Path) -> pd.DataFrame:
    """Lit un fichier de ventes, convertit la colonne date et ajoute une colonne fichier.

    Lève ColonnesManquantesError s'il manque une des colonnes de COLONNES_VENTES.
    """
    raise NotImplementedError


def charger_ventes(dossier: Path, pattern: str = "*.csv") -> pd.DataFrame:
    """Lit et assemble tous les fichiers de ventes du dossier.

    Lève CleNonUniqueError si un id_commande apparaît plusieurs fois.
    """
    raise NotImplementedError


def charger_reference(fichier: Path, cle: str) -> pd.DataFrame:
    """Lit une table de référence (produits ou régions) et vérifie que sa clé est unique."""
    raise NotImplementedError
