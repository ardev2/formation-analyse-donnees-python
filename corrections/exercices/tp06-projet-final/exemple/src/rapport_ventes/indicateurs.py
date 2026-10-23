import logging

import pandas as pd

logger = logging.getLogger(__name__)

NON_REFERENCE = "Non référencé"


def enrichir(ventes: pd.DataFrame, produits: pd.DataFrame, regions: pd.DataFrame) -> pd.DataFrame:
    df = ventes.merge(produits, on="id_produit", how="left", validate="many_to_one").merge(
        regions, on="code_region", how="left", validate="many_to_one"
    )
    hors_catalogue = df["produit"].isna()
    if hors_catalogue.any():
        codes = sorted(df.loc[hors_catalogue, "id_produit"].unique())
        logger.warning("%d ventes de produits hors catalogue : %s", hors_catalogue.sum(), ", ".join(codes))
    df[["produit", "categorie"]] = df[["produit", "categorie"]].fillna(NON_REFERENCE)
    df["montant"] = df["prix_unitaire"] * df["quantite"]
    return df


def indicateurs_mois_region(df: pd.DataFrame) -> pd.DataFrame:
    indicateurs = (
        df.assign(mois=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby(["mois", "region"], as_index=False)
        .agg(
            ca=("montant", "sum"),
            nb_commandes=("id_commande", "count"),
            panier_moyen=("montant", "mean"),
            quantite=("quantite", "sum"),
            objectif_mensuel=("objectif_mensuel", "first"),
        )
    )
    indicateurs["taux_realisation"] = indicateurs["ca"] / indicateurs["objectif_mensuel"]
    return indicateurs


def filtrer_periode(df: pd.DataFrame, debut: str | None = None, fin: str | None = None) -> pd.DataFrame:
    masque = pd.Series(True, index=df.index)
    if debut:
        masque &= df["date"] >= pd.Timestamp(debut)
    if fin:
        masque &= df["date"] < pd.Timestamp(fin) + pd.offsets.MonthBegin(1)
    return df[masque]
