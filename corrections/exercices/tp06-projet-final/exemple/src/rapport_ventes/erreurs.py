from pathlib import Path


class VentesError(Exception):
    """Erreur de base du traitement des ventes."""


class ConfigurationError(VentesError):
    """Fichier de configuration absent ou incomplet."""


class DossierVideError(VentesError):
    """Aucun fichier de ventes trouvé."""

    def __init__(self, dossier: Path, pattern: str) -> None:
        super().__init__(f"aucun fichier {pattern} dans {dossier}")


class ColonnesManquantesError(VentesError):
    """Un fichier ne contient pas toutes les colonnes attendues."""

    def __init__(self, fichier: Path, manquantes: set[str]) -> None:
        self.fichier = fichier
        self.manquantes = manquantes
        super().__init__(f"{fichier.name} : colonnes manquantes {sorted(manquantes)}")


class CleNonUniqueError(VentesError):
    """Une clé censée être unique contient des doublons."""

    def __init__(self, source: str, cle: str, nb_doublons: int) -> None:
        super().__init__(f"{source} : {nb_doublons} valeur(s) en double dans la clé {cle}")
