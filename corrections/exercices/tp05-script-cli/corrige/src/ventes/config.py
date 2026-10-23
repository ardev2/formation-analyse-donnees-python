from pathlib import Path
from typing import Any

import yaml

from ventes.erreurs import ConfigurationError

CLES_OBLIGATOIRES = {
    "donnees": {"ventes", "produits", "regions"},
    "sorties": {"indicateurs", "journal"},
}


def charger_config(chemin: Path) -> dict[str, Any]:
    if not chemin.exists():
        raise ConfigurationError(f"fichier de configuration introuvable : {chemin}")
    with chemin.open(encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f) or {}
        except yaml.YAMLError as erreur:
            raise ConfigurationError(f"{chemin} n'est pas un fichier YAML valide") from erreur
    for section, cles in CLES_OBLIGATOIRES.items():
        manquantes = cles - set(config.get(section, {}))
        if manquantes:
            raise ConfigurationError(f"{chemin.name} : clés manquantes dans {section} : {sorted(manquantes)}")
    return config
