import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger("ventes")


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


def main(argv: list[str] | None = None) -> int:
    args = creer_parser().parse_args(argv)
    print(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
