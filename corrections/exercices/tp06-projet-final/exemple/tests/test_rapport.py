import pandas as pd
import pytest

from rapport_ventes.rapport import alertes, construire_html, euros


@pytest.fixture
def donnees() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.DataFrame(
        {
            "id_commande": [1, 2, 3],
            "date": pd.to_datetime(["2025-01-05", "2025-02-10", "2025-02-11"]),
            "produit": ["Souris", "Clavier", "Souris"],
            "montant": [100.0, 200.0, 50.0],
        }
    )
    indicateurs = pd.DataFrame(
        {
            "mois": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-02-01"]),
            "region": ["Bretagne", "Bretagne", "Occitanie"],
            "ca": [100.0, 200.0, 50.0],
            "objectif_mensuel": [100, 100, 100],
            "taux_realisation": [1.0, 2.0, 0.5],
        }
    )
    return df, indicateurs


def test_alertes_du_dernier_mois(donnees) -> None:
    _, indicateurs = donnees
    resultat = alertes(indicateurs, seuil=0.8)
    assert resultat["region"].tolist() == ["Occitanie"]


def test_euros() -> None:
    assert euros(1234567.4) == "1 234 567 €"


def test_rapport_contient_les_sections(donnees) -> None:
    df, indicateurs = donnees
    html = construire_html(df, indicateurs, "Rapport test", 0.8)
    assert "<h1>Rapport test</h1>" in html
    assert "Occitanie" in html
    assert html.count("data:image/png;base64,") == 3
