import logging
from pathlib import Path

import pandas as pd

from ventes.erreurs import CleNonUniqueError, ColonnesManquantesError, DossierVideError

logger = logging.getLogger(__name__)

COLONNES_VENTES = {"id_commande", "date", "code_region", "id_produit", "quantite", "prix_unitaire", "client_fidele"}


def lister_fichiers(dossier: Path, pattern: str = "*.csv") -> list[Path]:
    fichiers = sorted(dossier.glob(pattern))
    if not fichiers:
        raise DossierVideError(dossier, pattern)
    logger.info("%d fichiers trouvés dans %s", len(fichiers), dossier)
    return fichiers


def charger_fichier_ventes(fichier: Path) -> pd.DataFrame:
    ventes = pd.read_csv(fichier, parse_dates=["date"])
    manquantes = COLONNES_VENTES - set(ventes.columns)
    if manquantes:
        raise ColonnesManquantesError(fichier, manquantes)
    ventes["fichier"] = fichier.name
    logger.debug("%s : %d lignes", fichier.name, len(ventes))
    return ventes


def charger_ventes(dossier: Path, pattern: str = "*.csv") -> pd.DataFrame:
    fichiers = lister_fichiers(dossier, pattern)
    ventes = pd.concat([charger_fichier_ventes(f) for f in fichiers], ignore_index=True)
    verifier_unicite(ventes, "id_commande", "ventes")
    logger.info("%d ventes chargées", len(ventes))
    return ventes


def charger_reference(fichier: Path, cle: str) -> pd.DataFrame:
    reference = pd.read_csv(fichier)
    verifier_unicite(reference, cle, fichier.name)
    return reference


def verifier_unicite(df: pd.DataFrame, cle: str, source: str) -> None:
    nb_doublons = int(df[cle].duplicated().sum())
    if nb_doublons:
        raise CleNonUniqueError(source, cle, nb_doublons)
