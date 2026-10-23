import argparse
import logging
import sys
from pathlib import Path

from rapport_ventes.chargement import charger_reference, charger_ventes
from rapport_ventes.config import charger_config
from rapport_ventes.erreurs import VentesError
from rapport_ventes.indicateurs import enrichir, filtrer_periode, indicateurs_mois_region
from rapport_ventes.rapport import construire_html

logger = logging.getLogger("rapport_ventes")

FORMAT_JOURNAL = "%(asctime)s %(levelname)-8s %(name)s : %(message)s"


def creer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rapport-ventes",
        description="Produit le rapport HTML des ventes : chiffres clés, graphiques et alertes sur les objectifs.",
    )
    parser.add_argument("-c", "--config", type=Path, default=Path("config.yaml"), help="fichier de configuration")
    parser.add_argument("--debut", help="premier mois à inclure, au format AAAA-MM")
    parser.add_argument("--fin", help="dernier mois à inclure, au format AAAA-MM")
    parser.add_argument("-v", "--verbose", action="store_true", help="affiche le détail du traitement")
    return parser


def configurer_journal(fichier: Path, verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format=FORMAT_JOURNAL)
    fichier.parent.mkdir(parents=True, exist_ok=True)
    journal = logging.FileHandler(fichier, encoding="utf-8")
    journal.setFormatter(logging.Formatter(FORMAT_JOURNAL))
    logging.getLogger().addHandler(journal)


def executer(args: argparse.Namespace) -> Path:
    config = charger_config(args.config)
    configurer_journal(Path(config["sorties"]["journal"]), args.verbose)
    donnees = config["donnees"]

    ventes = charger_ventes(Path(donnees["ventes"]))
    produits = charger_reference(Path(donnees["produits"]), "id_produit")
    regions = charger_reference(Path(donnees["regions"]), "code_region")
    df = filtrer_periode(enrichir(ventes, produits, regions), args.debut, args.fin)
    indicateurs = indicateurs_mois_region(df)

    dossier = Path(config["sorties"]["dossier"])
    dossier.mkdir(parents=True, exist_ok=True)
    indicateurs.to_parquet(dossier / "indicateurs_mois_region.parquet", index=False)

    html = construire_html(df, indicateurs, config["rapport"]["titre"], config["rapport"]["seuil_alerte"])
    rapport = dossier / "rapport.html"
    rapport.write_text(html, encoding="utf-8")
    logger.info("rapport écrit dans %s", rapport)
    return rapport


def main(argv: list[str] | None = None) -> int:
    args = creer_parser().parse_args(argv)
    try:
        executer(args)
    except VentesError as erreur:
        logging.basicConfig(format=FORMAT_JOURNAL)
        logger.error("%s", erreur)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
