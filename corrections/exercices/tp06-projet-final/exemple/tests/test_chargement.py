from pathlib import Path

import pandas as pd
import pytest

from rapport_ventes.chargement import charger_fichier_ventes, charger_reference, lister_fichiers
from rapport_ventes.erreurs import CleNonUniqueError, ColonnesManquantesError, DossierVideError


def test_lister_fichiers_dossier_vide(tmp_path: Path) -> None:
    with pytest.raises(DossierVideError):
        lister_fichiers(tmp_path)


def test_charger_fichier_colonne_manquante(tmp_path: Path) -> None:
    fichier = tmp_path / "ventes.csv"
    fichier.write_text(
        "id_commande,date,code_region,id_produit,prix_unitaire,client_fidele\n1,2025-01-02,IDF,P01,10.0,True\n"
    )
    with pytest.raises(ColonnesManquantesError) as erreur:
        charger_fichier_ventes(fichier)
    assert erreur.value.manquantes == {"quantite"}


def test_charger_fichier_ajoute_origine(tmp_path: Path) -> None:
    fichier = tmp_path / "ventes_2025_01.csv"
    fichier.write_text(
        "id_commande,date,code_region,id_produit,quantite,prix_unitaire,client_fidele\n1,2025-01-02,IDF,P01,2,10.0,True\n"
    )
    ventes = charger_fichier_ventes(fichier)
    assert ventes["fichier"].tolist() == ["ventes_2025_01.csv"]
    assert pd.api.types.is_datetime64_any_dtype(ventes["date"])


def test_reference_avec_doublon(tmp_path: Path) -> None:
    fichier = tmp_path / "produits.csv"
    fichier.write_text("id_produit,produit\nP01,Souris\nP01,Clavier\n")
    with pytest.raises(CleNonUniqueError):
        charger_reference(fichier, "id_produit")
