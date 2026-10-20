class VentesError(Exception):
    """Erreur de base du traitement des ventes."""


class ConfigurationError(VentesError):
    """Fichier de configuration absent, invalide ou incomplet."""


class DossierVideError(VentesError):
    """Aucun fichier de ventes trouvé.

    TODO : écrire un constructeur qui reçoit le dossier et le pattern de recherche,
    et produit un message du type « aucun fichier *.csv dans data/brut/ventes ».
    """


# TODO : ColonnesManquantesError, levée quand un fichier de ventes n'a pas toutes les
# colonnes attendues. Elle garde en attributs le fichier (Path) et les colonnes manquantes (set[str]).

# TODO : CleNonUniqueError, levée quand une clé censée être unique (id_commande, id_produit,
# code_region) contient des doublons.
