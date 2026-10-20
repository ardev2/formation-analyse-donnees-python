from pathlib import Path
from typing import Any


def charger_config(chemin: Path) -> dict[str, Any]:
    """Lit le fichier de configuration YAML et vérifie la présence des clés obligatoires.

    Lève ConfigurationError si le fichier est absent, invalide ou incomplet.
    """
    raise NotImplementedError
