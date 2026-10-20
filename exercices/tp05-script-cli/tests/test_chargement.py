from pathlib import Path

import pytest

from ventes.chargement import lister_fichiers
from ventes.erreurs import DossierVideError


def test_lister_fichiers_dossier_vide(tmp_path: Path) -> None:
    with pytest.raises(DossierVideError):
        lister_fichiers(tmp_path)


# TODO : tester charger_fichier_ventes sur un petit fichier écrit dans tmp_path :
# - un fichier valide reçoit bien la colonne fichier et une colonne date au bon type ;
# - un fichier sans colonne quantite lève ColonnesManquantesError, dont l'attribut manquantes vaut {"quantite"}.

# TODO : tester charger_reference sur un petit fichier de produits dont la clé id_produit
# apparaît deux fois : la fonction doit lever CleNonUniqueError.
