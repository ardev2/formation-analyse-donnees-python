"""Tests de recette : les chiffres de contrôle du cahier des charges, sur les vraies données."""

from pathlib import Path

import pandas as pd
import pytest

from rapport_ventes.chargement import charger_reference, charger_ventes
from rapport_ventes.indicateurs import NON_REFERENCE, enrichir, indicateurs_mois_region

DONNEES = Path(__file__).resolve().parent.parent / "data" / "brut"


@pytest.fixture(scope="module")
def ventes_enrichies() -> pd.DataFrame:
    ventes = charger_ventes(DONNEES / "ventes")
    produits = charger_reference(DONNEES / "produits.csv", "id_produit")
    regions = charger_reference(DONNEES / "regions.csv", "code_region")
    return enrichir(ventes, produits, regions)


def test_ventes_et_hors_catalogue(ventes_enrichies: pd.DataFrame) -> None:
    assert len(ventes_enrichies) == 2182
    assert ventes_enrichies["fichier"].nunique() == 9
    hors_catalogue = ventes_enrichies[ventes_enrichies["categorie"] == NON_REFERENCE]
    assert len(hors_catalogue) == 17
    assert set(hors_catalogue["id_produit"]) == {"P17"}


def test_chiffre_d_affaires(ventes_enrichies: pd.DataFrame) -> None:
    assert ventes_enrichies["montant"].sum() == pytest.approx(409501.59, abs=0.01)
    par_region = ventes_enrichies.groupby("region")["montant"].sum()
    assert par_region.idxmax() == "Île-de-France"
    assert par_region.max() == pytest.approx(127936.94, abs=0.01)


def test_table_des_indicateurs(ventes_enrichies: pd.DataFrame) -> None:
    indicateurs = indicateurs_mois_region(ventes_enrichies)
    assert len(indicateurs) == 54
    assert (indicateurs["taux_realisation"] >= 1).sum() == 25
