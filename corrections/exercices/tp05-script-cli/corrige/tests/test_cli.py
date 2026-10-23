from pathlib import Path

import pandas as pd

from ventes.cli import main

LIGNE = (
    "id_commande,date,code_region,id_produit,quantite,prix_unitaire,client_fidele\n1,2025-01-02,IDF,P01,2,10.0,True\n"
)


def preparer_projet(dossier: Path) -> Path:
    (dossier / "ventes").mkdir()
    (dossier / "ventes" / "ventes_2025_01.csv").write_text(LIGNE, encoding="utf-8")
    (dossier / "produits.csv").write_text("id_produit,produit,categorie\nP01,Souris,Informatique\n", encoding="utf-8")
    (dossier / "regions.csv").write_text(
        "code_region,region,objectif_mensuel\nIDF,Île-de-France,100\n", encoding="utf-8"
    )
    config = dossier / "config.yaml"
    config.write_text(
        f"donnees:\n  ventes: {dossier / 'ventes'}\n  produits: {dossier / 'produits.csv'}\n"
        f"  regions: {dossier / 'regions.csv'}\n"
        f"sorties:\n  indicateurs: {dossier / 'sortie.parquet'}\n  journal: {dossier / 'ventes.log'}\n",
        encoding="utf-8",
    )
    return config


def test_main_de_bout_en_bout(tmp_path: Path) -> None:
    config = preparer_projet(tmp_path)
    assert main(["--config", str(config)]) == 0
    assert pd.read_parquet(tmp_path / "sortie.parquet")["ca"].item() == 20.0


def test_main_code_erreur(tmp_path: Path) -> None:
    assert main(["--config", str(tmp_path / "absent.yaml")]) == 1
