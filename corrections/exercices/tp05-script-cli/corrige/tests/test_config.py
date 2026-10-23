from pathlib import Path

import pytest

from ventes.config import charger_config
from ventes.erreurs import ConfigurationError


def test_config_absente(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError):
        charger_config(tmp_path / "absent.yaml")


def test_config_incomplete(tmp_path: Path) -> None:
    chemin = tmp_path / "config.yaml"
    chemin.write_text("donnees:\n  ventes: data/brut/ventes\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="clés manquantes"):
        charger_config(chemin)


def test_config_yaml_invalide(tmp_path: Path) -> None:
    chemin = tmp_path / "config.yaml"
    chemin.write_text("donnees: [ventes\n", encoding="utf-8")
    with pytest.raises(ConfigurationError, match="YAML"):
        charger_config(chemin)
