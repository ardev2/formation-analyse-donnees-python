import argparse
import logging
import sys
from pathlib import Path

from ventes.chargement import charger_reference, charger_ventes
from ventes.config import charger_config
from ventes.erreurs import VentesError
from ventes.indicateurs import enrichir, filtrer_periode, indicateurs_mois_region

logger = logging.getLogger("ventes")

FORMAT_JOURNAL = "%(asctime)s %(levelname)-8s %(name)s : %(message)s"


def creer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ventes",
        description="Consolide les fichiers de ventes mensuels et calcule les indicateurs par mois et par région.",
    )
    parser.add_argument(
        "-c", "--config", type=Path, default=Path("config.yaml"), help="fichier de configuration (défaut : config.yaml)"
    )
    parser.add_argument(
        "-o", "--sortie", type=Path, help="fichier Parquet de sortie, remplace celui de la configuration"
    )
    parser.add_argument("--debut", help="premier mois à inclure, au format AAAA-MM")
    parser.add_argument("--fin", help="dernier mois à inclure, au format AAAA-MM")
    parser.add_argument("-v", "--verbose", action="store_true", help="affiche le détail du traitement")
    return parser


def configurer_console(verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format=FORMAT_JOURNAL)


def ajouter_fichier_journal(fichier: Path) -> None:
    fichier.parent.mkdir(parents=True, exist_ok=True)
    journal = logging.FileHandler(fichier, encoding="utf-8")
    journal.setFormatter(logging.Formatter(FORMAT_JOURNAL))
    logging.getLogger().addHandler(journal)


def executer(args: argparse.Namespace) -> Path:
    config = charger_config(args.config)
    ajouter_fichier_journal(Path(config["sorties"]["journal"]))
    donnees = config["donnees"]

    ventes = charger_ventes(Path(donnees["ventes"]))
    produits = charger_reference(Path(donnees["produits"]), "id_produit")
    regions = charger_reference(Path(donnees["regions"]), "code_region")

    df = filtrer_periode(enrichir(ventes, produits, regions), args.debut, args.fin)
    indicateurs = indicateurs_mois_region(df)

    sortie = args.sortie or Path(config["sorties"]["indicateurs"])
    sortie.parent.mkdir(parents=True, exist_ok=True)
    indicateurs.to_parquet(sortie, index=False)
    logger.info("%d lignes d'indicateurs écrites dans %s", len(indicateurs), sortie)
    return sortie


def main(argv: list[str] | None = None) -> int:
    args = creer_parser().parse_args(argv)
    configurer_console(args.verbose)
    try:
        executer(args)
    except VentesError as erreur:
        logger.error("%s", erreur)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
