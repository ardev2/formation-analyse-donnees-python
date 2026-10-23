import base64
import io
from dataclasses import dataclass
from html import escape

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from rapport_ventes import graphiques


@dataclass
class ChiffresCles:
    ca: float
    nb_commandes: int
    panier_moyen: float
    debut: pd.Timestamp
    fin: pd.Timestamp


def chiffres_cles(df: pd.DataFrame) -> ChiffresCles:
    return ChiffresCles(
        ca=float(df["montant"].sum()),
        nb_commandes=int(df["id_commande"].nunique()),
        panier_moyen=float(df["montant"].mean()),
        debut=df["date"].min(),
        fin=df["date"].max(),
    )


def alertes(indicateurs: pd.DataFrame, seuil: float) -> pd.DataFrame:
    dernier_mois = indicateurs["mois"].max()
    sous_seuil = indicateurs[(indicateurs["mois"] == dernier_mois) & (indicateurs["taux_realisation"] < seuil)]
    return sous_seuil[["region", "ca", "objectif_mensuel", "taux_realisation"]].sort_values("taux_realisation")


def figure_en_base64(fig: Figure) -> str:
    tampon = io.BytesIO()
    fig.savefig(tampon, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(tampon.getvalue()).decode("ascii")


def euros(valeur: float) -> str:
    return f"{valeur:,.0f} €".replace(",", " ")


def construire_html(df: pd.DataFrame, indicateurs: pd.DataFrame, titre: str, seuil: float) -> str:
    chiffres = chiffres_cles(df)
    liste_alertes = alertes(indicateurs, seuil)
    top_produits = df.groupby("produit")["montant"].sum().nlargest(5)

    images = {
        nom: figure_en_base64(fonction(indicateurs))
        for nom, fonction in [
            ("mensuel", graphiques.ca_mensuel),
            ("regions", graphiques.ca_par_region),
            ("taux", graphiques.taux_realisation),
        ]
    }

    if liste_alertes.empty:
        bloc_alertes = f"<p>Toutes les régions atteignent au moins {seuil:.0%} de leur objectif.</p>"
    else:
        lignes = "".join(
            f"<tr><td>{escape(r.region)}</td><td>{euros(r.ca)}</td><td>{euros(r.objectif_mensuel)}</td>"
            f"<td>{r.taux_realisation:.0%}</td></tr>"
            for r in liste_alertes.itertuples()
        )
        bloc_alertes = (
            "<table><tr><th>Région</th><th>Chiffre d'affaires</th><th>Objectif</th><th>Réalisé</th></tr>"
            f"{lignes}</table>"
        )

    lignes_produits = "".join(
        f"<tr><td>{escape(produit)}</td><td>{euros(ca)}</td></tr>" for produit, ca in top_produits.items()
    )

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{escape(titre)}</title>
<style>
body {{ font-family: Calibri, Arial, sans-serif; color: #1F2933; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
h1, h2 {{ color: #1F3A5F; }}
.chiffres {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
.chiffre {{ background: #EEF3F7; border-radius: 8px; padding: 1rem 1.5rem; flex: 1; min-width: 180px; }}
.chiffre strong {{ display: block; font-size: 1.8rem; color: #1F3A5F; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border-bottom: 1px solid #D5DCE3; padding: 0.4rem 0.6rem; text-align: left; }}
th {{ background: #1F3A5F; color: white; }}
img {{ max-width: 100%; }}
</style>
</head>
<body>
<h1>{escape(titre)}</h1>
<p>Période du {chiffres.debut:%d/%m/%Y} au {chiffres.fin:%d/%m/%Y}.</p>
<div class="chiffres">
  <div class="chiffre"><strong>{euros(chiffres.ca)}</strong>chiffre d'affaires</div>
  <div class="chiffre"><strong>{chiffres.nb_commandes}</strong>commandes</div>
  <div class="chiffre"><strong>{euros(chiffres.panier_moyen)}</strong>panier moyen</div>
</div>
<h2>Évolution mensuelle</h2>
<img alt="Chiffre d'affaires mensuel" src="data:image/png;base64,{images["mensuel"]}">
<h2>Répartition par région</h2>
<img alt="Chiffre d'affaires par région" src="data:image/png;base64,{images["regions"]}">
<h2>Objectifs</h2>
<img alt="Taux de réalisation par région et par mois" src="data:image/png;base64,{images["taux"]}">
<h2>Alertes du dernier mois : régions sous {seuil:.0%} de l'objectif</h2>
{bloc_alertes}
<h2>Les cinq produits qui rapportent le plus</h2>
<table><tr><th>Produit</th><th>Chiffre d'affaires</th></tr>{lignes_produits}</table>
</body>
</html>
"""
