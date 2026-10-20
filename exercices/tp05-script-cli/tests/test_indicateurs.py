import pandas as pd
import pytest

from ventes.indicateurs import NON_REFERENCE, enrichir


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


# TODO : tester indicateurs_mois_region sur la même fixture :
# en janvier, l'Île-de-France a 2 commandes, un chiffre d'affaires de 70 et un taux de réalisation de 0,7
# (comparer un décimal avec pytest.approx) ; la table compte 2 lignes.

# TODO : tester filtrer_periode sur la même fixture :
# avec fin="2025-01", il reste les 2 ventes de janvier ; avec debut="2025-02", la seule vente de février.
