import argparse
import logging
import sys

logger = logging.getLogger("ventes")


def creer_parser() -> argparse.ArgumentParser:
    """Déclare les paramètres de la commande : --config, --sortie, --debut, --fin, --verbose."""
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée de la commande ventes.

    Étapes : lire les arguments, configurer les journaux, lire la configuration,
    charger et enrichir les ventes, calculer les indicateurs, écrire le fichier Parquet.
    Renvoie 0 en cas de succès, 1 si une VentesError a été levée.
    """
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
