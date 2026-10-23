import pandas as pd
import pytest

from ventes.indicateurs import NON_REFERENCE, enrichir, filtrer_periode, indicateurs_mois_region


@pytest.fixture
def tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ventes = pd.DataFrame(
        {
            "id_commande": [1, 2, 3],
            "date": pd.to_datetime(["2025-01-05", "2025-01-20", "2025-02-03"]),
            "code_region": ["IDF", "IDF", "BRE"],
            "id_produit": ["P01", "P02", "P99"],
            "quantite": [2, 1, 3],
            "prix_unitaire": [10.0, 50.0, 5.0],
        }
    )
    produits = pd.DataFrame(
        {"id_produit": ["P01", "P02"], "produit": ["Souris", "Clavier"], "categorie": ["Informatique", "Informatique"]}
    )
    regions = pd.DataFrame(
        {"code_region": ["IDF", "BRE"], "region": ["Île-de-France", "Bretagne"], "objectif_mensuel": [100, 10]}
    )
    return ventes, produits, regions


def test_enrichir_garde_toutes_les_ventes(tables) -> None:
    ventes, produits, regions = tables
    df = enrichir(ventes, produits, regions)
    assert len(df) == len(ventes)
    assert df.loc[df["id_produit"] == "P99", "categorie"].item() == NON_REFERENCE
    assert df["montant"].tolist() == [20.0, 50.0, 15.0]


def test_indicateurs_par_mois_et_region(tables) -> None:
    indicateurs = indicateurs_mois_region(enrichir(*tables))
    janvier_idf = indicateurs[(indicateurs["mois"] == "2025-01-01") & (indicateurs["region"] == "Île-de-France")]
    assert janvier_idf["ca"].item() == 70.0
    assert janvier_idf["nb_commandes"].item() == 2
    assert janvier_idf["taux_realisation"].item() == pytest.approx(0.7)
    assert len(indicateurs) == 2


def test_filtrer_periode_inclut_le_dernier_mois(tables) -> None:
    df = enrichir(*tables)
    assert len(filtrer_periode(df, fin="2025-01")) == 2
    assert len(filtrer_periode(df, debut="2025-02")) == 1
