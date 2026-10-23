"""Tests de recette : les résultats attendus sur les vraies données du TP.

Ce fichier est fourni et ne doit pas être modifié. Ses tests échouent tant que le paquet
n'est pas écrit ; à la fin du TP, ils doivent tous passer.
"""

import shutil
from pathlib import Path

import pandas as pd
import pytest

from ventes.chargement import charger_reference, charger_ventes
from ventes.cli import main
from ventes.indicateurs import NON_REFERENCE, enrichir, filtrer_periode, indicateurs_mois_region

DONNEES = Path(__file__).resolve().parents[5] / "exercices" / "tp05-script-cli" / "data"

COLONNES_INDICATEURS = [
    "mois",
    "region",
    "ca",
    "nb_commandes",
    "panier_moyen",
    "quantite",
    "objectif_mensuel",
    "taux_realisation",
]


@pytest.fixture(scope="module")
def ventes_enrichies() -> pd.DataFrame:
    ventes = charger_ventes(DONNEES / "brut" / "ventes")
    produits = charger_reference(DONNEES / "brut" / "produits.csv", "id_produit")
    regions = charger_reference(DONNEES / "brut" / "regions.csv", "code_region")
    return enrichir(ventes, produits, regions)


def ecrire_config(dossier: Path, dossier_ventes: Path) -> Path:
    config = dossier / "config.yaml"
    config.write_text(
        "donnees:\n"
        f"  ventes: {dossier_ventes}\n"
        f"  produits: {DONNEES / 'brut' / 'produits.csv'}\n"
        f"  regions: {DONNEES / 'brut' / 'regions.csv'}\n"
        "sorties:\n"
        f"  indicateurs: {dossier / 'indicateurs.parquet'}\n"
        f"  journal: {dossier / 'ventes.log'}\n",
        encoding="utf-8",
    )
    return config


def test_les_9_fichiers_donnent_2182_ventes() -> None:
    ventes = charger_ventes(DONNEES / "brut" / "ventes")
    assert ventes.shape == (2182, 8)
    assert ventes["fichier"].nunique() == 9


def test_enrichir_garde_les_17_ventes_hors_catalogue(ventes_enrichies: pd.DataFrame) -> None:
    assert len(ventes_enrichies) == 2182
    assert (ventes_enrichies["categorie"] == NON_REFERENCE).sum() == 17
    assert ventes_enrichies["montant"].sum() == pytest.approx(409501.59, abs=0.01)


def test_table_des_indicateurs(ventes_enrichies: pd.DataFrame) -> None:
    indicateurs = indicateurs_mois_region(ventes_enrichies)
    assert list(indicateurs.columns) == COLONNES_INDICATEURS
    assert indicateurs.shape == (54, 8)
    assert indicateurs["nb_commandes"].sum() == 2182
    assert indicateurs["ca"].sum() == pytest.approx(409501.59, abs=0.01)
    assert (indicateurs["taux_realisation"] >= 1).sum() == 25


def test_filtrer_l_ete(ventes_enrichies: pd.DataFrame) -> None:
    ete = filtrer_periode(ventes_enrichies, "2025-07", "2025-08")
    assert len(ete) == 307
    assert ete["date"].min() >= pd.Timestamp("2025-07-01")
    assert ete["date"].max() < pd.Timestamp("2025-09-01")


def test_commande_de_bout_en_bout(tmp_path: Path) -> None:
    config = ecrire_config(tmp_path, DONNEES / "brut" / "ventes")
    assert main(["--config", str(config), "--debut", "2025-07", "--fin", "2025-08"]) == 0
    assert len(pd.read_parquet(tmp_path / "indicateurs.parquet")) == 12
    assert (tmp_path / "ventes.log").read_text(encoding="utf-8"), "le journal doit être écrit dans le fichier configuré"


def test_commande_avec_un_fichier_defectueux(tmp_path: Path) -> None:
    dossier_ventes = tmp_path / "ventes"
    shutil.copytree(DONNEES / "brut" / "ventes", dossier_ventes)
    shutil.copy(DONNEES / "exemples_erreurs" / "ventes_sans_quantite.csv", dossier_ventes / "ventes_2025_10.csv")
    config = ecrire_config(tmp_path, dossier_ventes)
    assert main(["--config", str(config)]) == 1
    journal = (tmp_path / "ventes.log").read_text(encoding="utf-8")
    assert "ventes_2025_10.csv" in journal and "quantite" in journal, "le message doit citer le fichier et la colonne"
