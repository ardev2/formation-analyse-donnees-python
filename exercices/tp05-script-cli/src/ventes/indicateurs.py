import logging

import pandas as pd

logger = logging.getLogger(__name__)

NON_REFERENCE = "Non référencé"


def enrichir(ventes: pd.DataFrame, produits: pd.DataFrame, regions: pd.DataFrame) -> pd.DataFrame:
    """Joint les ventes aux produits et aux régions sans perdre de ligne, et ajoute la colonne montant.

    Les ventes de produits absents du catalogue reçoivent le libellé NON_REFERENCE
    et sont signalées par un avertissement dans le journal.
    """
    raise NotImplementedError


def indicateurs_mois_region(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule une ligne par mois et par région.

    Colonnes : mois (premier jour du mois), region, ca, nb_commandes, panier_moyen,
    quantite, objectif_mensuel, taux_realisation.
    """
    raise NotImplementedError


def filtrer_periode(df: pd.DataFrame, debut: str | None = None, fin: str | None = None) -> pd.DataFrame:
    """Garde les ventes entre le mois de début et le mois de fin inclus, au format AAAA-MM."""
    raise NotImplementedError
