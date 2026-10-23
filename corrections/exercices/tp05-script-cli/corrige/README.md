# Corrigé du TP5

Une solution complète du TP5. Elle utilise les données du TP (`exercices/tp05-script-cli/data/brut`).

```bash
uv sync
uv run pytest
uv run ventes
uv run ventes --debut 2025-07 --fin 2025-08 --sortie outputs/ete.parquet
uv run ruff check .
uv run mypy src
```
